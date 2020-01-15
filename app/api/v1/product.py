from lin.redprint import Redprint

from app.libs.utils import paginate
from flask import request, jsonify

from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.product_property import ProductProperty
from app.validators.v1.product_forms import ProductIdAndCount

product_api = Redprint('product')


@product_api.route('/<int:pid>', methods=['GET'])
def get(pid):
    model = Product.get_model(pid, throw=True)
    desc_imgs = ProductImage.get_by_product_id_with_image(pid)
    if desc_imgs:
        model.desc_imgs = desc_imgs
        model._fields.append('desc_imgs')
    properties = ProductProperty.get_by_product_id(pid)
    if properties:
        model.properties = properties
        model._fields.append('properties')
    model.hide('img_id', 'delete_time', 'category_id', 'category')
    return jsonify(model)


@product_api.route('/<int:pid>/for/pre_order', methods=['GET'])
def get_for_pre_order(pid):
    model = Product.get_model_with_img(pid, throw=True)
    model._fields = ['id', 'name', 'image', 'price_str', 'old_price_str']
    return jsonify(model)


@product_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models_with_img(start, count, q, throw=True)
    for model in res['models']:
        model.hide('img_id', 'delete_time', 'category_id')
    return jsonify(res)


@product_api.route('/paginate/by/category/<int:cid>', methods=['GET'])
def get_paginate_by_category(cid):
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models(start, count, q, cid, throw=True)
    for model in res['models']:
        model.hide('img_id', 'delete_time', 'category_id')
    return jsonify(res)


@product_api.route('/paginate/by/theme/<int:tid>', methods=['GET'])
def get_paginate_by_theme(tid):
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models(start, count, q, tid=tid, throw=True)
    for model in res['models']:
        model.hide('img_id', 'delete_time', 'category_id')
    return jsonify(res)


@product_api.route('/recent', methods=['GET'])
def get_recent():
    models = Product.get_recent(20, throw=True)
    for model in models:
        model._fields = ['id', 'image', 'price_str', 'name', 'summary']
    return jsonify(models)


@product_api.route('/stock/check', methods=['POST'])
def check_stock():
    form = ProductIdAndCount().validate_for_api()
    has_stock = Product.check_stock(form.product_id.data, form.count.data)
    return {
        'product_id': form.product_id.data,
        'has_stock': has_stock
    }
