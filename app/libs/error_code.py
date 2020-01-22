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


# 产品相关
class ProductUnderStock(APIException):
    code = 400
    error_code = 30000
    msg = '相关商品库存不足'


# 订单相关
class OrderNotPay(APIException):
    code = 400
    error_code = 8000
    msg = '还没付款呢，想干嘛？或者你已经更新过订单了，不要再刷了'


# 微信相关
class WxCodeException(APIException):
    code = 400
    msg = '微信系统繁忙或code码无效'
    error_code = 90000


class WxAccessTokenException(APIException):
    code = 500
    error_code = 9001
    msg = '获取微信AccessToken异常'


class WxTplMsgException(APIException):
    code = 500
    error_code = 9002
    msg = '模板消息发送失败'


class WxPayException(APIException):
    code = 500
    error_code = 9003
    msg = '获取微信支付信息失败'


