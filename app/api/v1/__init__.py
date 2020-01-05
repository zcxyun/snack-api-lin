"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
from app.api.v1.book import book_api
from app.api.v1.member import member_api
from app.api.v1.product import product_api
from app.api.v1.token import token_api
from app.api.v1.banner import banner_api
from app.api.v1.theme import theme_api
from app.api.v1.category import category_api
from app.api.v1.keyword import keyword_api
from app.api.v1.like import like_api
from app.api.v1.comment import comment_api
from app.api.v1.cart import cart_api
from app.api.v1.address import address_api
from app.api.v1.order import order_api


def create_v1():
    bp_v1 = Blueprint('v1', __name__)
    book_api.register(bp_v1)
    member_api.register(bp_v1)
    product_api.register(bp_v1)
    token_api.register(bp_v1)
    banner_api.register(bp_v1)
    theme_api.register(bp_v1)
    category_api.register(bp_v1)
    keyword_api.register(bp_v1)
    like_api.register(bp_v1)
    comment_api.register(bp_v1)
    cart_api.register(bp_v1)
    address_api.register(bp_v1)
    order_api.register(bp_v1)
    return bp_v1
