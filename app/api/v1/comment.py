from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.models.comment import Comment
from app.validators.v1.comment_forms import CommentContent

comment_api = Redprint('comment')


@comment_api.route('/product/<int:pid>', methods=['GET'])
def get_comments_of_product(pid):
    models = Comment.get_comments_of_product(pid)
    return models


@comment_api.route('', methods=['POST'])
# @member_login_required
def create_comment():
    form = CommentContent().validate_for_api()
    # member = get_current_member()
    data = {
        'member_id': 1,
        **form.data
    }
    Comment.add(data, err_msg='相同内容已经评论过了')
    return Success(msg='评论成功')
