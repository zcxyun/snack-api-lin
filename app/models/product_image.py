from lin import db
from lin.core import File
from lin.exception import NotFound, ParameterException
from sqlalchemy import Column, Integer

from app.models.base import Base


class ProductImage(Base):
    id = Column(Integer, primary_key=True)
    img_id = Column(Integer, nullable=False, comment='关联图片ID')
    order = Column(Integer, nullable=False, default=0, comment='图片排序序号')
    product_id = Column(Integer, nullable=False, comment='商品id')

    def _set_fields(self):
        self._fields = ['order', 'img_id']

    @classmethod
    def get_by_product_id(cls, product_id, soft=True, *, err_msg=None):
        res = cls.query.filter_by(soft=soft, product_id=product_id).order_by(cls.order.asc()).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        return res

    @classmethod
    def get_by_product_id_with_image(cls, product_id, soft=True, *, throw=False):
        res = db.session.query(cls, File.path).filter_by(soft=soft).filter(
            cls.img_id == File.id,
            cls.product_id == product_id
        )
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关商品详细图片列表不存在')
        models = cls._add_img_to_models(res)
        return models

    @classmethod
    def edit_imgs_for_product(cls, product_id, img_ids):
        if type(img_ids) != list or len(img_ids) == 0:
            raise ParameterException(msg='产品描述图片id列表不能为空')
        models = cls.query.filter_by(product_id=product_id).all()
        if models:
            for model in models:
                model.hard_delete()
        order = 1
        for img_id in img_ids:
            cls.create(
                img_id=img_id,
                order=order,
                product_id=product_id
            )
            order += 1


