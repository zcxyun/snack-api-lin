from lin import db
from lin.exception import NotFound
from sqlalchemy import Column, Integer, String, Boolean, or_

from app.models.base import Base
from app.models.member import Member


class MemberAddress(Base):
    id = Column(Integer, primary_key=True)
    userName = Column(String(30), nullable=False, comment='收获人姓名')
    postalCode = Column(String(20), nullable=False, comment='邮编')
    provinceName = Column(String(20), nullable=False, comment='国标收货地址第一级地址')
    cityName = Column(String(20), nullable=False, comment='国标收货地址第二级地址')
    countyName = Column(String(20), nullable=False, comment='国标收货地址第三级地址')
    detailInfo = Column(String(100), nullable=False, comment='详细收货地址信息')
    nationalCode = Column(String(20), nullable=False, comment='收货地址国家码')
    telNumber = Column(String(20), nullable=False, comment='收货人手机号码')
    member_id = Column(Integer, nullable=False, comment='会员ID')

    def _set_fields(self):
        self._exclude = ['_create_time', '_update_time', 'delete_time']

    @classmethod
    def edit(cls, member_id, data):
        model = cls.get_by_member_id(member_id)
        if not model:
            cls.create(**data, member_id=member_id, commit=True)
            return True
        model.update(**data, commit=True)
        return True

    @classmethod
    def get_by_member_id(cls, member_id, *, throw=False):
        model = cls.query.filter_by(soft=True, member_id=member_id).first()
        if not model:
            if not throw:
                return None
            else:
                raise NotFound(msg='请选择收货地址')
        return model

    @classmethod
    def get_paginate_with_member(cls, start, count, q=None, soft=True, *, throw=False):
        statement = db.session.query(cls, Member).filter_by(soft=soft).filter(cls.member_id == Member.id)
        if q:
            q = '%{}%'.format(q)
            where = or_(cls.userName.ilike(q), Member.nickName.ilike(q))
            statement = statement.filter(where)
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关收货地址信息不存在')
        models = cls._combine_data(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def _combine_data(cls, res):
        models = []
        for item in res:
            model = cls._combine_single_data(*item)
            models.append(model)
        return models

    @classmethod
    def _combine_single_data(cls, address, member):
        address.member_avatar = member.avatarUrl
        address.member_name = member.nickName
        address.member_openid = member.openid
        address._fields.extend(['member_avatar', 'member_name', 'member_openid'])
        return address
