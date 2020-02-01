from flask import request
from lin import route_meta, group_required
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.member import Member

member_api = Redprint('member')


@member_api.route('/paginate', methods=['GET'])
@route_meta(auth='分页查询所有C端会员', module='C端会员')
@group_required
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Member.get_paginate_models(start, count, q, throw=True)
    return models
