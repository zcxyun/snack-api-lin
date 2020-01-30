from datetime import datetime, timedelta
from decimal import Decimal

from lin import db
from lin.exception import NotFound
from sqlalchemy import Column, Integer, DECIMAL, Date, func

from app.libs.error_code import RepeatStatException, NoDataStatException
from app.models.app_access_log import AppAccessLog
from app.models.member import Member
from .base import Base


class StatAllDaily(Base):
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

    @classmethod
    def get_by_date(cls, date, *, throw=False):
        model = cls.query.filter_by(soft=True, date=date).first()
        if not model:
            if not throw:
                return None
            else:
                raise NotFound(msg=f'{date}统计数据不存在')
        return model

    @classmethod
    def get_between_dates(cls, date_from, date_to, *, throw=False):
        models = cls.query.filter_by(soft=True).filter(
            cls.date >= date_from,
            cls.date <= date_to
        ).all()
        if not models:
            if not throw:
                return []
            else:
                raise NotFound(msg=f'{date_from} - {date_to} 的统计数据不存在')
        return models

    @classmethod
    def get_stat_date_section(cls):
        today = datetime.now().date()
        last_date = db.session.query(func.max(cls.date)).filter_by(soft=True).scalar()
        if last_date is None:
            last_date = db.session.query(func.min(AppAccessLog._create_time)).filter_by(soft=True).scalar()
            if last_date is None:
                last_date = db.session.query(func.min(Member._create_time)).filter_by(soft=True).scalar()
        else:
            if today - last_date == timedelta(days=1):
                raise RepeatStatException()
        if last_date:
            if type(last_date) == datetime:
                last_date = last_date.date()
            date_section = []
            while last_date < today:
                date_section.append(last_date)
                last_date += timedelta(days=1)
            return date_section
        else:
            raise NoDataStatException()
