from lin import db
from lin.exception import ParameterException
from sqlalchemy import Column, Integer, String, func, desc

from app.models.base import Base


class Comment(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, nullable=False, comment='会员ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')
    content = Column(String(20), nullable=False, comment='评论内容不能超过20个字')

    @classmethod
    def get_comments_of_product(cls, product_id, start=0, count=8):
        """分页显示某一商品的短评分组统计数量, 按统计数量倒序排序"""
        comments = db.session.query(
            cls.content,
            func.count(cls.content).label('nums')
        ).filter(
            cls.delete_time == None,
            cls.product_id == product_id
        ).group_by(
            cls.content
        ).order_by(
            desc('nums')
        ).offset(start).limit(count).all()
        comments = [{'content': content, 'nums': nums} for content, nums in comments]
        return comments

    @classmethod
    def add(cls, data, commit=True, *, throw=False):
        model = cls.query.filter_by(**data, soft=True).first()
        if model:
            if not throw:
                return False
            else:
                raise ParameterException(msg='相同内容已经评论过了')
        cls.create(**data, commit=commit)
        return True
