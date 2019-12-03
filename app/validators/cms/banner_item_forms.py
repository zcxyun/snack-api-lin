from lin.forms import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, AnyOf, NumberRange, Optional


class BannerItemType(Form):
    type = StringField(validators=[AnyOf(['1', '2', '3'], message='横幅子项目导向类型不正确')], default='1')


class BannerItemContent(Form):
    type = IntegerField(validators=[AnyOf([1, 2, 3], message='横幅子项目导向类型不正确')], default=1)
    img_id = IntegerField(validators=[DataRequired(message='横幅图片ID不能为空'),
                                      NumberRange(min=1, message='横幅图片ID必须是正整数')])
    content_id = IntegerField(validators=[NumberRange(min=1, message='横幅导向内容表ID必须大于0'), Optional()])
    banner_id = IntegerField(validators=[DataRequired(message='横幅ID不能为空'),
                                         NumberRange(min=1, message='横幅ID必须是正整数')])
