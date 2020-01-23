from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Keyword(Base):
    id = Column(Integer, primary_key=True)
    key = Column(String(20), nullable=False, unique=True, comment='搜索关键字')
    count = Column(Integer, default=1, comment='搜索关键字次数')

    @classmethod
    def get_hots(cls, count=8):
        """搜索热门关键字"""
        hots = cls.query.filter_by(soft=True).order_by(cls.count.desc()).limit(count).all()
        return hots

    @classmethod
    def add(cls, key):
        model = cls.query.filter_by(key=key, soft=True).first()
        if not model:
            cls.create(key=key, commit=True)
            return True
        count = model.count + 1     # 搜索次数加1
        model.update(count=count, commit=True)
        return True
