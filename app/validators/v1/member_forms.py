from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, AnyOf


class MemberInfoForm(Form):
    nickName = StringField(default='')
    avatarUrl = StringField(default='')
    gender = IntegerField(default=0)
    country = StringField(default='')
    province = StringField(default='')
    city = StringField(default='')
    language = StringField(default='')


class MemberLoginForm(MemberInfoForm):
    code = StringField(validators=[DataRequired(message='微信code码不能为空')])
