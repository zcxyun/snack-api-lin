import json
import uuid
from decimal import Decimal

from flask import current_app
from lin import db
from lin.exception import NotFound, Failed

from app.libs.enum import OrderStatus
from app.libs.error_code import WxPayException
from app.libs.wx_helper import WxHelper
from app.models.member_address import MemberAddress
from app.models.order import Order
from app.models.order_product import OrderProduct
from app.models.product import Product


class OrderService:

    def __init__(self, mid=None, products=None):
        if mid:
            self.mid = mid
        if products:
            self.products = products

    def _get_o_products(self):
        product_ids = [item['product_id'] for item in self.products if 'product_id' in item]
        o_products = Product.get_models_by_ids_with_img(product_ids, with_for_update=True, throw=True)
        return o_products

    def place(self):
        if not self.mid or not self.products:
            raise Failed(msg='缺少会员ID和商品参数, 下单失败')
        with db.auto_commit():
            self.o_products = self._get_o_products()
            order_snap = self._snap_order()
            res = self._create_order(order_snap)
        return res

    def _snap_order(self):
        snap = {
            'total_price': 0,
            'old_total_price': 0,
            'total_count': 0,
            'snap_products': [],
            'snap_address': json.dumps(self._get_member_address(), ensure_ascii=False),
            'snap_name': ', '.join([item.name for item in self.o_products]),
            'snap_img': self.o_products[0].image
        }
        for product in self.products:
            o_product = self.check_product_exist(product['product_id'])
            p_status = self._get_product_status(product, o_product)
            snap['total_price'] += Decimal(p_status['total_price_str'])
            snap['old_total_price'] += Decimal(p_status['old_total_price_str'])
            snap['total_count'] += p_status['count']
            snap['snap_products'].append(p_status)
        snap['snap_products'] = json.dumps(snap['snap_products'], ensure_ascii=False)
        return snap

    def check_product_exist(self, product_id):
        product_exist = list(filter(lambda x: x.id == product_id, self.o_products))
        if product_exist:
            product = product_exist[0]
        else:
            raise NotFound(msg='id为{}的商品不存在，订单创建失败'.format(product_id))
        return product

    def _get_product_status(self, product, o_product):
        total_price = (o_product.price * product['count']).quantize(Decimal('0.00'))
        old_price = o_product.old_price if o_product.old_price else o_product.price
        old_total_price = (old_price * product['count']).quantize(Decimal('0.00'))
        p_status = dict()
        p_status['id'] = o_product.id
        p_status['name'] = o_product.name
        p_status['count'] = product['count']
        p_status['image'] = o_product.image
        p_status['price_str'] = o_product.price_str
        p_status['old_price_str'] = o_product.old_price_str
        p_status['total_price_str'] = str(total_price)
        p_status['old_total_price_str'] = str(old_total_price)
        have_stock = o_product.stock >= product['count']
        if not have_stock:
            raise Failed(msg='{}的库存不足, 下单失败'.format(o_product.name))
        stock = o_product.stock - product['count']
        o_product.update(stock=stock)
        return p_status

    def _create_order(self, order_snap):
        order_snap['member_id'] = self.mid
        order_snap['order_no'] = self.get_order_no()
        order = Order.create(**order_snap)
        db.session.flush()
        for item in self.products:
            OrderProduct.create(order_id=order.id, product_id=item['product_id'], count=item['count'])
        return {
            'order_no': order.order_no,
            'order_id': order.id,
            'create_time': order.create_time_str
        }

    @staticmethod
    def get_order_no():
        return str(uuid.uuid1()).replace('-', '')

    def check_order_stock(self, order_id):
        o_products, ids_products, _ = self.get_stock_data(order_id)
        res = list(filter(lambda x: x.stock < ids_products[x.id].count, o_products))
        if res:
            return False
        return True

    def _get_member_address(self):
        member_address = MemberAddress.get_by_member_id(self.mid, throw=True)
        return dict(member_address)

    def get_stock_data(self, order_id):
        order_products = OrderProduct.get_by_order_id(order_id, throw=True)
        product_ids = [item.product_id for item in order_products]
        o_products = Product.get_models_by_ids(product_ids, throw=True)
        ids_products = {item.product_id: item for item in order_products}
        return o_products, ids_products, order_products

    def cancel(self, member_id, order_id):
        order = Order.query.filter_by(soft=True, member_id=member_id, id=order_id).filter(
            Order.order_status == OrderStatus.UNPAID.value
        ).first()
        if not order:
            raise NotFound(msg='订单不存在或订单不是待支付状态')
        with db.auto_commit():
            order.update(order_status=OrderStatus.CANCEL.value)
            o_products, ids_products, order_products = self.get_stock_data(order_id)
            for o_product in o_products:
                o_stock = o_product.stock + ids_products[o_product.id]['count']
                o_product.update(stock=o_stock)
            for item in order_products:
                item.delete()
        return True

    def confirm(self, member_id, order_id):
        order = Order.query.filter_by(soft=True, member_id=member_id, id=order_id).filter(
            Order.order_status == OrderStatus.UNRECEIPTED.value
        ).first()
        if not order:
            raise NotFound(msg='订单不存在或订单不是待收货状态')
        order.update(order_status=OrderStatus.DONE.value, commit=True)
        return True

    def delivery(self, member_id, order_id):
        order = Order.query.filter_by(soft=True, member_id=member_id, id=order_id).filter(
            Order.order_status == OrderStatus.UNDELIVERED.value
        ).first()
        if not order:
            raise NotFound(msg='订单不是待发货状态')
        order.update(order_status=OrderStatus.UNRECEIPTED.value, commit=True)
        return True

    def pay(self, member_id, openid, order_id):
        order = Order.query.filter_by(member_id=member_id, id=order_id, soft=True).first()
        if not order:
            raise NotFound(msg='指定订单不存在')

        mina_config = current_app.config['WE_CHAT']
        notify_url = current_app.config['SITE_DOMAIN'] + mina_config['PAY_NOTIFY_URL']

        wx_helper = WxHelper(merchant_key=mina_config['PAY_KEY'])

        pay_data = {
            'appid': mina_config['APP_ID'],
            'mch_id': mina_config['MCH_ID'],
            'nonce_str': wx_helper.get_random_str(),
            'body': 'snack',
            'out_trade_no': order.order_no,
            'total_fee': int(order.total_price * 100),
            'notify_url': notify_url,
            'trade_type': 'JSAPI',
            'openid': openid
        }
        pay_info = wx_helper.get_pay_info(pay_data)
        if pay_info:
            # 保存prepay_id为了后面发模板消息
            order.update(prepay_id=pay_info['prepay_id'], commit=True)
        else:
            raise WxPayException()
        return pay_info
