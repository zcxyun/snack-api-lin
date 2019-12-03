from lin import db
from lin.exception import NotFound
from pydash import group_by, uniq_by
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, comment='分类名称')
    img_id = Column(Integer, comment='关联图片ID')
    summary = Column(String(100), comment='描述')

    def _set_fields(self):
        self._exclude = ['create_time', 'update_time']

    @classmethod
    def get_all_with_products(cls, soft=True, *, err_msg=None):
        from app.models.product import Product
        res = db.session.query(cls, Product).filter_by(soft=soft).filter(
            cls.id == Product.category_id
        ).order_by(cls.id.desc()).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(res)
        return models

    @classmethod
    def _combine_data(cls, data):
        res = []
        for category, product in data:
            category.products = category.products if hasattr(category, 'products') else []
            category.products.append(product)
            res.append(category)
        res = uniq_by(res, 'id')
        for category in res:
            category._fields.append('products')
        return res
