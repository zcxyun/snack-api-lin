from enum import Enum


# class GenderEnum(Enum):
#     UNKNOWN = 0
#     MALE = 1
#     FEMALE = 2


class BannerItemType(Enum):
    UNKNOWN = 1
    PRODUCT = 2
    THEME = 3


class MemberActive(Enum):
    INACTIVE = 0
    ACTIVE = 1


class OrderStatus(Enum):
    UNPAID = 0
    UNDELIVERED = 1
    UNRECEIPTED = 2
    DONE = 3
    CANCEL = -1
    # PAID_BUT_INSUFFICIENT_STOCK = -2


# class LoginMethod(Enum):
#     WECHAT = 1
#     ALIPAY = 2
#     MOBILE = 3
#     SMS = 4
