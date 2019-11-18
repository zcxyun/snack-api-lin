from sqlalchemy import Column, Integer, String

from app.models.base import Base


class ProductProperty(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), default='', comment='详情属性名称')
    detail = Column(String(255), nullable=False, comment='详情属性')
    product_id = Column(Integer, nullable=False, comment='商品id')

    def _set_fields(self):
        self._fields = ['name', 'detail']
