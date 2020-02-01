from lin.forms import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class DeliveryForm(Form):
    member_id = IntegerField(validators=[DataRequired(message='会员ID不能为空'),
                                         NumberRange(min=1, message='会员ID必须大于0')])
    order_id = IntegerField(validators=[DataRequired(message='订单ID不能为空'),
                                        NumberRange(min=1, message='订单ID必须大于0')])
