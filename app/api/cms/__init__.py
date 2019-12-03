"""
    register api to admin blueprint
    ~~~~~~~~~
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint


def create_cms():
    cms = Blueprint('cms', __name__)
    from .admin import admin_api
    from .user import user_api
    from .log import log_api
    from .file import file_api
    from .test import test_api
    from .banner import banner_api
    from .banner_item import banner_item_api
    from .theme import theme_api
    from .product import product_api
    from .category import category_api
    from .member import member_api
    admin_api.register(cms)
    user_api.register(cms)
    log_api.register(cms)
    file_api.register(cms)
    test_api.register(cms)
    banner_api.register(cms)
    banner_item_api.register(cms)
    theme_api.register(cms)
    product_api.register(cms)
    category_api.register(cms)
    member_api.register(cms)
    return cms
