from datetime import datetime, timedelta

from lin import db
from lin.exception import NotFound
from sqlalchemy import func

from app.libs.error_code import RepeatStatException, NoDataStatException
from app.models.app_access_log import AppAccessLog
from app.models.member import Member
from .base import Base


class StatBase(Base):
    __abstract__ = True

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
            last_date += timedelta(days=1)
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
