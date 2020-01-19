from lin.exception import NotFound
from sqlalchemy import Column, String, Integer, SmallInteger

from app.libs.enum import MemberActive
from .base import Base


class Member(Base):
    id = Column(Integer, primary_key=True, comment='会员id')
    openid = Column(String(100), comment='微信用户openid')
    nickName = Column(String(30), nullable=False, comment='会员昵称')
    avatarUrl = Column(String(500), comment='会员头像')
    gender = Column(SmallInteger, default=0, comment='会员性别; 0, 未知 1, 男性 2, 女性')
    country = Column(String(30), comment='会员所在国家')
    province = Column(String(30), comment='会员所在省份')
    city = Column(String(30), comment='会员所在城市')
    language = Column(String(10), comment='显示 country，province，city 所用的语言')
    active = Column(SmallInteger, default=1,
                    comment='当前用户是否为激活状态，非激活状态默认失去用户权限 ; 1 -> 激活 | 0 -> 非激活')

    def _set_fields(self):
        self._fields = ['nickName', 'avatarUrl', 'gender_str', 'country', 'province', 'city', 'gender']

    def is_active(self):
        return self.active == MemberActive.ACTIVE.value

    @property
    def gender_str(self):
        description = {0: '未知', 1: '男性', 2: '女性'}
        return description[self.gender]

    @classmethod
    def get_paginate_models(cls, start, count, q=None, soft=True, *, throw=False):
        """分页查询会员模型(支持搜索)"""
        statement = cls.query.filter_by(soft=soft)
        if q:
            search_key = '%{}%'.format(q)
            statement = statement.filter(cls.nickName.ilike(search_key))
        total = statement.count()
        models = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not models:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关会员不存在')
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }
