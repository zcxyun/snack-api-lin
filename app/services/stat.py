import json
from datetime import datetime
from decimal import Decimal
from random import randint

from lin import db
from lin.exception import NotFound
from pydash import group_by, assign_with, flat_map, key_by
from sqlalchemy import func

from app.libs.enum import OrderStatus
from app.models.app_access_log import AppAccessLog
from app.models.member import Member
from app.models.order import Order
from app.models.product import Product
from app.models.stat_all_daily import StatAllDaily
from app.models.stat_member_daily import StatMemberDaily
from app.models.stat_product_daily import StatProductDaily


class Stat:
    """统计某日的数据"""

    def __init__(self, one_date):
        self.one_date = one_date
        self.date_from = datetime.strptime(f'{one_date} 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.date_to = datetime.strptime(f'{one_date} 23:59:59', '%Y-%m-%d %H:%M:%S')

    def stat_all(self):
        """统计某天订单相关数据"""
        price, order_count = self.stat_price_count_for_all()
        total_price, total_order_count = self.stat_total_price_count_for_all()
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
        # 测试数据
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

    def stat_price_count_for_all(self):
        """统计某天订单总金额和总数量"""
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

    def stat_total_price_count_for_all(self):
        """统计至计为止所有订单总金额和总数量"""
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

    def stat_member(self):
        """未完成, 暂不统计单个会员一天的总消费和总购买数量, 感觉没意义"""
        pass
        # res = db.session.query(
        #     Member.id, func.sum(Order.total_price), func.sum(Order.total_count)
        # ).filter_by(soft=True).filter(
        #     Order.order_status != OrderStatus.UNPAID.value,
        #     Order.order_status != OrderStatus.CANCEL.value,
        #     Order._create_time >= self.date_from,
        #     Order._create_time <= self.date_to
        # ).group_by(Member.id).all()
        # with db.auto_commit():
        #     for item in res:
        #         StatMemberDaily.create(
        #             date=self.one_date,
        #             member_id=item[0],
        #             total_pay=item[1],
        #             total_buy_count=item[2],
        #         )

    def stat_product(self):
        """统计某天商品数据"""
        # 查询当天消费过的商品
        res = db.session.query(Order.snap_products).filter_by(soft=True).filter(
            Order.order_status != OrderStatus.UNPAID.value,
            Order.order_status != OrderStatus.CANCEL.value,
            Order._create_time >= self.date_from,
            Order._create_time <= self.date_to
        ).all()
        if res:
            product_dicts = flat_map(res, lambda x: json.loads(x[0]))
            products = self.define_products(product_dicts)
        else:
            products = []
        product_ids = db.session.query(Product.id).filter_by(soft=True).all()
        # 所有商品ID列表
        product_ids = [item[0] for item in product_ids]
        # 所有当天消费过的商品ID列表
        ids_products_paid = key_by(products, 'id')
        with db.auto_commit():
            for product_id in product_ids:
                total_price_res = Decimal('0.00')
                total_count_res = 0
                if product_id in ids_products_paid.keys():
                    total_price_res = ids_products_paid[product_id]['total_price_str']
                    total_count_res = ids_products_paid[product_id]['count']
                # StatProductDaily.create(
                #     date=self.one_date,
                #     product_id=product_id,
                #     total_price=total_price_res,
                #     total_count=total_count_res
                # )
                StatProductDaily.create(
                    date=self.one_date,
                    product_id=product_id,
                    total_price=Decimal(f'{randint(1, 999)}.34'),
                    total_count=randint(1, 999)
                )

    def define_products(self, data):
        """
        处理商品数据
        1 按商品ID分组;
        2 分组后的数据合并数值成为一个字典, 数量与金额相加, 其它不变;
        3 将处理完的数据(一个字典)添加进新的数组并返回
        """
        def ass(obj_v, src_v, k, obj, src):
            if k == 'id' or k == 'name' or k == 'image':
                return obj_v
            elif k == 'count':
                return obj_v + src_v
            else:
                return Decimal(obj_v) + Decimal(src_v)
        group = group_by(data, 'id')
        res = []
        for item in group.values():
            if len(item) > 1:
                obj = assign_with(*item, ass)
            else:
                obj = item[0]
            res.append(obj)
        return res
