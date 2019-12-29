from lin.redprint import Redprint

from app.models.keyword import Keyword
from app.validators.v1.keyword_forms import KeywordContent

keyword_api = Redprint('keyword')


@keyword_api.route('/hots', methods=['GET'])
def get_hots():
    hots = Keyword.get_hots()
    hots_keys = [hot.key for hot in hots]
    return hots_keys


@keyword_api.route('', methods=['POST'])
def add_keyword():
    form = KeywordContent().validate_for_api()
    Keyword.add(form.key.data)
    hots = Keyword.get_hots()
    hots_keys = [hot.key for hot in hots]
    return hots_keys
