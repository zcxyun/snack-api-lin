from flask import current_app
from lin import db
from lin.exception import ParameterException, NotFound
from sqlalchemy import Column, Integer, String, DECIMAL, SmallInteger, Text, DateTime

from app.libs.enum import OrderStatus
from app.libs.utils import datetime_format
from app.models.base import Base
from app.models.member import Member


class Order(Base):
    id = Column(Integer, primary_key=True)
    order_no = Column(String(32), nullable=False, comment='订单号')
    member_id = Column(Integer, nullable=False, comment='会员id，注意并不是openid')
    total_price = Column(DECIMAL, nullable=False, comment='总价格')
    total_count = Column(Integer, nullable=False, default=0, comment='总数量')
    order_status = Column(
        SmallInteger, nullable=False, default=0,
        comment='0 待付款, 1 待发货, 2 待收货, 3 已完成, -1 已取消, -2 已支付, 但库存不足')
    pay_time = Column(DateTime, comment='支付时间')

    snap_img = Column(String(255), comment='订单快照图片')
    snap_name = Column(String(80), comment='订单快照名称')
    snap_items = Column(Text, comment='订单其他信息快照（json)')
    snap_address = Column(String(500), comment='地址快照')
    prepay_id = Column(String(100), comment='订单微信支付的预订单id（用于发送模板消息）')

    def _set_fields(self):
        self._fields = ['order_no', 'total_price', 'total_count', 'order_status', 'order_status_desc',
                        'snap_img', 'snap_name', 'snap_items', 'snap_address',  'pay_time_format', 'create_time']

    @property
    def order_status_enum(self):
        try:
            status = OrderStatus(self.order_status)
        except ValueError:
            current_app.logger.error('数据库中的订单状态不符合规范')
            return
        return status

    @order_status_enum.setter
    def order_status_enum(self, status):
        if type(status) == OrderStatus:
            self.order_status = status.value
        else:
            raise ParameterException('要更改的订单状态不符合规范')

    @property
    def order_status_desc(self):
        status_map = {
            OrderStatus.UNPAID: '待支付',
            OrderStatus.UNDELIVERED: '待发货',
            OrderStatus.UNRECEIPTED: '待收货',
            OrderStatus.DONE: '已完成',
            OrderStatus.CANCEL: '已取消',
            OrderStatus.PAID_BUT_INSUFFICIENT_STOCK: '已支付, 但库存不足'
        }
        return status_map.get(self.order_status_enum, '未设置订单状态文字描述信息')

    # @property
    # def order_number(self):
    #     order_number = self.create_time.strftime('%Y%m%d%H%M%S')
    #     order_number += str(self.id).zfill(5)
    #     return order_number

    @property
    def pay_time_format(self):
        if not self.pay_time:
            return '未支付'
        return datetime_format(self.pay_time)

    @classmethod
    def get_paginate_with_member(cls, start, count, q, soft=True, *, err_msg=None):
        statement = db.session.query(cls, Member).filter_by(soft=soft).filter(cls.member_id == Member.id)
        if q:
            q = '%{}%'.format(q)
            statement = statement.filter(cls.order_no.ilike(q))
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def _combine_data(cls, data):
        res = []
        for i in data:
            model = cls._combine_single_data(*i)
            res.append(model)
        return res

    @classmethod
    def _combine_single_data(cls, order, member):
        order.member = member.nickName
        order.member_avatarurl = member.avatarUrl
        order._fields.extend(['member', 'member_avatarurl'])
        return order
