from lin import db
from lin.core import File
from lin.exception import NotFound, ParameterException
from sqlalchemy import Column, Integer, SmallInteger

from app.libs.enum import BannerItemType
from app.models.banner import Banner
from app.models.base import Base
from app.models.product import Product
from app.models.theme import Theme


class BannerItem(Base):
    id = Column(Integer, primary_key=True)
    img_id = Column(Integer, nullable=False, comment='关联图片ID')
    content_id = Column(Integer, comment='导向内容表ID，根据不同的type导向不同的表')
    type = Column(
        SmallInteger, default=1,
        comment='跳转类型: 可能导向商品，可能导向专题，可能导向其他 1 无导向 2 导向商品 3 导向专题')
    banner_id = Column(Integer, nullable=False, comment='banner表ID')

    def _set_fields(self):
        self._fields = ['id', 'content_id', 'type', 'type_desc', 'banner_id', 'img_id', 'delete_time']

    @property
    def type_desc(self):
        desc = self.get_all_type_desc()
        return desc[self.type]

    @classmethod
    def get_all_type_desc(cls):
        desc = {
            1: '无导向',
            2: '导向商品',
            3: '导向专题'
        }
        return desc

    @classmethod
    def get_by_banner_id(cls, bid, soft=True, *, err_msg=None):
        res = db.session.query(cls, File.path).filter_by(soft=soft).filter(
            cls.banner_id == bid,
            cls.img_id == File.id
        ).order_by(cls.id.desc()).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        model = cls._add_img_to_models(res)
        return model

    @classmethod
    def get_paginate_models(cls, start, count, q=None, type=0, soft=True, *, err_msg=None):
        type_enum = cls.validate_banner_item_type(type)
        if q:
            q = '%{}%'.format(q)
        if type_enum == BannerItemType.UNKNOWN:
            statement = db.session.query(cls, Banner, File).filter(
                cls.banner_id == Banner.id,
                cls.img_id == File.id
            )
        elif type_enum == BannerItemType.PRODUCT:
            statement = db.session.query(cls, Product, Banner, File).filter(
                cls.content_id == Product.id,
                cls.banner_id == Banner.id,
                cls.img_id == File.id
            )
            if q:
                statement = statement.filter(Product.name.ilike(q))
        elif type_enum == BannerItemType.THEME:
            statement = db.session.query(cls, Theme, Banner, File).filter(
                cls.content_id == Theme.id,
                cls.banner_id == Banner.id,
                cls.img_id == File.id
            )
            if q:
                statement = statement.filter(Theme.name.ilike(q))
        else:
            return {}
        statement = statement.filter_by(soft=soft, type=type)
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if err_msg is None:
                return {}
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(type_enum, res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def _combine_data(cls, type_enum, data):
        res = []
        for item in data:
            if type_enum == BannerItemType.UNKNOWN:
                model = cls._combine_unknown_single_data(*item)
            elif type_enum == BannerItemType.PRODUCT:
                model = cls._combine_product_single_data(*item)
            elif type_enum == BannerItemType.THEME:
                model = cls._combine_theme_single_data(*item)
            res.append(model)
        return res

    @classmethod
    def _combine_unknown_single_data(cls, model, banner, file):
        model.banner = banner.name
        model.image = cls.get_file_url(file.path)
        model._fields.extend(['banner', 'image'])
        return model

    @classmethod
    def _combine_product_single_data(cls, model, product, banner, file):
        model.content = product.name
        model.banner = banner.name
        model.image = cls.get_file_url(file.path)
        model._fields.extend(['content', 'banner', 'image'])
        return model

    @classmethod
    def _combine_theme_single_data(cls, model, theme, banner, file):
        model.content = theme.name
        model.banner = banner.name
        model.image = cls.get_file_url(file.path)
        model._fields.extend(['content', 'banner', 'image'])
        return model

    @classmethod
    def validate_banner_item_type(cls, type):
        try:
            res = BannerItemType(int(type))
            return res
        except ValueError:
            raise ParameterException(msg='导向类型不正确')

    @classmethod
    def add_model(cls, data, commit=True, *, err_msg=None):
        model = cls.query.filter_by(**data).first()
        if model:
            if err_msg is None:
                return False
            else:
                raise ParameterException(msg=err_msg)
        cls.create(**data, commit=True)
        return True

    @classmethod
    def edit_model(cls, id, data, commit=True, *, err_msg=None):
        model = cls.query.filter_by(id=id, soft=True).first()
        if not model:
            if err_msg is None:
                return False
            else:
                raise NotFound(msg=err_msg)
        model.update(**data, commit=True)
        return True
