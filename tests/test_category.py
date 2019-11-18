from pprint import pprint

from app.app import create_app


app = create_app()


def test_get():
    with app.test_client() as c:
        rv = c.get('/cms/category/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_all():
    with app.test_client() as c:
        rv = c.get('/cms/category/all')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_paginate():
    with app.test_client() as c:
        rv = c.get('/cms/category/paginate')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_create():
    with app.test_client() as c:
        rv = c.post('/cms/category', json={
            'name': '蔬菜',
            'description': '蔬菜世界',
            'img_id': 2
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_update():
    with app.test_client() as c:
        rv = c.put('/cms/category/1', json={
            'name': '炒货',
            'description': '炒货天堂',
            'img_id': 3
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_hide():
    with app.test_client() as c:
        rv = c.put('/cms/category/hide/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_show():
    with app.test_client() as c:
        rv = c.put('/cms/category/show/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201

#
# def test_delete():
#     with app.test_client() as c:
#         rv = c.delete('/cms/category/1')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201
