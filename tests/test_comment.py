from pprint import pprint

from app.app import create_app


app = create_app(environment='development')


def test_get_comment_of_product():
    with app.test_client() as c:
        rv = c.get('/v1/comment/product/1')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_create_comment():
    with app.test_client() as c:
        rv = c.post('/v1/comment', json={
            'product_id': 1,
            'content': '生命苦短, 我用python'
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201
