import json
import uuid
from decimal import Decimal

from lin import db
from lin.exception import NotFound, Failed

from app.libs.enum import OrderStatus
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
            'total_count': 0,
            'snap_products': [],
            'snap_address': json.dumps(self._get_member_address()),
            'snap_name': ', '.join([item.name for item in self.o_products]),
            'snap_img': self.o_products[0].image
        }
        for product in self.products:
            o_product = self.check_product_exist(product['product_id'])
            p_status = self._get_product_status(product, o_product)
            snap['total_price'] += Decimal(p_status['total_price'])
            snap['total_count'] += p_status['count']
            snap['snap_products'].append(p_status)
        snap['snap_products'] = json.dumps(snap['snap_products'])
        return snap

    def check_product_exist(self, product_id):
        product_exist = list(filter(lambda x: x.id == product_id, self.o_products))
        if product_exist:
            product = product_exist[0]
        else:
            raise NotFound(msg='id为{}的商品不存在，订单创建失败'.format(product_id))
        return product

    def _get_product_status(self, product, o_product):
        total_price = str((o_product.price * product['count']).quantize(Decimal('0.00')))
        p_status = dict()
        p_status['id'] = o_product.id
        p_status['name'] = o_product.name
        p_status['count'] = product['count']
        p_status['price'] = o_product.price_str
        p_status['total_price'] = total_price
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
            'create_time': order.create_time
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
        member_address = MemberAddress.get_by_member_id(self.mid)
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
