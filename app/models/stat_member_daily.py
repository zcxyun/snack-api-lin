from sqlalchemy import Column, Integer, DECIMAL, Date

from .base import Base


class StatMemberDaily(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, comment='统计日期')
    member_id = Column(Integer, nullable=False, comment='会员ID')
    total_pay = Column(DECIMAL(10, 2), nullable=False, comment='总计付款')
    total_buy_count = Column(Integer, nullable=False, comment='总购买数量')
