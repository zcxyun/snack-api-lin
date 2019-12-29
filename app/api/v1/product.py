from lin.redprint import Redprint

from app.libs.utils import paginate
from flask import request, jsonify

from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.product_property import ProductProperty

product_api = Redprint('product')


@product_api.route('/<int:pid>', methods=['GET'])
def get(pid):
    model = Product.get_model(pid, err_msg='相关产品不存在')
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


@product_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models_with_img(start, count, q, err_msg='相关商品不存在')
    for model in res['models']:
        model.hide('img_id', 'delete_time', 'category_id')
    return jsonify(res)


@product_api.route('/paginate/by/category/<int:cid>', methods=['GET'])
def get_paginate_by_category(cid):
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models(start, count, q, cid, err_msg='相关商品不存在')
    for model in res['models']:
        model.hide('img_id', 'delete_time', 'category_id')
    return jsonify(res)


@product_api.route('/paginate/by/theme/<int:tid>', methods=['GET'])
def get_paginate_by_theme(tid):
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models(start, count, q, tid=tid, err_msg='相关商品不存在')
    for model in res['models']:
        model.hide('img_id', 'delete_time', 'category_id')
    return jsonify(res)


@product_api.route('/recent', methods=['GET'])
def get_recent():
    models = Product.get_recent(20, err_msg='相关产品不存在')
    for model in models:
        model._fields = ['id', 'image', 'price_str', 'name', 'summary']
    return jsonify(models)
