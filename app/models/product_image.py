from sqlalchemy import Column, Integer

from app.models.base import Base


class ProductImage(Base):
    id = Column(Integer, primary_key=True)
    img_id = Column(Integer, nullable=False, comment='关联图片ID')
    order = Column(Integer, nullable=False, default=0, comment='图片排序序号')
    product_id = Column(Integer, nullable=False, comment='商品id')

    def _set_fields(self):
        self._fields = ['order']
