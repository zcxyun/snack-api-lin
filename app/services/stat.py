from datetime import datetime
from decimal import Decimal
from random import randint

from lin import db
from sqlalchemy import func

from app.libs.enum import OrderStatus
from app.models.app_access_log import AppAccessLog
from app.models.member import Member
from app.models.order import Order
from app.models.stat_all_daily import StatAllDaily


class Stat:
    """统计某日的数据"""

    def __init__(self, one_date):
        self.one_date = one_date
        self.date_from = datetime.strptime(f'{one_date} 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.date_to = datetime.strptime(f'{one_date} 23:59:59', '%Y-%m-%d %H:%M:%S')

    def stat_all(self):
        price, order_count = self.stat_price_count()
        total_price, total_order_count = self.stat_total_price_count()
        member_count = Member.stat_total_by_date(self.one_date)
        total_member_count = Member.stat_total(self.date_to)
        access = AppAccessLog.stat_total_by_date(self.one_date)
        total_access = AppAccessLog.stat_total(self.date_to)
        # StatAllDaily.create(
        #     date=self.one_date,
        #     price=price,
        #     total_price=total_price,
        #     order_count=order_count,
        #     total_order_count=total_order_count,
        #     member_count=member_count,
        #     total_member_count=total_member_count,
        #     access=access,
        #     total_access=total_access,
        #     commit=True
        # )
        StatAllDaily.create(
            date=self.one_date,
            price=Decimal(f'{randint(1, 999)}.34'),
            total_price=Decimal(f'{randint(1, 9999)}.34'),
            order_count=randint(1, 999),
            total_order_count=randint(1, 9999),
            member_count=randint(1, 999),
            total_member_count=randint(1, 9999),
            access=randint(1, 999),
            total_access=randint(1, 9999),
            commit=True
        )
        return True

    def stat_price_count(self):
        res = db.session.query(
            func.sum(Order.total_price), func.sum(Order.total_count)
        ).filter_by(soft=True).filter(
            Order.order_status != OrderStatus.UNPAID.value,
            Order.order_status != OrderStatus.CANCEL.value,
            Order._create_time >= self.date_from,
            Order._create_time <= self.date_to
        ).first()
        if res[0] is None and res[1] is None:
            return [Decimal('0.00'), 0]
        return res

    def stat_total_price_count(self):
        res = db.session.query(
            func.sum(Order.total_price), func.sum(Order.total_count)
        ).filter_by(soft=True).filter(
            Order.order_status != OrderStatus.UNPAID.value,
            Order.order_status != OrderStatus.CANCEL.value,
            Order._create_time <= self.date_to
        ).first()
        if res[0] is None and res[1] is None:
            return [Decimal('0.00'), 0]
        return res

