from flask import jsonify
from lin.redprint import Redprint

from app.models.category import Category

category_api = Redprint('category')


@category_api.route('/<int:cid>', methods=['GET'])
def get(cid):
    model = Category.get_model_with_img(cid, err_msg='相关分类不存在')
    return jsonify(model)


@category_api.route('/<int:cid>/products', methods=['GET'])
def get_with_products(cid):
    model = Category.get_with_products(cid, err_msg='相关种类不存在')
    model._fields = ['id', 'image', 'name', 'products']
    for prod in model.products:
        prod._fields = ['id', 'image', 'name']
    return jsonify(model)


@category_api.route('/all', methods=['GET'])
def get_all():
    models = Category.get_all_models(err_msg='相关分类不存在')
    for model in models:
        model._fields = ['id', 'name']
    return jsonify(models)

