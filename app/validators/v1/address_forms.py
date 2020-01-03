from lin.forms import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class MemberAddressContent(Form):
    userName = StringField(validators=[DataRequired(message='收货人姓名不能为空')])
    postalCode = StringField(validators=[DataRequired(message='邮编不能为空')])
    provinceName = StringField(validators=[DataRequired(message='省份不能为空')])
    cityName = StringField(validators=[DataRequired(message='地市不能为空')])
    countyName = StringField(validators=[DataRequired(message='县区不能为空')])
    detailInfo = StringField(validators=[DataRequired(message='详细收货地址信息不能为空')])
    nationalCode = StringField(validators=[DataRequired(message='收货地址国家码不能为空')])
    telNumber = StringField(validators=[DataRequired(message='收货人手机号码不能为空')])
