from lin.exception import NotFound
from sqlalchemy import Column, Integer

from app.models.base import Base


class OrderProduct(Base):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False, comment='订单id')
    product_id = Column(Integer, nullable=False, comment='商品id')
    count = Column(Integer, nullable=False, comment='商品数量')

    @classmethod
    def get_by_order_id(cls, order_id, soft=True, *, throw=False):
        models = cls.query.filter_by(soft=soft, order_id=order_id).all()
        if not models:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关订单商品关系不存在')
        return models
