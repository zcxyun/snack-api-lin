from flask import request, jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.banner_item import BannerItem
from app.validators.cms.banner_item_forms import BannerItemType, BannerItemContent

banner_item_api = Redprint('banner-item')


@banner_item_api.route('/<int:bid>', methods=['GET'])
def get(bid):
    model = BannerItem.get_model_with_img(bid, throw=True)
    return jsonify(model)


@banner_item_api.route('/types', methods=['GET'])
def get_types():
    types = BannerItem.get_all_type_desc()
    res = [{'id': k, 'name': v} for k, v in types.items()]
    return res


@banner_item_api.route('/paginate', methods=['GET'])
def get_paginate():
    form = BannerItemType().validate_for_api()
    content_type = int(form.type.data)
    start, count = paginate()
    q = request.args.get('q', None)
    res = BannerItem.get_paginate_models(start, count, q, content_type, soft=False, throw=True)
    return jsonify(res)


@banner_item_api.route('', methods=['POST'])
def create():
    form = BannerItemContent().validate_for_api()
    BannerItem.add_model(form.data, throw=True)
    return Success(msg='添加横幅成功')


@banner_item_api.route('/<int:bid>', methods=['PUT'])
def update(bid):
    form = BannerItemContent().validate_for_api()
    BannerItem.edit_model(bid, form.data, throw=True)
    return Success(msg='修改横幅成功')


@banner_item_api.route('/hide/<int:bid>', methods=['PUT'])
def hide(bid):
    BannerItem.hide_model(bid, throw=True)
    return Success(msg='横幅隐藏成功')


@banner_item_api.route('/show/<int:bid>', methods=['PUT'])
def show(bid):
    BannerItem.show_model(bid, throw=True)
    return Success(msg='横幅显示成功')


@banner_item_api.route('/<int:bid>', methods=['DELETE'])
def delete(bid):
    BannerItem.remove_model(bid, throw=True)
    return Success(msg='横幅删除成功')
