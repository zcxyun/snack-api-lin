from flask import request
from lin.exception import ParameterException
from wtforms import Form as WTForm
from lin.forms import Form
from wtforms import IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class CartContent(Form):
    product_id = IntegerField(validators=[DataRequired(message='购物车中商品ID不能为空'),
                                          NumberRange(min=1, message='购物车中商品ID必须大于0')])
    count = IntegerField(validators=[DataRequired(message='购物车中商品数量不能为空'),
                                     NumberRange(min=1, message='购物车中商品数量必须大于0')])
    selected = BooleanField(default=True)


class CartContentOne(WTForm):
    product_id = IntegerField(validators=[DataRequired(message='购物车中商品ID不能为空'),
                                          NumberRange(min=1, message='购物车中商品ID必须大于0')])
    count = IntegerField(validators=[DataRequired(message='购物车中商品数量不能为空'),
                                     NumberRange(min=1, message='购物车中商品数量必须大于0')])
    selected = BooleanField(default=True)


def validate_some_cart_content():
    cart_contents = request.get_json()
    if cart_contents and type(cart_contents) == list:
        for cart_content in cart_contents:
            cc = CartContentOne(data=cart_content)
            valid = cc.validate()
            if not valid:
                raise ParameterException(msg=cc.errors)
        return cart_contents
