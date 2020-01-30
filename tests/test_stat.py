from datetime import date
from pprint import pprint

from app.app import create_app

app = create_app(environment='development')


def test_stat_all():
    with app.test_client() as c:
        rv = c.get('/cms/stat/date/section')
        stat_date_section = rv.get_json()
        pprint(stat_date_section)
        assert rv.status_code == 200
        assert stat_date_section is not None, '还没有人访问或注册过, 不需要统计'
        for one_date in stat_date_section:
            rv = c.post('/cms/stat', json={
                'date_str': one_date
            })
            res = rv.get_json()
            pprint(res)
            assert rv.status_code == 201


def test_dashboard():
    with app.test_client() as c:
        rv = c.get('/cms/stat/dashboard')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200

