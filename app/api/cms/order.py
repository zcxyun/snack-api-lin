from flask import request, jsonify
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.order import Order

order_api = Redprint('order')


@order_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    res = Order.get_paginate_with_member(start, count, q, throw=True)
    return jsonify(res)
