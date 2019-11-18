from sqlalchemy import Column, Integer

from app.models.base import Base


class OrderProduct(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False, comment='订单id')
    product_id = Column(Integer, nullable=False, comment='商品id')
    count = Column(Integer, nullable=False, comment='商品数量')
