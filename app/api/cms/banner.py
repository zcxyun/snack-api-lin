from flask import request, jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.banner import Banner
from app.validators.cms.banner_forms import BannerContent

banner_api = Redprint('banner')


@banner_api.route('/<int:bid>', methods=['GET'])
def get(bid):
    model = Banner.get_model(bid, err_msg='相关横幅未添加或已隐藏')
    return jsonify(model)


@banner_api.route('/all', methods=['GET'])
def get_all():
    models = Banner.get_all_models(err_msg='相关横幅未添加或已隐藏')
    for model in models:
        model._fields = ['id', 'name']
    return jsonify(models)


@banner_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    res = Banner.get_paginate_models(start, count, q, soft=False, err_msg='相关横幅不存在')
    return jsonify(res)


@banner_api.route('', methods=['POST'])
def create():
    form = BannerContent().validate_for_api()
    Banner.add_model(form.data, err_msg='相关横幅已存在或已隐藏')
    return Success(msg='添加横幅成功')


@banner_api.route('/<int:bid>', methods=['PUT'])
def update(bid):
    form = BannerContent().validate_for_api()
    Banner.edit_model(bid, form.data, err_msg=['相关横幅名字已存在', '相关横幅未添加或已隐藏'])
    return Success(msg='修改横幅成功')


@banner_api.route('/hide/<int:bid>', methods=['PUT'])
def hide(bid):
    Banner.hide_model(bid, err_msg='相关横幅未添加或已隐藏')
    return Success(msg='横幅隐藏成功')


@banner_api.route('/show/<int:bid>', methods=['PUT'])
def show(bid):
    Banner.show_model(bid, err_msg='相关横幅未添加或已显示')
    return Success(msg='横幅显示成功')


@banner_api.route('/<int:bid>', methods=['DELETE'])
def delete(bid):
    Banner.remove_model(bid, err_msg='相关横幅未添加或已隐藏')
    return Success(msg='横幅删除成功')
