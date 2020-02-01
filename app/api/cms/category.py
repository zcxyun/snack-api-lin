from flask import jsonify, request
from lin import route_meta, group_required
from lin.core import File
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.category import Category
from app.validators.cms.category_forms import CategoryContent

category_api = Redprint('category')


@category_api.route('/<int:cid>', methods=['GET'])
@route_meta(auth='查询指定分类', module='分类')
@group_required
def get(cid):
    model = Category.get_model_with_img(cid, throw=True)
    mini_image = File.get(one=True, id=model.mini_img_id)
    if mini_image:
        model.mini_image = Category.get_file_url(mini_image.path)
        model._fields.append('mini_image')
    return jsonify(model)


@category_api.route('/all', methods=['GET'])
@route_meta(auth='查询所有分类', module='分类')
@group_required
def get_all():
    models = Category.get_all_models_with_img(throw=True)
    for model in models:
        model._fields = ['id', 'name']
    return models


@category_api.route('/all/products', methods=['GET'])
@route_meta(auth='查询所有分类及其下商品', module='分类')
@group_required
def get_all_with_products():
    """待用"""
    models = Category.get_all_with_products(throw=True)
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
@route_meta(auth='分页查询所有分类', module='分类')
@group_required
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Category.get_pagiante(start, count, q, soft=False, throw=True)
    return jsonify(models)


@category_api.route('', methods=['POST'])
@route_meta(auth='创建分类', module='分类')
@group_required
def create():
    form = CategoryContent().validate_for_api()
    Category.add_model(form.data, throw=True)
    return Success(msg='种类添加成功')


@category_api.route('/<int:cid>', methods=['PUT'])
@route_meta(auth='修改分类', module='分类')
@group_required
def update(cid):
    form = CategoryContent().validate_for_api()
    Category.edit_model(cid, form.data, throw=True)
    return Success(msg='种类更新成功')


@category_api.route('/<int:cid>', methods=['DELETE'])
@route_meta(auth='删除分类', module='分类')
@group_required
def delete(cid):
    Category.remove_model(cid, throw=True)
    return Success(msg='种类删除成功')


@category_api.route('/hide/<int:cid>', methods=['PUT'])
@route_meta(auth='隐藏分类', module='分类')
@group_required
def hide(cid):
    Category.hide_model(cid, throw=True)
    return Success(msg='种类隐藏成功')


@category_api.route('/show/<int:cid>', methods=['PUT'])
@route_meta(auth='显示分类', module='分类')
@group_required
def show(cid):
    Category.show_model(cid, throw=True)
    return Success(msg='种类显示成功')
