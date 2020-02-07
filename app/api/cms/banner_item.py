from flask import request, jsonify
from lin import route_meta, group_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.banner_item import BannerItem
from app.validators.cms.banner_item_forms import BannerItemType, BannerItemContent

banner_item_api = Redprint('banner-item')


@banner_item_api.route('/<int:bid>', methods=['GET'])
@route_meta(auth='查询指定横幅子项', module='横幅子项')
@group_required
def get(bid):
    model = BannerItem.get_model_with_img(bid, throw=True)
    return jsonify(model)


@banner_item_api.route('/types', methods=['GET'])
@route_meta(auth='查询横幅子项的所有类型', module='横幅子项')
@group_required
def get_types():
    types = BannerItem.get_all_type_desc()
    res = {k: v for k, v in types.items()}
    return res


@banner_item_api.route('/paginate', methods=['GET'])
@route_meta(auth='分页查询所有横幅子项', module='横幅子项')
@group_required
def get_paginate():
    form = BannerItemType().validate_for_api()
    content_type = int(form.type.data)
    start, count = paginate()
    q = request.args.get('q', None)
    res = BannerItem.get_paginate_models(start, count, q, content_type, soft=False, throw=True)
    for model in res['models']:
        model._fields = ['image', 'banner', 'type_desc', 'content', 'id', 'delete_time']
    return jsonify(res)


@banner_item_api.route('', methods=['POST'])
@route_meta(auth='创建横幅子项', module='横幅子项')
@group_required
def create():
    form = BannerItemContent().validate_for_api()
    BannerItem.add_model(form.data, throw=True)
    return Success(msg='添加横幅成功')


@banner_item_api.route('/<int:bid>', methods=['PUT'])
@route_meta(auth='修改横幅子项', module='横幅子项')
@group_required
def update(bid):
    form = BannerItemContent().validate_for_api()
    BannerItem.edit_model(bid, form.data, throw=True)
    return Success(msg='修改横幅成功')


@banner_item_api.route('/hide/<int:bid>', methods=['PUT'])
@route_meta(auth='隐藏横幅子项', module='横幅子项')
@group_required
def hide(bid):
    BannerItem.hide_model(bid, throw=True)
    return Success(msg='横幅隐藏成功')


@banner_item_api.route('/show/<int:bid>', methods=['PUT'])
@route_meta(auth='显示横幅子项', module='横幅子项')
@group_required
def show(bid):
    BannerItem.show_model(bid, throw=True)
    return Success(msg='横幅显示成功')


@banner_item_api.route('/<int:bid>', methods=['DELETE'])
@route_meta(auth='删除横幅子项', module='横幅子项')
@group_required
def delete(bid):
    BannerItem.remove_model(bid, throw=True)
    return Success(msg='横幅删除成功')
