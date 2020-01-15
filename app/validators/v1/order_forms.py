from flask import request
from lin.exception import ParameterException
from lin.forms import Form
from wtforms import Form as WTForm, IntegerField
from wtforms.validators import DataRequired, NumberRange, AnyOf


class OneProductOfOrder(WTForm):
    product_id = IntegerField(validators=[DataRequired(message='商品ID不能为空'),
                                          NumberRange(min=1, message='商品ID必须大于0')])
    count = IntegerField(validators=[DataRequired(message='商品数量不能为空'),
                                     NumberRange(min=1, message='商品数量必须大于0')])


def validate_place_order():
    products = request.get_json()
    if products and type(products) == list:
        for product in products:
            cc = OneProductOfOrder(data=product)
            valid = cc.validate()
            if not valid:
                raise ParameterException(msg=cc.errors)
        return products


class OrderStatusForm(Form):
    order_status = IntegerField(validators=[AnyOf([-1, 0, 1, 2, 3], message='订单状态不正确')])
