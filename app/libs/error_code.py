"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.exception import APIException


class BookNotFound(APIException):
    code = 404  # http状态码
    msg = '没有找到相关图书'  # 异常信息
    error_code = 80010  # 约定的异常码

    
class RefreshException(APIException):
    code = 401
    msg = "refresh token 获取失败"
    error_code = 10100


class GenderStatusException(APIException):
    code = 400
    msg = '会员性别状态错误'
    error_code = 20000


class WxCodeException(APIException):
    code = 400
    msg = '微信系统繁忙或code码无效'
    error_code = 90000
