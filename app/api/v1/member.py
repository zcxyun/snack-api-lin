from flask import jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.validators.v1.member_forms import MemberInfoForm

member_api = Redprint('member')


@member_api.route('/get', methods=['GET'])
@member_login_required
def get():
    member = get_current_member()
    return jsonify(member)


@member_api.route('/update', methods=['POST'])
@member_login_required
def update():
    form = MemberInfoForm().validate_for_api()
    member = get_current_member()
    member.update(
        nickName=form.nickName.data,
        avatarUrl=form.avatarUrl.data,
        gender=form.gender.data,
        country=form.country.data,
        province=form.province.data,
        city=form.city.data,
        commit=True
    )
    return Success(msg='微信用户信息已更改')


