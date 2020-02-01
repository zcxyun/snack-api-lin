from flask import jsonify, request
from lin import route_meta, group_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.theme import Theme
from app.validators.cms.theme_forms import ThemeContent

theme_api = Redprint('theme')


@theme_api.route('/<int:tid>', methods=['GET'])
@route_meta(auth='查询指定主题', module='主题')
@group_required
def get(tid):
    model = Theme.get_model(tid, throw=True)
    return jsonify(model)


@theme_api.route('/all', methods=['GET'])
@route_meta(auth='查询所有主题', module='主题')
@group_required
def get_all():
    models = Theme.get_all_models(throw=True)
    for model in models:
        model._fields = ['id', 'name']
    return models


@theme_api.route('/paginate', methods=['GET'])
@route_meta(auth='分页查询所有主题', module='主题')
@group_required
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Theme.get_paginate_models(start, count, q, soft=False, throw=True)
    return jsonify(models)


@theme_api.route('', methods=['POST'])
@route_meta(auth='创建主题', module='主题')
@group_required
def create():
    form = ThemeContent().validate_for_api()
    Theme.add_model(form.data, throw=True)
    return Success('主题新建成功')


@theme_api.route('/<int:tid>', methods=['PUT'])
@route_meta(auth='修改主题', module='主题')
@group_required
def update(tid):
    form = ThemeContent().validate_for_api()
    Theme.edit_model(tid, form.data, throw=True)
    return Success('主题更新成功')


@theme_api.route('/<int:tid>', methods=['DELETE'])
@route_meta(auth='删除主题', module='主题')
@group_required
def delete(tid):
    Theme.remove_model(tid, throw=True)
    return Success('主题删除成功')


@theme_api.route('/hide/<int:tid>', methods=['PUT'])
@route_meta(auth='隐藏主题', module='主题')
@group_required
def hide(tid):
    Theme.hide_model(tid, throw=True)
    return Success('主题隐藏成功')


@theme_api.route('/show/<int:tid>', methods=['PUT'])
@route_meta(auth='显示主题', module='主题')
@group_required
def show(tid):
    Theme.show_model(tid, throw=True)
    return Success('主题显示成功')
