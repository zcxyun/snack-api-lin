from lin import db
from lin.core import File
from lin.exception import NotFound
from pydash import uniq_by
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import aliased

from app.models.base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, comment='分类名称')
    img_id = Column(Integer, comment='关联图片ID')
    mini_img_id = Column(Integer, comment='关联小图片ID')
    summary = Column(String(100), comment='描述')

    def _set_fields(self):
        self._exclude = ['create_time', 'update_time']

    @classmethod
    def get_all_with_mini_img(cls, soft=True, *, throw=False):
        res = db.session.query(cls, File.path).filter_by(soft=soft).filter(
            cls.mini_img_id == File.id
        ).all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关种类不存在')
        models = cls._combine_data_for_get_all_with_mini_img(res)
        return models

    @classmethod
    def _combine_data_for_get_all_with_mini_img(cls, data):
        models = []
        for item in data:
            category, mini_path = item
            category.mini_image = cls.get_file_url(mini_path)
            category._fields.append('mini_image')
            models.append(category)
        return models

    @classmethod
    def get_pagiante(cls, start, count, q=None, soft=True, *, throw=False):
        Image = aliased(File)
        MiniImage = aliased(File)
        statement = db.session.query(cls, Image.path, MiniImage.path).join(
            Image, cls.img_id == Image.id,
        ).join(
            MiniImage, cls.mini_img_id == MiniImage.id
        ).filter_by(soft=soft).filter(
        ).order_by(cls.id.desc()).offset(start).limit(count)
        if q:
            q = '%{}%'.format(q)
            statement = statement.filter(cls.name.ilike(q))
        total = statement.count()
        res = statement.all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关种类不存在')
        models = cls._combine_data_for_get_paginate(res)
        return {
            'start': start,
            'count': count,
            'models': models,
            'total': total
        }

    @classmethod
    def _combine_data_for_get_paginate(cls, data):
        models = []
        for item in data:
            model = cls._combine_single_data_for_get_paginate(*item)
            models.append(model)
        return models

    @classmethod
    def _combine_single_data_for_get_paginate(cls, category, path, mini_path):
        category.image = cls.get_file_url(path)
        category.mini_image = cls.get_file_url(mini_path)
        category._fields.extend(['image', 'mini_image'])
        return category

    @classmethod
    def get_with_products(cls, cid, count=12, soft=True, *, throw=False):
        from app.models.product import Product
        cate_img = aliased(File)
        prod_img = aliased(File)
        res = db.session.query(cls, Product, cate_img.path, prod_img.path).filter_by(soft=soft).filter(
            cls.id == cid,
            cls.id == Product.category_id,
            cls.img_id == cate_img.id,
            Product.img_id == prod_img.id
        ).offset(0).limit(count).all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关种类不存在')
        model = cls._combine_data(res)[0]
        return model

    @classmethod
    def get_all_with_products(cls, count=12, soft=True, *, throw=False):
        from app.models.product import Product
        cate_img = aliased(File)
        prod_img = aliased(File)
        res = db.session.query(cls, Product, cate_img.path, prod_img.path).filter_by(soft=soft).filter(
            cls.id == Product.category_id,
            cls.img_id == cate_img.id,
            Product.img_id == prod_img.id
        ).order_by(cls.id.desc()).all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关种类和产品不存在')
        models = cls._combine_data(res)
        for model in models:
            model.products = model.products[0:count]
        return models

    @classmethod
    def _combine_data(cls, data):
        res = []
        for category, product, cate_path, prod_path in data:
            category.products = getattr(category, 'products', [])
            product.image = cls.get_file_url(prod_path)
            product._fields.append('image')
            category.products.append(product)
            category.image = cls.get_file_url(cate_path)
            res.append(category)
        res = uniq_by(res, 'id')
        for category in res:
            category._fields.extend(['products', 'image'])
        return res
