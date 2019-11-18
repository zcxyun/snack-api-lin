from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp


class ProductContent(Form):
    name = StringField(validators=[DataRequired(message='商品名字不能为空')])
    price_str = StringField(validators=[DataRequired(message='商品价格不能为空'),
                                        Regexp(r'^\d+\.\d{2}$', message='价格格式不正确, 需要保留两位小数')])
    stock = IntegerField(validators=[NumberRange(min=0, message='商品库存必须大于等于0')])
    summary = StringField(validators=[DataRequired(message='商品摘要不能为空'),
                                      Length(max=30, message='摘要长度小于等于30个字符')])
    category_id = IntegerField(validators=[DataRequired(message='分类ID不能为空'),
                                           NumberRange(min=1, message='分类ID必须大于0')])
    theme_id = IntegerField(validators=[DataRequired(message='主题ID不能为空'),
                                           NumberRange(min=1, message='主题ID必须大于0')])
    img_id = IntegerField(validators=[DataRequired(message='商品图片ID不能为空'),
                                           NumberRange(min=1, message='商品图片ID必须大于0')])
