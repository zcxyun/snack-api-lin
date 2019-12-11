from pprint import pprint

from app.app import create_app

app = create_app()


def test_get():
    with app.test_client() as c:
        rv = c.get('/cms/theme/3')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_all():
    with app.test_client() as c:
        # rv = c.get('/cms/theme/all')
        rv = c.get('/v1/theme/all')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_paginate():
    with app.test_client() as c:
        rv = c.get('/cms/theme/paginate')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_with_products():
    with app.test_client() as c:
        rv = c.get('/v1/theme/5/product')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_create():
    with app.test_client() as c:
        rv = c.post('/cms/theme', json={
            'name': '炒货天堂',
            'summary': '炒货无敌',
            'topic_img_id': 2,
            'head_img_id': 2
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_update():
    with app.test_client() as c:
        rv = c.put('/cms/theme/2', json={
            'name': '水果世界',
            'summary': '美味水果世界',
            'topic_img_id': 1,
            'head_img_id': 1
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_hide():
    with app.test_client() as c:
        rv = c.put('/cms/theme/hide/2')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_show():
    with app.test_client() as c:
        rv = c.put('/cms/theme/show/2')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


# def test_delete():
#     with app.test_client() as c:
#         rv = c.delete('/cms/theme/2')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201
