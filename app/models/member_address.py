from lin.exception import NotFound
from sqlalchemy import Column, Integer, String, Boolean

from app.models.base import Base


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
        self._exclude = ['create_time', 'update_time', 'delete_time']

    @classmethod
    def get_address(cls, member_id):
        model = cls.query.filter_by(soft=True, member_id=member_id).first()
        return model

    @classmethod
    def edit(cls, member_id, data):
        model = cls.get_address(member_id)
        if not model:
            cls.create(**data, member_id=member_id, commit=True)
            return True
        model.update(**data, commit=True)
        return True

    @classmethod
    def get_by_member_id(cls, member_id):
        model = cls.query.filter_by(soft=True, member_id=member_id).first()
        if not model:
            raise NotFound(msg='请选择收货地址')
        return model
