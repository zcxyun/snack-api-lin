from flask import jsonify, request, current_app
from lin import db
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.product import Product
from app.models.product_property import ProductProperty
from app.models.theme_product import ThemeProduct
from app.validators.cms.product_forms import ProductContent, validate_product_props

product_api = Redprint('product')


@product_api.route('/<int:pid>', methods=['GET'])
def get(pid):
    model = Product.get_model(pid, err_msg='相关产品未添加或已隐藏')
    product_propertes = ProductProperty.get_by_product_id(model.id)
    product_themes = Product.get_themes_by_id(model.id)
    if product_propertes:
        model.params = product_propertes
        model._fields.append('params')
    if product_themes:
        model.theme_ids = [item.id for item in product_themes]
        model._fields.append('theme_ids')
    return jsonify(model)


@product_api.route('/category/<int:cid>', methods=['GET'])
def get_products_by_category(cid):
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models(start, count, q, cid, soft=False, err_msg='相关产品不存在')
    products_with_themes(res['models'])
    return jsonify(res)


@product_api.route('/theme/<int:tid>', methods=['GET'])
def get_products_by_theme(tid):
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models(start, count, q, tid=tid, soft=False, err_msg='相关产品不存在')
    products_with_themes(res['models'])
    return jsonify(res)


@product_api.route('/paginate', methods=['GET'])
def get_paginate():
    start, count = paginate()
    q = request.args.get('q', None)
    res = Product.get_paginate_models(start, count, q, soft=False, err_msg='相关产品不存在')
    products_with_themes(res['models'])
    return jsonify(res)


def products_with_themes(products):
    ids = [item.id for item in products]
    themes = Product.get_themes_by_ids(ids)
    for model in products:
        model.themes = themes.get(model.id, [])
        model._fields.append('themes')


@product_api.route('/recent', methods=['GET'])
def get_recent():
    models = Product.get_recent(current_app.config.get('RECENT', 15), err_msg='相关产品未添加或已隐藏')
    return jsonify(models)


@product_api.route('', methods=['POST'])
def create():
    form = ProductContent().validate_for_api()
    props = validate_product_props()
    with db.auto_commit():
        product = Product.add_model(form.data, commit=False, err_msg='相关商品已存在')
        db.session.flush()
        if props:
            for prop in props:
                ProductProperty.create(**prop, product_id=product.id)
        if form.theme_ids:
            ThemeProduct.add_themes(form.theme_ids.data, product.id)
    return Success(msg='商品添加成功')


@product_api.route('/<int:pid>', methods=['PUT'])
def update(pid):
    form = ProductContent().validate_for_api()
    props = validate_product_props()
    with db.auto_commit():
        Product.edit_model(pid, form.data, commit=False, err_msg=['相同名字商品已存在', '相关商品不存在或已隐藏'])
        if props:
            ProductProperty.edit_properties(pid, props)
        if form.theme_ids:
            ThemeProduct.edit_themes(form.theme_ids.data, pid)
    return Success('商品更新成功')


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

