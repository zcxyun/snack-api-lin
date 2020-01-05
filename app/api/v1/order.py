from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.services.order import OrderService
from app.validators.v1.order_forms import validate_place_order

order_api = Redprint('order')


@order_api.route('/place', methods=['POST'])
@member_login_required
def place():
    member = get_current_member()
    products = validate_place_order()
    OrderService(member.id, products).place()
    return Success(msg='下单成功')


@order_api.route('/<int:oid>/cancel', methods=['POST'])
# @member_login_required
def cancel(oid):
    # member = get_current_member()
    OrderService().cancel(1, oid)
    return Success(msg='取消订单成功')


@order_api.route('/<int:oid>/confirm', methods=['POST'])
# @member_login_required
def confirm(oid):
    # member = get_current_member()
    OrderService().confirm(1, oid)
    return Success(msg='确认订单成功')
