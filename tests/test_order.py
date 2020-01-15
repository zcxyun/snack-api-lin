from pprint import pprint

from app.app import create_app


app = create_app()


# def test_place_order():
#     with app.test_client() as c:
#         rv = c.post('/v1/order/place', json=[{
#             'product_id': 1,
#             'count': 1,
#         }, {
#             'product_id': 2,
#             'count': 2,
#         }, {
#             'product_id': 3,
#             'count': 3,
#         }, {
#             'product_id': 4,
#             'count': 4,
#         }])
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201


# def test_cancel_order():
#     with app.test_client() as c:
#         rv = c.post('/v1/order/1/cancel')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201
#
#
# def test_comfirm_order():
#     with app.test_client() as c:
#         rv = c.post('/v1/order/1/confirm')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 201

# def test_get_paginate():
#     with app.test_client() as c:
#         rv = c.get('/v1/order/paginate?start=0&count=10')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200
#
#
# def test_get_paginate_by_status():
#     with app.test_client() as c:
#         rv = c.get('/v1/order/paginate/status/0?start=0&count=10')
#         json_data = rv.get_json()
#         pprint(json_data)
#         assert rv.status_code == 200
