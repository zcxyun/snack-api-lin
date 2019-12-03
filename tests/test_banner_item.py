from pprint import pprint

from app.app import create_app

app = create_app()


def test_get_banner_item():
    with app.test_client() as c:
        rv = c.get('/cms/banner-item/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_paginate_banner_item():
    with app.test_client() as c:
        rv = c.get('/cms/banner-item/paginate?type=2')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_create_banner_item():
    with app.test_client() as c:
        rv = c.post('/cms/banner-item', json={
            'img_id': 1,
            'type': 1,
            'banner_id': 2
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_update_banner_item():
    with app.test_client() as c:
        rv = c.put('/cms/banner-item/1', json={
            'img_id': 2,
            'content_id': 1,
            'type': 2,
            'banner_id': 2
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_hide_banner_item():
    with app.test_client() as c:
        rv = c.put('/cms/banner-item/hide/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_show_banner_item():
    with app.test_client() as c:
        rv = c.put('/cms/banner-item/show/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


# def test_delete_banner_item():
#     with app.test_client() as c:
#         rv = c.delete('/cms/banner-item/1')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201
