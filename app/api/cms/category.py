from flask import jsonify, request
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.category import Category
from app.validators.cms.category_forms import CategoryContent

category_api = Redprint('category')


@category_api.route('/<int:cid>', methods=['GET'])
def get(cid):
    model = Category.get_model_with_img(cid, err_msg='相关产品种类未添加或已隐藏')
    return jsonify(model)


@category_api.route('/all', methods=['GET'])
def get_all():
    models = Category.get_all_models_with_img(err_msg='相关分类不存在')
    for model in models:
        model._fields = ['id', 'name']
    return models


@category_api.route('/all/products', methods=['GET'])
def get_all_with_products():
    models = Category.get_all_with_products(err_msg='相关种类和产品不存在')
    # res = []
    # for model in models:
    #     cate_res = {'label': model.name, 'value': model.id}
    #     res.append(cate_res)
    #     if getattr(model, 'products'):
    #         cate_res.setdefault('children', [])
    #         for product in model.products:
    #             cate_res['children'].append({'label': product.name, 'value': product.id})
    return models


@category_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Category.get_paginate_models_with_img(start, count, q, soft=False, err_msg='相关产品种类不存在')
    return jsonify(models)


@category_api.route('', methods=['POST'])
def create():
    form = CategoryContent().validate_for_api()
    Category.add_model(form.data, err_msg='相同名字种类已存在')
    return Success(msg='种类添加成功')


@category_api.route('/<int:cid>', methods=['PUT'])
def update(cid):
    form = CategoryContent().validate_for_api()
    Category.edit_model(cid, form.data, err_msg=['相同名字种类已存在', '相关种类不存在或已隐藏'])
    return Success(msg='种类更新成功')


@category_api.route('/<int:cid>', methods=['DELETE'])
def delete(cid):
    Category.remove_model(cid, err_msg='相关种类不存在')
    return Success(msg='种类删除成功')


@category_api.route('/hide/<int:cid>', methods=['PUT'])
def hide(cid):
    Category.hide_model(cid, err_msg='相关种类未添加或已隐藏')
    return Success(msg='种类隐藏成功')


@category_api.route('/show/<int:cid>', methods=['PUT'])
def show(cid):
    Category.show_model(cid, err_msg='相关种类未添加或已显示')
    return Success(msg='种类显示成功')
