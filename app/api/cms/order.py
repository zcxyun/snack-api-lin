from flask import request, jsonify
from lin import route_meta, group_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.order import Order
from app.services.order import OrderService
from app.validators.cms.order_forms import DeliveryForm

order_api = Redprint('order')


@order_api.route('/paginate', methods=['GET'])
@route_meta(auth='分页查询所有订单', module='订单')
@group_required
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    res = Order.get_paginate_with_member(start, count, q, throw=True)
    for model in res['models']:
        model._fields = ['member', 'member_avatarurl', 'order_no', 'total_price_str', 'total_count',
                         'order_status_desc', 'pay_time_format', 'create_time_str']
    return jsonify(res)


@order_api.route('/delivery', methods=['POST'])
@route_meta(auth='订单发货', module='订单')
@group_required
def delivery():
    form = DeliveryForm().validate_for_api()
    OrderService().delivery(form.member_id.data, form.order_id.data)
    return Success(msg='发货成功')
