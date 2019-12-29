from lin.exception import ParameterException
from sqlalchemy import Column, Integer, Boolean

from app.models.base import Base


class Like(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False, comment='会员id')
    product_id = Column(Integer, nullable=False, comment='商品id')
    like_status = Column(Boolean, default=False, comment='是否点赞')

    @classmethod
    def like(cls, product_id, member_id):
        """点赞"""
        data = {
            'product_id': product_id,
            'member_id': member_id
        }
        model = cls.query.filter_by(**data).first()
        if model:
            if model.delete_time is None:
                if model.like_status is True:
                    raise ParameterException(msg='对不起, 已经点过赞了, 不能再点了')
                else:
                    model.update(like_status=True, commit=True)
            else:
                model.update(delete_time=None, like_status=True, commit=True)
        else:
            cls.create(**data, like_status=True, commit=True)
        return True

    @classmethod
    def unlike(cls, product_id, member_id):
        """取消点赞"""
        data = {
            'product_id': product_id,
            'member_id': member_id
        }
        model = cls.query.filter_by(**data).first()
        if model:
            if model.delete_time is None:
                if model.like_status is False:
                    raise ParameterException(msg='对不起, 已经取消过点赞了, 不能再取消了')
                else:
                    model.update(like_status=False, commit=True)
            else:
                model.update(delete_time=None, like_status=False, commit=True)
        else:
            cls.create(**data, like_status=False, commit=True)
        return True

    @classmethod
    def get_like_status_by_member_product(cls, member_id, product_id):
        """获取某一会员某一商品的点赞状态"""
        model = cls.query.filter_by(soft=True, product_id=product_id, member_id=member_id).first()
        return model.like_status if model else False

    @classmethod
    def get_likes_by_member(cls, member_id):
        """获取某一会员的所有点赞模型"""
        models = cls.query.filter_by(soft=True, member_id=member_id, like_status=True).all()
        return models

    @classmethod
    def get_like_count_by_product(cls, product_id):
        """获取某一商品的点赞数量"""
        count = cls.query.filter_by(soft=True, product_id=product_id, like_status=True).count()
        return count

    @classmethod
    def get_like(cls, product_id, member_id):
        """获取某一会员某一商品的点赞信息"""
        like_count = cls.get_like_count_by_product(product_id)
        like_status = cls.get_like_status_by_member_product(member_id, product_id)
        return {
            'like_count': like_count,
            'like_status': like_status,
            'product_id': product_id
        }
