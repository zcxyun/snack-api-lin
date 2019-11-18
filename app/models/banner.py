from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Banner(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), comment='Banner名称')
    summary = Column(String(255), comment='Banner描述')

    def _set_fields(self):
        self._fields = ['name', 'summary']
