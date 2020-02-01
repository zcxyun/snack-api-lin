from datetime import datetime, timedelta

from flask import jsonify
from lin import login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.stat_all_daily import StatAllDaily
from app.services.stat import Stat
from app.validators.cms.stat_forms import DateStrForm

stat_api = Redprint('stat')


@stat_api.route('/date/section', methods=['GET'])
@login_required
def get_last_stat_date():
    stat_date_section = StatAllDaily.get_stat_date_section()
    return jsonify(stat_date_section)


@stat_api.route('', methods=['POST'])
@login_required
def stat_all_for_one_day():
    form = DateStrForm().validate_for_api()
    one_date = datetime.strptime(form.date_str.data, '%Y-%m-%d').date()
    Stat(one_date).stat_all()
    return Success(msg=f'{one_date}统计完成')


@stat_api.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    date_to = datetime.now() - timedelta(days=1)
    date_from = date_to - timedelta(days=30)
    models = StatAllDaily.get_between_dates(date_from.date(), date_to.date(), throw=True)
    return jsonify(models)


# def get_chart_data(categories, series):
#     series_data = [{'name': key, 'data': series[key]} for key in series]
#     return {
#         'categories': categories,
#         'series': series_data
#     }
