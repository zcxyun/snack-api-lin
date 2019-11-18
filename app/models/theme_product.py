from lin.exception import ParameterException, NotFound
from sqlalchemy import Column, Integer

from app.models.base import Base


class ThemeProduct(Base):
    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, nullable=False, comment='主题ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')

    @classmethod
    def new(cls, tid, pid, *, err_msg=None):
        model = cls.query.filter_by(theme_id=tid, product_id=pid).first()
        if model:
            if err_msg is None:
                return False
            else:
                raise ParameterException(msg=err_msg)
        cls.create(theme_id=tid, product_id=pid, commit=True)
        return True

    @classmethod
    def remove(cls, tid, pid, *, err_msg=None):
        model = cls.query.filter_by(theme_id=tid, product_id=pid, soft=True).first()
        if not model:
            if err_msg is None:
                return False
            else:
                raise NotFound(msg=err_msg)
        model.delete(commit=True)
        return True

    @classmethod
    def revert(cls, tid, pid, *, err_msg=None):
        model = cls.query.filter_by(theme_id=tid, product_id=pid).filter(cls.delete_time != None).first()
        if not model:
            if err_msg is None:
                return False
            else:
                raise NotFound(msg=err_msg)
        model.update(delete_time=None, commit=True)
        return True
