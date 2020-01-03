import json
import uuid

from lin import db

from app.libs.enum import OrderStatus
from app.libs.error_code import OrderNotFound, ProductNotFound, OrderNotPay
from app.models.member_address import MemberAddress
from app.models.order import Order
from app.models.order_product import OrderProduct
from app.models.product import Product


class OrderService:

    def __init__(self, mid=None, o_products=None):
        if mid:
            self.mid = mid
        if o_products:
            self.o_products = o_products
            self.products = self._get_products_by_order(o_products)

    def check_order_stock(self, order_id):
        self.o_products = OrderProduct.query.filter_by(order_id=order_id).first_or_404(OrderNotFound())
        self.products = self._get_products_by_order(self.o_products)
        status = self._get_order_status()
        return status

    def send_tpl_msg(self, order_id, jump_page=''):
        order = Order.query.get_or_404(order_id, OrderNotFound())
        if order.order_status_enum != OrderStatus.PAID:
            raise OrderNotPay()
        with db.auto_commit():
            order.order_status_enum = OrderStatus.DELIVERED
            db.session.add(order)

    def place(self):
        status = self._get_order_status()
        if not status['pass']:
            status['order_id'] = -1
            return status
        order_snap = self._snap_order()
        status = self._create_order_by_trans(order_snap)
        status['pass'] = True
        return status

    @staticmethod
    def _get_products_by_order(o_products):
        product_ids = [item.product_id for item in o_products]
        products = Product.query.filter(Product.id.in_(product_ids), Product.status != 0).all()
        return products

    def _get_order_status(self):
        status = {
            'pass': True,
            'order_price': 0,
            'p_status_array': []
        }
        for o_product in self.o_products:
            product = self.check_product_exist(o_product['product_id'])
            p_status = self._get_product_status(o_product, product)
            if not p_status['have_stock']:
                status['pass'] = False
            status['order_price'] += p_status['total_price']
            status['p_status_array'].append(p_status)
        return status

    def check_product_exist(self, product_id):
        product_exist = filter(lambda x: x.id == product_id, self.products)
        if product_exist:
            product = product_exist[0]
        else:
            raise ProductNotFound(error_code=2000, msg='id为{}的商品不存在，订单创建失败'.format(product_id))
        return product

    def _get_product_status(self, o_product, product):
        p_status = dict()
        p_status['id'] = product.id
        p_status['name'] = product.name
        p_status['count'] = o_product['count']
        p_status['total_price'] = product.price * o_product['count']
        p_status['have_stock'] = product.stock >= o_product['count']
        return p_status

    def _snap_order(self):
        snap = {
            'order_price': 0,
            'total_count': 0,
            'p_status': [],
            'snap_address': json.dumps(self._get_member_address()),
            'snap_name': self.products[0].name,
            'snap_img': self.products[0].main_img_url
        }
        if len(self.products) > 1:
            snap['snap_name'] += '等'
        for i in range(len(self.products)):
            product = self.products[i]
            o_product = self.o_products[i]
            p_status = self._snap_product(product, o_product['count'])
            snap['order_price'] += p_status['total_price']
            snap['total_count'] += p_status['count']
            snap['p_status'].append(p_status)
        return snap

    def _get_member_address(self):
        user_address = MemberAddress.get_by_member_id(self.mid, err_msg="相关地址不存在")
        return dict(user_address)

    def _snap_product(self, product, o_count):
        p_status = dict()
        p_status['id'] = product.id
        p_status['name'] = product.name
        p_status['main_img_url'] = product.main_img_url
        p_status['total_price'] = product.price * o_count
        p_status['price'] = product.price
        p_status['count'] = o_count
        return p_status

    def _create_order_by_trans(self, order_snap):
        with db.auto_commit():
            order = Order()
            order.member_id = self.mid
            order.order_no = self.get_order_no()
            order.total_price = order_snap['order_price']
            order.total_count = order_snap['total_count']
            order.snap_name = order_snap['snap_name']
            order.snap_img = order_snap['snap_img']
            order.snap_address = order_snap['snap_address']
            order.snap_items = json.dumps(order_snap['p_status'])
            db.session.add(order)
        with db.auto_commit():
            for item in self.o_products:
                order_product = OrderProduct()
                order_product.order_id = order.id
                order_product.product_id = item['product_id']
                order_product.count = item['count']
                db.session.add(order_product)
        return {
            'order_no': order.order_no,
            'order_id': order.id,
            'create_time': order.format_create_time
        }

    @staticmethod
    def get_order_no():
        return str(uuid.uuid1()).replace('-', '')
