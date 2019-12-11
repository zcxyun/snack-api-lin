from lin.exception import NotFound
from sqlalchemy import Column, Integer

from app.models.base import Base


class ThemeProduct(Base):
    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, nullable=False, comment='主题ID')
    product_id = Column(Integer, nullable=False, comment='商品ID')

    @classmethod
    def edit_themes(cls, tids, pid, *, err_msg=None):
        models = cls.query.filter_by(product_id=pid, soft=True).all()
        if not models:
            if err_msg is None:
                return False
            else:
                raise NotFound(msg=err_msg)
        id_themes = {model.theme_id: model for model in models}
        theme_ids = id_themes.keys()
        adding_ids = set(tids) - set(theme_ids)   # 原主题ids 添加 传入主题ids 和 原主题ids 差集
        deling_ids = set(theme_ids) - set(tids)   # 原主题ids 软删除 原主题ids 和传入主题ids 差集
        for adding_id in adding_ids:
            exist = cls.query.filter_by(theme_id=adding_id, product_id=pid).first()
            if exist:
                exist.update(delete_time=None)
            else:
                cls.create(theme_id=adding_id, product_id=pid)
        for deling_id in deling_ids:
            id_themes[deling_id].delete()
