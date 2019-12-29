from pprint import pprint

from app.app import create_app


app = create_app()


def test_create_cart_all():
    with app.test_client() as c:
        rv = c.post('/v1/cart/all', json=[{
            'product_id': 1,
            'count': 9,
            'selected': False
        }, {
            'product_id': 2,
            'count': 2,
            'selected': True
        }, {
            'product_id': 3,
            'count': 3,
            'selected': True
        }, {
            'product_id': 4,
            'count': 1,
            'selected': True
        }])
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_get_products():
    with app.test_client() as c:
        rv = c.get('/v1/cart/products')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


# def test_get_total_count():
#     with app.test_client() as c:
#         rv = c.get('/v1/cart/products/count')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200


# def test_create_cart():
#     with app.test_client() as c:
#         rv = c.post('/v1/cart', json={
#             'product_id': 1,
#             'count': 4,
#             'selected': True
#         })
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201



