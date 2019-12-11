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
    summary = Column(String(100), comment='描述')

    def _set_fields(self):
        self._exclude = ['create_time', 'update_time']

    @classmethod
    def get_with_products(cls, cid, count=10, soft=True, *, err_msg=None):
        from app.models.product import Product
        cate_img = aliased(File)
        prod_img = aliased(File)
        res = db.session.query(cls, Product, cate_img.path, prod_img.path).filter_by(soft=soft).filter(
            cls.id == cid,
            cls.id == Product.category_id,
            cls.img_id == cate_img.id,
            Product.img_id == prod_img.id
        ).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        model = cls._combine_data(res)[0]
        model.products = model.products[0:count]
        return model

    @classmethod
    def get_all_with_products(cls, count=10, soft=True, *, err_msg=None):
        from app.models.product import Product
        cate_img = aliased(File)
        prod_img = aliased(File)
        res = db.session.query(cls, Product, cate_img.path, prod_img.path).filter_by(soft=soft).filter(
            cls.id == Product.category_id,
            cls.img_id == cate_img.id,
            Product.img_id == prod_img.id
        ).order_by(cls.id.desc()).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
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
