from flask import jsonify, request
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.theme import Theme
from app.models.theme_product import ThemeProduct
from app.validators.cms.theme_forms import ThemeRelateProduct, ThemeContent

theme_api = Redprint('theme')


@theme_api.route('/<int:tid>', methods=['GET'])
def get(tid):
    model = Theme.get_model(tid, err_msg='相关主题未添加或已经隐藏')
    return jsonify(model)


@theme_api.route('/all', methods=['GET'])
def get_all():
    models = Theme.get_all_models(err_msg='相关主题不存在')
    for model in models:
        model._fields = ['id', 'name']
    return models


@theme_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Theme.get_paginate_models(start, count, q, soft=False, err_msg='相关主题不存在')
    return jsonify(models)


@theme_api.route('', methods=['POST'])
def create():
    form = ThemeContent().validate_for_api()
    Theme.add_model(form.data, err_msg='主题已经存在或已经隐藏')
    return Success('主题新建成功')


@theme_api.route('/<int:tid>', methods=['PUT'])
def update(tid):
    form = ThemeContent().validate_for_api()
    Theme.edit_model(tid, form.data, err_msg=['相同名字主题已存在', '相关主题不存在或已经隐藏'])
    return Success('主题更新成功')


@theme_api.route('/<int:tid>', methods=['DELETE'])
def delete(tid):
    Theme.remove_model(tid, err_msg='相关主题不存在')
    return Success('主题删除成功')


@theme_api.route('/hide/<int:tid>', methods=['PUT'])
def hide(tid):
    Theme.hide_model(tid, err_msg='相关主题不存在或已经隐藏')
    return Success('主题隐藏成功')


@theme_api.route('/show/<int:tid>', methods=['PUT'])
def show(tid):
    Theme.show_model(tid, err_msg='主题还未隐藏或还未添加')
    return Success('主题显示成功')


@theme_api.route('/product', methods=['POST'])
def create_product():
    form = ThemeRelateProduct().validate_for_api()
    ThemeProduct.new(form.tid.data, form.pid.data, err_msg='主题产品关联已经存在，请不要重复添加')
    return Success(msg='主题加入产品成功')


@theme_api.route('/product', methods=['DELETE'])
def delete_product():
    form = ThemeRelateProduct().validate_for_api()
    ThemeProduct.remove(form.tid.data, form.pid.data, err_msg='此产品不属于此主题或已经删除，不能删除')
    return Success(msg='主题删除产品成功')


@theme_api.route('/product/revert', methods=['PUT'])
def revert_product():
    form = ThemeRelateProduct().validate_for_api()
    ThemeProduct.revert(form.tid.data, form.pid.data, err_msg='此产品还没有删除或未添加此主题, 不能恢复')
