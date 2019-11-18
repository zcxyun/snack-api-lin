from functools import wraps

from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from lin.exception import AuthFailed, NotFound

from app.models.member import Member

identity = dict(uid=0, scope='zcx')


def member_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_member_access_token()
        return fn(*args, **kwargs)
    return wrapper


def get_current_member():
    identity = get_jwt_identity()
    if identity['scope'] != 'zcx':
        raise AuthFailed()
    remote_addr = identity.get('remote_addr')
    if remote_addr and remote_addr != request.remote_addr:
        raise AuthFailed()
    # token is granted , member must be exit
    # 如果token已经被颁发，则该用户一定存在
    member = Member.get(id=identity['uid'], one=True)
    if member is None:
        raise NotFound(msg='会员不存在')
    if not member.is_active:
        raise AuthFailed(msg='您目前处于未激活状态，请联系超级管理员')
    return member


def get_member_tokens(member, verify_remote_addr=False):
    identity['uid'] = member.id
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token


def verify_member_access_token():
    __verify_token('access')


def verify_member_refresh_token():
    __verify_token('refresh')


def __verify_token(request_type):
    from flask import request
    from flask_jwt_extended.config import config
    from flask_jwt_extended.view_decorators import _decode_jwt_from_request as decode
    from flask_jwt_extended.utils import verify_token_claims
    try:
        from flask import _app_ctx_stack as ctx_stack
    except ImportError:
        from flask import _request_ctx_stack as ctx_stack

    if request.method not in config.exempt_methods:
        jwt_data = decode(request_type=request_type)
        ctx_stack.top.jwt = jwt_data
        verify_token_claims(jwt_data)
