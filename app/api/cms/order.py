from datetime import datetime

from flask import request, jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.order import Order
from app.services.order import OrderService
from app.validators.cms.order_forms import DeliveryForm
from app.validators.common import DatetimeSection

order_api = Redprint('order')


@order_api.route('/get/<int:oid>', methods=['GET'])
@route_meta(auth='查询指定订单', module='订单')
# @group_required
def get(oid):
    model = Order.get_model(oid, throw=True)
    model.hide('deadline_str', 'order_status')
    return jsonify(model)


@order_api.route('/paginate', methods=['GET'])
@route_meta(auth='分页查询所有订单', module='订单')
@group_required
def get_paginate():
    form = DatetimeSection().validate_for_api()
    date_start = form.date_start.data
    date_end = form.date_end.data
    start, count = paginate()
    q = request.args.get('q', None)
    order_status = request.args.get('order_status', None)
    res = Order.get_paginate_with_member(start, count, q, order_status, date_start, date_end, throw=True)
    for model in res['models']:
        model._fields = ['member_id', 'member_name', 'member_avatarurl', 'id', 'order_no', 'total_price_str',
                         'total_count', 'order_status_desc', 'pay_time_format', 'create_time_str']
    return jsonify(res)


@order_api.route('/delivery', methods=['POST'])
@route_meta(auth='订单发货', module='订单')
@group_required
def delivery():
    form = DeliveryForm().validate_for_api()
    OrderService().delivery(form.member_id.data, form.order_id.data)
    return Success(msg='发货成功')


@order_api.route('/all/order_status', methods=['GET'])
@route_meta(auth='查询订单所有状态', module='订单', mount=False)
@login_required
def get_all_order_status():
    status_map = Order.get_status_map()
    res = {order_enum.value: desc for order_enum, desc in status_map.items()}
    return jsonify(res)
