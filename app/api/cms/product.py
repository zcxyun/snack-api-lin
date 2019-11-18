from flask import jsonify, request, current_app
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.product import Product
from app.validators.cms.product_forms import ProductContent

product_api = Redprint('product')


@product_api.route('/<int:pid>', methods=['GET'])
def get(pid):
    model = Product.get_model(pid, err_msg='相关产品未添加或已隐藏')
    return jsonify(model)


@product_api.route('/category/<int:cid>', methods=['GET'])
def get_products_by_category(cid):
    start, count = paginate()
    q = request.args.get('q', None)
    models = Product.get_paginate_models(start, count, q, cid, soft=False, err_msg='相关产品不存在')
    return jsonify(models)


@product_api.route('/theme/<int:tid>', methods=['GET'])
def get_products_by_theme(tid):
    start, count = paginate()
    q = request.args.get('q', None)
    models = Product.get_paginate_models(start, count, q, tid=tid, soft=False, err_msg='相关产品不存在')
    return jsonify(models)


@product_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    models = Product.get_paginate_models(start, count, q, soft=False, err_msg='相关产品不存在')
    return jsonify(models)


@product_api.route('/recent', methods=['GET'])
def get_recent():
    models = Product.get_recent(current_app.config.get('RECENT', 15), err_msg='相关产品未添加或已隐藏')
    return jsonify(models)


@product_api.route('', methods=['POST'])
def create():
    form = ProductContent().validate_for_api()
    Product.add_model(form.data, err_msg='相关商品已存在')
    return Success(msg='商品添加成功')


@product_api.route('/<int:pid>', methods=['DELETE'])
def delete(pid):
    Product.remove_model(pid, err_msg='相关商品不存在')
    return Success('商品删除成功')


@product_api.route('/hide/<int:pid>', methods=['PUT'])
def hide(pid):
    Product.hide_model(pid, err_msg='相关商品未添加或已隐藏')
    return Success('商品隐藏成功')


@product_api.route('/show/<int:pid>', methods=['PUT'])
def show(pid):
    Product.show_model(pid, err_msg='相关商品未添加或已显示')
    return Success('商品显示成功')


@product_api.route('/<int:pid>', methods=['PUT'])
def update(pid):
    form = ProductContent().validate_for_api()
    Product.edit_model(pid, form.data, err_msg=['相同名字商品已存在', '相关商品不存在或已隐藏'])
    return Success('商品更新成功')
