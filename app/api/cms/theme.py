from flask import jsonify, request
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.theme import Theme
from app.validators.cms.theme_forms import ThemeContent

theme_api = Redprint('theme')


@theme_api.route('/<int:tid>', methods=['GET'])
def get(tid):
    model = Theme.get_model(tid, throw=True)
    return jsonify(model)


@theme_api.route('/all', methods=['GET'])
def get_all():
    models = Theme.get_all_models(throw=True)
    for model in models:
        model._fields = ['id', 'name']
    return models


@theme_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Theme.get_paginate_models(start, count, q, soft=False, throw=True)
    return jsonify(models)


@theme_api.route('', methods=['POST'])
def create():
    form = ThemeContent().validate_for_api()
    Theme.add_model(form.data, throw=True)
    return Success('主题新建成功')


@theme_api.route('/<int:tid>', methods=['PUT'])
def update(tid):
    form = ThemeContent().validate_for_api()
    Theme.edit_model(tid, form.data, throw=True)
    return Success('主题更新成功')


@theme_api.route('/<int:tid>', methods=['DELETE'])
def delete(tid):
    Theme.remove_model(tid, throw=True)
    return Success('主题删除成功')


@theme_api.route('/hide/<int:tid>', methods=['PUT'])
def hide(tid):
    Theme.hide_model(tid, throw=True)
    return Success('主题隐藏成功')


@theme_api.route('/show/<int:tid>', methods=['PUT'])
def show(tid):
    Theme.show_model(tid, throw=True)
    return Success('主题显示成功')
