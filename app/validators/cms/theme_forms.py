from lin.forms import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange


class ThemeRelateProduct(Form):
    tid = IntegerField(validators=[DataRequired(message='主题ID不能为空'),
                                   NumberRange(min=1, message='主题ID必须为正整数')])
    pid = IntegerField(validators=[DataRequired(message='产品ID不能为空'),
                                   NumberRange(min=1, message='产品ID必须为正整数')])


class ThemeContent(Form):
    name = StringField(validators=[DataRequired(message='主题名称不能为空')])
    summary = StringField(validators=[DataRequired(message='主题描述不能为空')])
    topic_img_id = IntegerField(validators=[DataRequired(message='主题主图不能为空'),
                                            NumberRange(min=1, message='主题主图ID必须为正整数')])
    head_img_id = IntegerField(validators=[DataRequired(message='主题页标题图ID不能为空'),
                                           NumberRange(min=1, message='主题主图ID必须为正整数')])
