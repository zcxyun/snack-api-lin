from lin.exception import NotFound
from sqlalchemy import Column, Integer, DECIMAL, Date

from .stat_base import StatBase


class StatMemberDaily(StatBase):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, comment='统计日期')
    member_id = Column(Integer, nullable=False, comment='会员ID')
    total_pay = Column(DECIMAL(10, 2), nullable=False, comment='总计付款')
    total_buy_count = Column(Integer, nullable=False, comment='总购买数量')

    # @classmethod
    # def get_for_member_by_date_section(cls, member_id, date_from, date_to, *, throw=False):
    #     models = cls.query.filter_by(soft=True, member_id=member_id).filter(
    #         cls.date >= date_from,
    #         cls.date <= date_to
    #     )
    #     if not models:
    #         if not throw:
    #             return []
    #         else:
    #             raise NotFound(msg='指定会员指定时间内统计信息不存在')
    #     return models
