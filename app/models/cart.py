from lin import db
from lin.core import File
from lin.exception import NotFound, ParameterException
from sqlalchemy import Column, Integer, func, Boolean

from app.models.base import Base
from app.models.product import Product


class Cart(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False, comment='会员ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    count = Column(Integer, nullable=False, comment='商品数量')
    selected = Column(Boolean, default=True, comment='是否被选中')

    @classmethod
    def get_products(cls, member_id):
        res = db.session.query(Product, cls.count, cls.selected, File.path).filter(
            cls.member_id == member_id,
            cls.product_id == Product.id,
            Product.img_id == File.id,
            cls.delete_time == None,
            Product.delete_time == None
        ).all()
        if res:
            res = cls._combine_data(res)
        return res

    @classmethod
    def get_total_count(cls, member_id):
        count = db.session.query(func.sum(cls.count)).filter_by(member_id=member_id, soft=True).scalar()
        return count or 0

    @classmethod
    def _combine_data(cls, data):
        res = []
        for item in data:
            model = cls._combine_single_data(*item)
            res.append(model)
        return res

    @classmethod
    def _combine_single_data(cls, product, count, selected, relative_img_path):
        product.count = count
        product.selected = selected
        product.image = cls.get_file_url(relative_img_path)
        product._fields.extend(['count', 'image', 'selected'])
        return product

    @classmethod
    def edit(cls, member_id, product_id, count, selected):
        models = cls.query.filter_by(member_id=member_id, soft=True).all()
        ids = [item.product_id for item in models]
        if len(models) >= 10 and product_id not in ids:
            raise ParameterException(msg='购物车最多放10种商品')
        model = cls.query.filter_by(product_id=product_id, member_id=member_id, soft=True).first()
        if model:
            model.update(count=count, selected=selected, commit=True)
            return True
        cls.create(member_id=member_id, product_id=product_id, count=count, selected=selected, commit=True)
        return True

    @classmethod
    def edit_some(cls, member_id, cart_contents):
        o_models = cls.query.filter_by(member_id=member_id).all()
        o_ids = set([item.product_id for item in o_models])
        ids = set([item['product_id'] for item in cart_contents])
        ids_to_add = ids - o_ids    # 要添加的商品ID列表
        ids_to_del = o_ids - ids    # 要删除的商品ID列表
        ids_to_update = ids & o_ids # 要更新的商品ID列表
        with db.auto_commit():
            if ids_to_add:
                models_to_add = list(filter(lambda x: x['product_id'] in ids_to_add, cart_contents))
                cls.add_models(models_to_add, member_id)
            if ids_to_del:
                models_to_del = list(filter(lambda x: x.product_id in ids_to_del, o_models))
                cls.del_models(models_to_del)
            if ids_to_update:
                o_models_to_update = list(filter(lambda x: x.product_id in ids_to_update, o_models))
                d_models_to_update = list(filter(lambda x: x['product_id'] in ids_to_update, cart_contents))
                cls.edit_models(o_models_to_update, d_models_to_update)
        return True

    @classmethod
    def add_models(cls, data, member_id):
        for item in data:
            cls.create(
                member_id=member_id,
                product_id=item['product_id'],
                count=item['count'],
                selected=item['selected']
            )

    @classmethod
    def del_models(cls, data):
        for item in data:
            item.hard_delete()

    @classmethod
    def edit_models(cls, o_models, d_models):
        id_contents = {item['product_id']: item for item in d_models}
        for model in o_models:
            model.update(
                count=id_contents[model.product_id]['count'],
                selected=id_contents[model.product_id]['selected']
            )

    @classmethod
    def clear(cls, member_id):
        models = cls.query.filter_by(member_id=member_id).all()
        if not models:
            raise NotFound(msg='购物车已空,不能再清空')
        for model in models:
            model.hard_delete(commit=True)
        return True

