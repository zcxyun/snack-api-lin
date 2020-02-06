from datetime import date
from pprint import pprint

from app.app import create_app

app = create_app(environment='development')


def test_stat_all():
    with app.test_client() as c:
        rv = c.get('/cms/stat/date/section/for/all')
        stat_date_section = rv.get_json()
        pprint(stat_date_section)
        assert rv.status_code == 200
        for one_date in stat_date_section:
            rv = c.post('/cms/stat/all', json={
                'date_str': one_date
            })
            res = rv.get_json()
            pprint(res)
            assert rv.status_code == 201


# 暂不测试
# def test_stat_member():
#     with app.test_client() as c:
#         rv = c.get('/cms/stat/date/section/for/member')
#         stat_date_section = rv.get_json()
#         pprint(stat_date_section)
#         assert rv.status_code == 200
#         for one_date in stat_date_section:
#             rv = c.post('/cms/stat/member', json={
#                 'date_str': one_date
#             })
#             res = rv.get_json()
#             pprint(res)
#             assert rv.status_code == 201


def test_stat_product():
    with app.test_client() as c:
        # rv = c.get('/cms/stat/date/section/for/product')
        # stat_date_section = rv.get_json()
        stat_date_section = ['2020-02-05']
        # pprint(stat_date_section)
        # assert rv.status_code == 200
        for one_date in stat_date_section:
            rv = c.post('/cms/stat/product', json={
                'date_str': one_date
            })
            res = rv.get_json()
            pprint(res)
            assert rv.status_code == 201


# def test_dashboard():
#     with app.test_client() as c:
#         rv = c.get('/cms/stat/dashboard')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200


# def test_get_all_stat():
#     with app.test_client() as c:
#         rv = c.get('/cms/stat/all?date_from=2020-1-1&date_to=2020-1-2')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200
#
# 暂不测试
# def test_get_member_stat():
#     with app.test_client() as c:
#         rv = c.get('/cms/stat/member/2?date_from=2020-1-1&date_to=2020-1-2')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200
#
#
# def test_get_product_stat():
#     with app.test_client() as c:
#         rv = c.get('/cms/stat/product/1?date_from=2020-1-1&date_to=2020-1-2')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200
