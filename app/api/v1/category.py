from flask import jsonify
from lin.redprint import Redprint

from app.models.category import Category

category_api = Redprint('category')


@category_api.route('/<int:cid>', methods=['GET'])
def get(cid):
    model = Category.get_model_with_img(cid, throw=True)
    return jsonify(model)


@category_api.route('/<int:cid>/products', methods=['GET'])
def get_with_products(cid):
    model = Category.get_with_products(cid, throw=True)
    model._fields = ['id', 'image', 'name', 'products']
    for prod in model.products:
        prod._fields = ['id', 'image', 'name']
    return jsonify(model)


@category_api.route('/all', methods=['GET'])
def get_all():
    models = Category.get_all_models(throw=True)
    for model in models:
        model._fields = ['id', 'name']
    return jsonify(models)


@category_api.route('/all/with/mini_img', methods=['GET'])
def get_all_with_mini_img():
    models = Category.get_all_with_mini_img(throw=True)
    for model in models:
        model._fields = ['id', 'name', 'mini_image']
    return jsonify(models)
