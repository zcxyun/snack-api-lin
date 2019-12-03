import re
from decimal import Decimal

from lin import db
from lin.core import File
from lin.exception import NotFound, ParameterException
from pydash import group_by
from sqlalchemy import Column, Integer, String, DECIMAL

from app.models.base import Base
from app.models.category import Category
from app.models.theme import Theme
from app.models.theme_product import ThemeProduct


class Product(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True, comment='商品名称')
    price = Column(DECIMAL(10, 2), nullable=False, comment='价格')
    stock = Column(Integer, default=0, comment='库存量')
    summary = Column(String(50), comment='摘要')
    category_id = Column(Integer, nullable=False, comment='分类ID')
    img_id = Column(Integer, comment='关联图片ID')

    def _set_fields(self):
        self._fields = ['id', 'name', 'price_str', 'stock', 'summary',
                        'delete_time', 'category_id', 'img_id']

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
        res = db.session.query(cls, Category, File).filter(
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
        statement = db.session.query(cls, Category, File).filter(
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
        res = db.session.query(cls, Category, File).filter(
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
    def get_themes_by_id(cls, pid, soft=True):
        res = db.session.query(Theme).filter(
            cls.id == ThemeProduct.product_id,
            cls.id == pid,
            ThemeProduct.theme_id == Theme.id,
            ThemeProduct.delete_time == None,
            Theme.delete_time == None,
        ).filter_by(soft=soft).all()
        return res

    @classmethod
    def get_themes_by_ids(cls, ids, soft=True):
        res = db.session.query(cls.id, Theme).filter(
            cls.id.in_(ids),
            cls.id == ThemeProduct.product_id,
            ThemeProduct.theme_id == Theme.id,
            ThemeProduct.delete_time == None,
            Theme.delete_time == None,
        ).filter_by(soft=soft).order_by(cls.id.desc()).all()
        res = group_by(res, 'id')
        for k, v in res.items():
            res[k] = [i[1].name for i in v]
        return res

    @classmethod
    def _combine_single_data(cls, model, category, file):
        model.category = category.name
        model.image = cls.get_file_url(file.path)
        model._fields.extend(['category', 'image'])
        return model

    @classmethod
    def _combine_data(cls, data):
        res = []
        for item in data:
            model = cls._combine_single_data(*item)
            res.append(model)
        return res
