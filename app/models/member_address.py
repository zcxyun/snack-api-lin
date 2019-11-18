from sqlalchemy import Column, Integer, String, Boolean

from app.models.base import Base


class MemberAddress(Base):
    id = Column(Integer, primary_key=True)
    userName = Column(String(30), nullable=False, comment='收获人姓名')
    nationalCode = Column(String(20), comment='收货地址国家码')
    provinceName = Column(String(20), nullable=False, comment='国标收货地址第一级地址')
    cityName = Column(String(20), nullable=False, comment='国标收货地址第二级地址')
    countyName = Column(String(20), nullable=False, comment='国标收货地址第三级地址')
    detailInfo = Column(String(100), nullable=False, comment='详细收货地址信息')
    telNumber = Column(String(20), nullable=False, comment='收货人手机号码')
    is_default = Column(Boolean, nullable=False, default=False, comment='默认不是默认地址')
    member_id = Column(Integer, nullable=False, comment='会员ID')

    def _set_fields(self):
        self._exclude = ['create_time', 'update_time', 'delete_time']
