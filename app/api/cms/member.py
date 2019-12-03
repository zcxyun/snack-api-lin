from flask import request
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.member import Member

member_api = Redprint('member')


@member_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Member.get_paginate_models(start, count, q, err_msg='相关会员不存在')
    return models
