from flask import jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.libs.utils import paginate
from app.models.order import Order
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
@member_login_required
def cancel(oid):
    member = get_current_member()
    OrderService().cancel(member.id, oid)
    return Success(msg='订单已取消')


@order_api.route('/<int:oid>/confirm', methods=['POST'])
@member_login_required
def confirm(oid):
    member = get_current_member()
    OrderService().confirm(member.id, oid)
    return Success(msg='订单已确认')


@order_api.route('/<int:oid>', methods=['GET'])
def get(oid):
    model = Order.get_model(oid, throw=True)
    model.hide('snap_img', 'snap_name')
    return jsonify(model)


@order_api.route('/paginate', methods=['GET'])
@member_login_required
def get_paginate():
    member = get_current_member()
    start, count = paginate()
    res = Order.get_paginate(member.id, start, count, throw=True)
    for order in res['models']:
        order.hide('snap_address', 'snap_products')
    return jsonify(res)


@order_api.route('/paginate/status/<int:status>', methods=['GET'])
@member_login_required
def get_paginate_by_status(status):
    member = get_current_member()
    start, count = paginate()
    res = Order.get_paginate(member.id, start, count, status, throw=True)
    for order in res['models']:
        order.hide('snap_address', 'snap_products')
    return jsonify(res)

