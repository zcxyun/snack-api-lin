from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class CategoryContent(Form):
    name = StringField(validators=[DataRequired(message='种类名不能为空')])
    img_id = IntegerField(validators=[DataRequired(message='图片ID不能为空'),
                                      NumberRange(min=1, message='图片ID必须大于0')])
    mini_img_id = IntegerField(validators=[DataRequired(message='小图片ID不能为空'),
                                      NumberRange(min=1, message='小图片ID必须大于0')])
    summary = StringField(validators=[DataRequired(message='种类描述不能为空')])
