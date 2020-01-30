from pprint import pprint

from app.app import create_app


app = create_app(environment='development')


def test_get_hots():
    with app.test_client() as c:
        rv = c.get('/v1/keyword/hots')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_create():
    with app.test_client() as c:
        rv = c.post('/v1/keyword', json={
            'key': 'python'
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201
