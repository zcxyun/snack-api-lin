from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class CommentContent(Form):
    product_id = IntegerField(validators=[DataRequired(message='点赞商品id不能为空'),
                                          NumberRange(min=1, message='点赞商品id必须大于0')])
    content = StringField(validators=[DataRequired(message='评论内容不能为空'),
                                      Length(max=20, message='评论内容最多20个字符')])
