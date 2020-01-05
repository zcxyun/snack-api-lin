from flask import jsonify
from lin.redprint import Redprint

from app.models.banner_item import BannerItem

banner_api = Redprint('banner')


@banner_api.route('/<int:bid>/banner-item', methods=['GET'])
def get(bid):
    models = BannerItem.get_by_banner_id(bid, throw=True)
    for model in models:
        model.hide('delete_time', 'img_id', 'banner_id')
    return jsonify(models)
