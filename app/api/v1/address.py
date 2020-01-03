from flask import jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.models.member_address import MemberAddress
from app.validators.v1.address_forms import MemberAddressContent

address_api = Redprint('address')


@address_api.route('', methods=['GET'])
@member_login_required
def get():
    member = get_current_member()
    model = MemberAddress.get_address(member.id)
    return jsonify(model)


@address_api.route('', methods=['POST'])
@member_login_required
def update():
    form = MemberAddressContent().validate_for_api()
    member = get_current_member()
    MemberAddress.edit(member.id, form.data)
    return Success(msg='收货人地址更新成功')
