from pprint import pprint

from app.app import create_app


app = create_app()


# def test_like():
#     with app.test_client() as c:
#         rv = c.put('/v1/like/product/1')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201
#
#
# def test_unlike():
#     with app.test_client() as c:
#         rv = c.put('/v1/like/cancel/product/1')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201
#
#
# def test_get_like_info():
#     with app.test_client() as c:
#         rv = c.get('/v1/like/info/product/1')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200


def test_get_like_products():
    with app.test_client() as c:
        rv = c.get('/v1/like/products')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200
