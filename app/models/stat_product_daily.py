from sqlalchemy import Column, Integer, DECIMAL, Date

from .base import Base


class StatProductDaily(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, comment='统计日期')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    total_price = Column(DECIMAL(10, 2), nullable=False, comment='单日销售总价')
    total_count = Column(Integer, nullable=False, comment='单日销售总数')
