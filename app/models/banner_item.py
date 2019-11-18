from sqlalchemy import Column, Integer, SmallInteger

from app.models.base import Base


class BannerItem(Base):
    id = Column(Integer, primary_key=True)
    img_id = Column(Integer, nullable=False, comment='关联图片ID')
    content_id = Column(Integer, nullable=False, comment='导向内容表ID，根据不同的type导向不同的表')
    type = Column(
        SmallInteger, nullable=False, default=1,
        comment='跳转类型: 可能导向商品，可能导向专题，可能导向其他 0 无导向 1 导向商品 2 导向专题')
    banner_id = Column(Integer, nullable=False, comment='banner表ID')

    def _set_fields(self):
        self._fields = ['content_id', 'type', 'banner_id']
