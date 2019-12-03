from lin.forms import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class BannerContent(Form):
    name = StringField(validators=[DataRequired(message='横幅名字不能为空')])
    summary = StringField(validators=[DataRequired(message='横幅摘要不能为空')])
