from datetime import datetime, timedelta

from flask import jsonify
from lin import login_required, route_meta, group_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.stat_all_daily import StatAllDaily
from app.models.stat_member_daily import StatMemberDaily
from app.models.stat_product_daily import StatProductDaily
from app.services.stat import Stat
from app.validators.cms.stat_forms import DateStrForm, DateStrBetweenForm

stat_api = Redprint('stat')


@stat_api.route('/date/section/for/all', methods=['GET'])
@login_required
def get_stat_date_section_for_all():
    stat_date_section = StatAllDaily.get_stat_date_section()
    return jsonify(stat_date_section)


@stat_api.route('/all', methods=['POST'])
@login_required
def stat_all_for_one_day():
    one_date = get_one_date()
    Stat(one_date).stat_all()
    return Success(msg=f'{one_date}统计完成')


@stat_api.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    date_to = datetime.now() - timedelta(days=1)
    date_from = date_to - timedelta(days=30)
    models = StatAllDaily.get_between_dates(date_from.date(), date_to.date(), throw=True)
    return jsonify(models)


@stat_api.route('/all', methods=['GET'])
@route_meta(auth='获取指定日期区间的所有统计数据', module='统计')
@group_required
def get_all_by_date_section():
    date_from, date_to = get_date_section()
    models = StatAllDaily.get_between_dates(date_from, date_to, throw=True)
    return jsonify(models)


# @stat_api.route('/date/section/for/member', methods=['GET'])
# @login_required
# def get_stat_date_section_for_member():
#     stat_date_section = StatMemberDaily.get_stat_date_section()
#     return jsonify(stat_date_section)


# @stat_api.route('/member', methods=['POST'])
# def stat_member_for_one_day():
#     one_date = get_one_date()
#     Stat(one_date).stat_member()
#     return Success(msg=f'{one_date}统计完成')


# @stat_api.route('/member/<int:mid>', methods=['GET'])
# def get_member_by_date_section(mid):
#     date_from, date_to = get_date_section()
#     models = StatMemberDaily.get_for_member_by_date_section(mid, date_from, date_to, throw=True)
#     return jsonify(models)


@stat_api.route('/date/section/for/product', methods=['GET'])
@login_required
def get_stat_date_section_for_product():
    stat_date_section = StatProductDaily.get_stat_date_section()
    return jsonify(stat_date_section)


@stat_api.route('/product', methods=['POST'])
@route_meta(auth='统计指定商品指定日期的数据', module='统计')
@group_required
def stat_product_for_one_day():
    one_date = get_one_date()
    Stat(one_date).stat_product()
    return Success(msg=f'{one_date}统计完成')


@stat_api.route('/product/<int:pid>', methods=['GET'])
@route_meta(auth='获取指定商品指定日期区间的统计数据', module='统计')
@group_required
def get_product_by_date_section(pid):
    date_from, date_to = get_date_section()
    models = StatProductDaily.get_for_product_by_date_section(pid, date_from, date_to, throw=True)
    return jsonify(models)


def get_one_date():
    form = DateStrForm().validate_for_api()
    one_date = datetime.strptime(form.date_str.data, '%Y-%m-%d').date()
    return one_date


def get_date_section():
    form = DateStrBetweenForm().validate_for_api()
    date_from = datetime.strptime(form.date_from.data, '%Y-%m-%d').date()
    date_to = datetime.strptime(form.date_to.data, '%Y-%m-%d').date()
    return date_from, date_to
