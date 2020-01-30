from flask import request
from sqlalchemy import Column, Integer, String

from .base import Base


class AppAccessLog(Base):
    id = Column(Integer, primary_key=True)
    refer_url = Column(String(255), comment='当前访问的refer')
    target_url = Column(String(255), comment='访问的url')
    ua = Column(String(255), comment='访问的user-agent')
    ip = Column(String(32), comment='访问ip')

    @classmethod
    def add_access_log(cls):
        cls.create(
            refer_url=request.referrer,
            target_url=request.url,
            ua=request.headers.get('User-Agent'),
            ip=request.remote_addr,
            commit=True
        )
        return True

