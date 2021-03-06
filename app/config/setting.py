"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta


class BaseConfig(object):
    """
    基础配置
    """
    # 分页配置
    COUNT_DEFAULT = 10
    PAGE_DEFAULT = 0
    PAY_COUNTDOWN = 1800     # 单位秒

    # 屏蔽 sql alchemy 的 FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """
    开发环境普通配置
    """
    DEBUG = True
    SITE_DOMAIN = 'http://localhost:5000'

    # 令牌配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # 插件模块暂时没有开启，以下配置可忽略
    # plugin config写在字典里面
    PLUGIN_PATH = {
        'poem': {'path': 'app.plugins.poem', 'enable': True, 'version': '0.0.1', 'limit': 20},
        'oss': {'path': 'app.plugins.oss', 'enable': True, 'version': '0.0.1', 'access_key_id': 'not complete',
                'access_key_secret': 'not complete', 'endpoint': 'http://oss-cn-shenzhen.aliyuncs.com',
                'bucket_name': 'not complete', 'upload_folder': 'app',
                'allowed_extensions': ['jpg', 'gif', 'png', 'bmp']}
    }


class ProductionConfig(BaseConfig):
    """
    生产环境普通配置
    """
    DEBUG = False
    SITE_DOMAIN = "https://7yue.site"

    # 令牌配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # 插件模块暂时没有开启，以下配置可忽略
    # plugin config写在字典里面
    PLUGIN_PATH = {
        'poem': {'path': 'app.plugins.poem', 'enable': True, 'version': '0.0.1', 'limit': 20},
        'oss': {'path': 'app.plugins.oss', 'enable': True, 'version': '0.0.1', 'access_key_id': 'not complete',
                'access_key_secret': 'not complete', 'endpoint': 'http://oss-cn-shenzhen.aliyuncs.com',
                'bucket_name': 'not complete', 'upload_folder': 'app',
                'allowed_extensions': ['jpg', 'gif', 'png', 'bmp']}
    }
