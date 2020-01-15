from flask import jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.libs.utils import paginate
from app.models.like import Like

like_api = Redprint('like')


@like_api.route('/product/<int:pid>', methods=['PUT'])
@member_login_required
def like(pid):
    member = get_current_member()
    Like.like(pid, member.id)
    return Success(msg='点赞成功')


@like_api.route('/cancel/product/<int:pid>', methods=['PUT'])
@member_login_required
def like_cancel(pid):
    member = get_current_member()
    Like.unlike(pid, member.id)
    return Success(msg='取消点赞成功')


@like_api.route('/info/product/<int:pid>', methods=['GET'])
@member_login_required
def get_info(pid):
    member = get_current_member()
    info = Like.get_like(pid, member.id)
    return info


@like_api.route('/count', methods=['GET'])
@member_login_required
def get_count():
    member = get_current_member()
    count = Like.get_like_count_by_member(member.id)
    return {
        'member_id': member.id,
        'like_count': count
    }


@like_api.route('/products', methods=['GET'])
@member_login_required
def get_like_products():
    member = get_current_member()
    start, count = paginate()
    res = Like.get_like_products(member.id, start, count, throw=True)
    for model in res['models']:
        model._fields = ['id', 'name', 'old_price_str', 'price_str', 'summary', 'image']
    return jsonify(res)
