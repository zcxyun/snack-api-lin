from flask import jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.models.cart import Cart
from app.validators.v1.cart_forms import CartContent, validate_some_cart_content

cart_api = Redprint('cart')


@cart_api.route('/products', methods=['GET'])
@member_login_required
def get_products():
    member = get_current_member()
    products = Cart.get_products(member.id)
    for product in products:
        product._fields = ['id', 'count', 'image', 'name', 'price_str', 'selected']
    return jsonify(products)


@cart_api.route('/products/count', methods=['GET'])
@member_login_required
def get_total_count():
    member = get_current_member()
    total_count = Cart.get_total_count(member.id)
    return jsonify({'total_count': int(total_count)})


@cart_api.route('', methods=['POST'])
@member_login_required
def create_or_update():
    member = get_current_member()
    form = CartContent().validate_for_api()
    Cart.edit(member.id, form.product_id.data, form.count.data, form.selected.data)
    return Success(msg='加入购物车成功')


@cart_api.route('/all', methods=['POST'])
@member_login_required
def create_or_update_all():
    member = get_current_member()
    cart_contents = validate_some_cart_content()
    Cart.edit_some(member.id, cart_contents)
    return Success(msg='更新购物车成功')


@cart_api.route('', methods=['DELETE'])
@member_login_required
def clear():
    member = get_current_member()
    Cart.clear(member.id)
    return Success(msg='购物车已清空')
