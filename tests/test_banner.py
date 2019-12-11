from pprint import pprint

from app.app import create_app

app = create_app()


def test_get_banner():
    with app.test_client() as c:
        rv = c.get('/cms/banner/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_with_banner_item():
    with app.test_client() as c:
        rv = c.get('/v1/banner/5/banner-item')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_paginate_banner():
    with app.test_client() as c:
        rv = c.get('/cms/banner/paginate')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_create_banner():
    with app.test_client() as c:
        rv = c.post('/cms/banner', json={
            'name': '首页置顶',
            'summary': '首页轮播图'
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_update_banner():
    with app.test_client() as c:
        rv = c.put('/cms/banner/2', json={
            'name': '首页置',
            'summary': '首页轮播图'
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_hide_banner():
    with app.test_client() as c:
        rv = c.put('/cms/banner/hide/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_show_banner():
    with app.test_client() as c:
        rv = c.put('/cms/banner/show/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_delete_banner():
    with app.test_client() as c:
        rv = c.delete('/cms/banner/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201
