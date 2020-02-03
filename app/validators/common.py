from datetime import datetime

from lin.forms import Form
from wtforms import ValidationError, DateTimeField
from wtforms.validators import StopValidation


class DatetimeSection(Form):
    date_start = DateTimeField()
    date_end = DateTimeField()

    def validate_date_start(self, value):
        if value.data is None:
            raise StopValidation()
        try:
            date_start = datetime.strptime(value.data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValidationError('开始日期格式不正确')
        value.data = date_start

    def validate_date_end(self, value):
        if value.data is None:
            raise StopValidation()
        try:
            date_end = datetime.strptime(value.data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValidationError('结束日期格式不正确')
        value.data = date_end
