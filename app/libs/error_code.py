from lin.exception import APIException


# 登录相关
class RefreshException(APIException):
    code = 401
    msg = "refresh token 获取失败"
    error_code = 10100


# 会员相关
class GenderStatusException(APIException):
    code = 400
    msg = '会员性别状态错误'
    error_code = 20000


# 微信相关
class WxCodeException(APIException):
    code = 400
    msg = '微信系统繁忙或code码无效'
    error_code = 90000


# 产品相关
class ProductNotFound(APIException):
    code = 404
    msg = '相关产品不存在'


# 订单相关
class OrderNotPay(APIException):
    code = 400
    msg = '订单还未支付'
    error_code = 80000


class OrderNotFound(APIException):
    code = 404
    msg = '订单未找到'
    error_code = 80010


# 地址相关
class AddressNotFound(APIException):
    code = 404
    msg = '收货地址未找到'
    error_code = 70010

