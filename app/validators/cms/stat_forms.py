from lin.forms import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp


class DateStrForm(Form):
    date_str = StringField(validators=[DataRequired(message='日期字符串不能为空'),
                                       Regexp(r'\d\d\d\d-\d\d-\d\d', message='日期字符串格式不正确')])


class DateStrBetweenForm(Form):
    date_from = StringField(validators=[DataRequired(message='日期字符串不能为空'),
                                       Regexp(r'\d\d\d\d-\d\d-\d\d', message='日期字符串格式不正确')])
    date_to = StringField(validators=[DataRequired(message='日期字符串不能为空'),
                                       Regexp(r'\d\d\d\d-\d\d-\d\d', message='日期字符串格式不正确')])
