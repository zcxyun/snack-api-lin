from flask import request
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.member_address import MemberAddress

address_api = Redprint('address')


@address_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = MemberAddress.get_paginate_models(start, count, q, throw=True)
    return models
