from flask import request
from lin import route_meta, group_required
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.member_address import MemberAddress

address_api = Redprint('address')


@address_api.route('/paginate', methods=['GET'])
@route_meta(auth='分页查询C端会员收货地址', module='C端会员')
@group_required
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = MemberAddress.get_paginate_with_member(start, count, q, throw=True)
    return models
