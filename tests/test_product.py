from pprint import pprint

from app.app import create_app

app = create_app()


def test_get():
    with app.test_client() as c:
        # rv = c.get('/cms/product/1')
        rv = c.get('/v1/product/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_recent():
    with app.test_client() as c:
        rv = c.get('/v1/product/recent')
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
            'name': 'a2',
            'price_str': '1.21',
            'stock': 2,
            'category_id': 2,
            'summary': '好吗',
            'img_id': 2,
            'props': [{'detail': 'a2', 'name': '品名'}, {'detail': '优', 'name': '品质'}],
            'theme_ids': [5, 6, 7]
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


def test_hide():
    with app.test_client() as c:
        rv = c.put('/cms/product/hide/3')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_show():
    with app.test_client() as c:
        rv = c.put('/cms/product/show/3')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_update():
    with app.test_client() as c:
        rv = c.put('/cms/product/1', json={
            'name': 'd',
            'price_str': '1.20',
            'stock': 0,
            'category_id': 6,
            'summary': 'd好吃吗',
            'img_id': 1,
            'props': [
                {'detail': 'super', 'name': '品名'},
                {'detail': 'm国', 'name': '产地'},
                {'detail': '10day', 'name': '保质期'}
            ],
            'theme_ids': [1, 5],
            'desc_img_ids': [34, 39, 44, 50, 56, 9, 17, 24, 33, 38, 47, 52, 58]
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201
