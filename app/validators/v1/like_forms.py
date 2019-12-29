from lin.forms import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


# class LikeContent(Form):
#     product_id = IntegerField(validators=[DataRequired(message='点赞商品id不能为空'),
#                                           NumberRange(min=1, message='点赞商品id必须大于0')])
#     member_id = IntegerField(validators=[DataRequired(message='点赞会员id不能为空'),
#                                          NumberRange(min=1, message='点赞会员id必须大于0')])
