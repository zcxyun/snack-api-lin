from lin.forms import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class ProductIdAndCount(Form):
    product_id = IntegerField(validators=[DataRequired(message='商品ID不能为空'),
                                          NumberRange(min=1, message='商品ID必须大于0')])
    count = IntegerField(validators=[DataRequired(message='商品数量不能为空'),
                                     NumberRange(min=1, message='商品数量必须大于0')])
