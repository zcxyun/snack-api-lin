from flask import jsonify
from lin.redprint import Redprint

from app.models.theme import Theme

theme_api = Redprint('theme')


@theme_api.route('/<int:tid>', methods=['GET'])
def get(tid):
    model = Theme.get_model(tid, err_msg='相关主题不存在')
    return jsonify(model)


@theme_api.route('/all', methods=['GET'])
def get_all():
    models = Theme.get_all_models(err_msg='相关主题不存在')
    for model in models:
        model.hide('delete_time', 'head_img_id', 'summary', 'topic_img_id', 'head_img')
    return jsonify(models)


@theme_api.route('/<int:tid>/product', methods=['GET'])
def get_with_products(tid):
    model = Theme.get_with_products(tid, err_msg="相关主题不存在")
    model._fields = ['name', 'head_img', 'products']
    for product in model.products:
        product._fields = ['id', 'image', 'price_str', 'name']
    return jsonify(model)
