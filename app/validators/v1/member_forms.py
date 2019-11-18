from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, AnyOf


class MemberInfoForm(Form):
    nickName = StringField(validators=[DataRequired(message='会员昵称不能为空')])
    avatarUrl = StringField(validators=[DataRequired(message='会员头像不能为空')])
    gender = IntegerField(validators=[DataRequired(message='会员性别不能为空'),
                                      AnyOf([0, 1, 2], message='会员性别只能为 0, 未知 1, 男 2, 女')])
    country = StringField(default='')
    province = StringField(default='')
    city = StringField(default='')


class MemberLoginForm(MemberInfoForm):
    code = StringField(validators=[DataRequired(message='微信code码不能为空')])
