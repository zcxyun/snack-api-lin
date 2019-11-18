from lin import db
from lin.core import File
from lin.exception import NotFound
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import aliased

from app.models.base import Base


class Theme(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True, comment='专题名称')
    summary = Column(String(255), comment='专题描述')
    topic_img_id = Column(Integer, nullable=False, comment='主题图ID')
    head_img_id = Column(Integer, nullable=False, comment='专题列表页，头图ID')

    def _set_fields(self):
        self._exclude = ['create_time', 'update_time']

    @classmethod
    def get_model(cls, id, soft=True, *, err_msg=None):
        topic_img = aliased(File)
        head_img = aliased(File)
        res = db.session.query(cls, topic_img.path, head_img.path).filter(
            cls.topic_img_id == topic_img.id,
            cls.head_img_id == head_img.id,
            cls.id == id
        ).filter_by(soft=soft).first()
        if not res:
            if err_msg is None:
                return None
            else:
                raise NotFound(msg=err_msg)
        model = cls._combine_single_data(*res)
        return model

    @classmethod
    def get_all_models(cls, soft=True, *, err_msg=None):
        topic_img = aliased(File)
        head_img = aliased(File)
        res = db.session.query(cls, topic_img.path, head_img.path).filter(
            cls.topic_img_id == topic_img.id,
            cls.head_img_id == head_img.id,
        ).filter_by(soft=soft).all()
        if not res:
            if err_msg is None:
                return None
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(res)
        return models

    @classmethod
    def get_paginate_models(cls, start, count, q=None, soft=True, *, err_msg=None):
        topic_img = aliased(File)
        head_img = aliased(File)
        statement = db.session.query(cls, topic_img.path, head_img.path).filter(
            cls.topic_img_id == topic_img.id,
            cls.head_img_id == head_img.id
        ).filter_by(soft=soft)
        if q:
            q = '%{}%'.format(q)
            statement = statement.filter(cls.name.ilike(q))
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def _combine_single_data(cls, model, topic_img, head_img):
        model.topic_img = cls.get_file_url(topic_img)
        model.head_img = cls.get_file_url(head_img)
        model._fields.extend(['topic_img', 'head_img'])
        return model

    @classmethod
    def _combine_data(cls, data):
        res = []
        for item in data:
            model = cls._combine_single_data(*item)
            res.append(model)
        return res
