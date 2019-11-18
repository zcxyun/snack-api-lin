from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, comment='分类名称')
    img_id = Column(Integer, comment='关联图片ID')
    summary = Column(String(100), comment='描述')

    def _set_fields(self):
        self._exclude = ['create_time', 'update_time']
