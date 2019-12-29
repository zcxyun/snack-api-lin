from lin.forms import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class KeywordContent(Form):
    key = StringField(validators=[DataRequired(message='搜索关键字不能为空'),
                                  Length(max=8, message='搜索关键字必须小于等于8个字符')])
