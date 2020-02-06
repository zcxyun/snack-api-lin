from decimal import Decimal

from sqlalchemy import Column, Integer, DECIMAL, Date

from .stat_base import StatBase


class StatAllDaily(StatBase):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, comment='统计日期')
    price = Column(DECIMAL(10, 2), nullable=False, comment='当日应收总金额')
    total_price = Column(DECIMAL(10, 2), nullable=False, comment='截止目前应收总金额')
    order_count = Column(Integer, nullable=False, comment='当日订单总数')
    total_order_count = Column(Integer, nullable=False, comment='截止目前总订单数')
    member_count = Column(Integer, nullable=False, comment='当日会员总数')
    total_member_count = Column(Integer, nullable=False, comment='截止目前会员总数')
    access = Column(Integer, nullable=False, comment='当日访问量')
    total_access = Column(Integer, nullable=False, comment='总访问量')

    def _set_fields(self):
        self._fields = ['date', 'price_str', 'total_price_str', 'order_count', 'total_order_count',
                        'member_count', 'total_member_count', 'access', 'total_access']

    @property
    def price_str(self):
        return str(self.price.quantize(Decimal('0.00')))

    @property
    def total_price_str(self):
        return str(self.total_price.quantize(Decimal('0.00')))
