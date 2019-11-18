from pprint import pprint

from app.app import create_app

app = create_app()


def test_get():
    with app.test_client() as c:
        rv = c.get('/cms/product/3')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


# def test_get_by_category():
#     with app.test_client() as c:
#         rv = c.get('/cms/product/category/1')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200


def test_get_paginate():
    with app.test_client() as c:
        rv = c.get('/cms/product/paginate')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_create():
    with app.test_client() as c:
        rv = c.post('/cms/product', json={
            'name': '芹菜2',
            'price_str': '2.21',
            'stock': 0,
            'category_id': 2,
            'summary': '芹菜好吃吗',
            'img_id': 2,
            'theme_id': 3
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


# def test_delete():
#     with app.test_client() as c:
#         rv = c.delete('/cms/product/2')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201


# def test_hide():
#     with app.test_client() as c:
#         rv = c.put('/cms/product/hide/3')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201

#
# def test_show():
#     with app.test_client() as c:
#         rv = c.put('/cms/product/show/3')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201
#
#
def test_update():
    with app.test_client() as c:
        rv = c.put('/cms/product/1', json={
            'name': '芹菜1',
            'price_str': '1.20',
            'stock': 0,
            'category_id': 2,
            'summary': '芹菜好吃吗',
            'img_id': 1,
            'theme_id': 3
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201
