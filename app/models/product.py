from decimal import Decimal

from lin import db
from lin.core import File
from lin.exception import NotFound, ParameterException
from sqlalchemy import Column, Integer, String, DECIMAL
import re
from app.models.base import Base
from app.models.category import Category
from app.models.product_property import ProductProperty
from app.models.theme import Theme


class Product(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True, comment='商品名称')
    price = Column(DECIMAL(10, 2), nullable=False, comment='价格')
    stock = Column(Integer, default=0, comment='库存量')
    summary = Column(String(50), comment='摘要')
    category_id = Column(Integer, nullable=False, comment='分类ID')
    theme_id = Column(Integer, default=1, comment='主题ID')
    img_id = Column(Integer, comment='关联图片ID')

    def _set_fields(self):
        self._fields = ['id', 'name', 'price_str', 'stock', 'summary',
                        'delete_time', 'category_id', 'theme_id', 'img_id']

    @property
    def price_str(self):
        return str(self.price.quantize(Decimal('0.00'))) if self.price else '0.00'

    @price_str.setter
    def price_str(self, value):
        if type(value) == str and re.findall(r'^\d+\.\d{2}$', value):
            self.price = Decimal(value)
        else:
            raise ParameterException(msg='商品价格格式不正确, 需要保留两位小数')

    @classmethod
    def get_model(cls, id, soft=True, *, err_msg=None):
        res = db.session.query(cls, Category.name, Theme.name, File.path).filter(
            cls.theme_id == Theme.id,
            cls.category_id == Category.id,
            cls.img_id == File.id,
            cls.id == id
        ).filter_by(soft=soft).first()
        if not res:
            if err_msg is None:
                return None
            else:
                raise NotFound(msg=err_msg)
        model = cls._combine_single_data(*res)
        return model

    @classmethod
    def get_paginate_models(cls, start, count, q=None, cid=0, tid=0, soft=True, *, err_msg=None):
        statement = db.session.query(cls, Category.name, Theme.name, File.path).filter(
            cls.theme_id == Theme.id,
            cls.category_id == Category.id,
            cls.img_id == File.id
        ).filter_by(soft=soft)
        if cid:
            statement = statement.filter_by(category_id=cid)
        if tid:
            statement = statement.filter_by(theme_id=tid)
        if q:
            q = '%{}%'.format(q)
            statement = statement.filter(cls.name.ilike(q))
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def get_recent(cls, count, soft=True, *, err_msg=None):
        res = db.session.query(cls, Category.name, Theme.name, File.path).filter(
            cls.theme_id == Theme.id,
            cls.category_id == Category.id,
            cls.img_id == File.id
        ).filter_by(soft=soft).order_by(cls.id.desc()).limit(count).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(res)
        return models

    @classmethod
    def _combine_single_data(cls, model, category, theme, path):
        model.category = category
        model.theme = theme
        model.image = cls.get_file_url(path)
        model._fields.extend(['category', 'theme', 'image'])
        return model

    @classmethod
    def _combine_data(cls, data):
        res = []
        for item in data:
            model = cls._combine_single_data(*item)
            res.append(model)
        return res
