from lin.exception import NotFound
from pydash import difference_by, intersection_by
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class ProductProperty(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(30), default='', comment='详情属性名称')
    detail = Column(String(255), nullable=False, comment='详情属性')
    product_id = Column(Integer, nullable=False, comment='商品id')

    def _set_fields(self):
        self._fields = ['name', 'detail']

    @classmethod
    def get_by_product_id(cls, product_id, soft=True, *, err_msg=None):
        models = cls.query.filter_by(product_id=product_id, soft=soft).all()
        if not models:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        return models

    @classmethod
    def get_by_product_ids(cls, product_ids, soft=True, *, err_msg=None):
        models = cls.query.filter_by(soft=soft).filter(
            cls.product_id.in_(product_ids)).order_by(cls.product_id.desc()).all()
        if not models:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        return models

    @classmethod
    def edit_properties(cls, pid, props):
        pps = cls.get_by_product_id(pid)
        key_pps = {pp.name: pp for pp in pps} if pps else {}
        dict_pps = [dict(pp) for pp in pps] if pps else []

        # 原属性列表 软删除 原属性列表 和 传入属性列表 差集
        pps_diff_props = difference_by(dict_pps, props, lambda p: p['name'])
        # 原属性列表 更新 原属性列表 和 传入属性列表 交集
        props_inter_pps = intersection_by(props, dict_pps, lambda p: p['name'])
        # 原属性列表 添加 传入属性列表 和 原属性列表 差集
        props_diff_pps = difference_by(props, dict_pps, lambda p: p['name'])

        for p in pps_diff_props:
            key_pps[p['name']].delete()
        for p in props_inter_pps:
            key_pps[p['name']].update(**p)
        for p in props_diff_pps:
            exist = cls.query.filter_by(name=p['name'], product_id=pid).first()
            if exist:
                exist.update(delete_time=None)
            else:
                cls.create(**p, product_id=pid)
