from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.models.like import Like

like_api = Redprint('like')


@like_api.route('/product/<int:pid>', methods=['PUT'])
# @member_login_required
def like(pid):
    # member = get_current_member()
    Like.like(pid, 1)
    return Success(msg='点赞成功')


@like_api.route('/cancel/product/<int:pid>', methods=['PUT'])
# @member_login_required
def like_cancel(pid):
    # member = get_current_member()
    Like.unlike(pid, 1)
    return Success(msg='取消点赞成功')


@like_api.route('/info/product/<int:pid>', methods=['GET'])
# @member_login_required
def get_info(pid):
    # member = get_current_member()
    info = Like.get_like(pid, 1)
    return info
