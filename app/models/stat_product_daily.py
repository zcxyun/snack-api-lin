from lin.exception import NotFound
from sqlalchemy import Column, Integer, DECIMAL, Date

from .stat_base import StatBase


class StatProductDaily(StatBase):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, comment='统计日期')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    total_price = Column(DECIMAL(10, 2), nullable=False, comment='单日销售总价')
    total_count = Column(Integer, nullable=False, comment='单日销售总数')

    def _set_fields(self):
        self._fields = ['date', 'product_id', 'total_price_str', 'total_count']

    @property
    def total_price_str(self):
        return str(self.total_price)

    @classmethod
    def get_for_product_by_date_section(cls, product_id, date_from, date_to, *, throw=False):
        models = cls.query.filter_by(soft=True, product_id=product_id).filter(
            cls.date >= date_from,
            cls.date <= date_to
        ).all()
        if not models:
            if not throw:
                return []
            else:
                raise NotFound(msg='统计信息不存在')
        return models
