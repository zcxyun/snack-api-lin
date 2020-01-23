import os

from flask import current_app
from lin import db
from lin.core import File
from lin.exception import ParameterException, NotFound
from lin.interface import InfoCrud


class Base(InfoCrud):
    __abstract__ = True

    def _set_fields(self):
        self._exclude = []

    @property
    def create_time_str(self):
        if self._create_time is None:
            return None
        return self._create_time.strftime('%Y-%m-%d %H:%M:%S')
    #
    # @property
    # def update_time(self):
    #     if self._update_time is None:
    #         return None
    #     return self._update_time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_model(cls, id, soft=True, *, throw=False):
        """根据ID查询单个模型数据"""
        model = cls.query.filter_by(id=id, soft=soft).first()
        if not model:
            if not throw:
                return None
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        return model

    @classmethod
    def get_all_models(cls, soft=True, *, throw=False):
        """获取所有数据"""
        models = cls.query.filter_by(soft=soft).all()
        if not models:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        return models

    @classmethod
    def get_paginate_models(cls, start, count, q=None, soft=True, *, throw=False):
        """查询分页数据(支持搜索)"""
        statement = cls.query.filter_by(soft=soft)
        if q:
            q = '%{}%'.format(q)
            statement = statement.filter(cls.name.ilike(q))
        total = statement.count()
        models = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not models:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def get_models_by_ids(cls, ids, soft=True, *, throw=False):
        """根据多个ID查询多个模型数据"""
        models = cls.query.filter_by(soft=soft).filter(cls.id.in_(ids)).all()
        if not models:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        return models

    @classmethod
    def get_model_with_img(cls, id, soft=True, *, throw=False):
        """根据ID查询带图片资源的单个模型数据"""
        res = db.session.query(cls, File.path).filter(
            cls.img_id == File.id,
            cls.id == id
        ).filter_by(soft=soft).first()
        if not res:
            if not throw:
                return None
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        model = cls._add_img_to_model(*res)
        return model

    @classmethod
    def get_all_models_with_img(cls, soft=True, *, throw=False):
        """获取所有数据带图片"""
        res = db.session.query(cls, File.path).filter(
            cls.img_id == File.id,
        ).filter_by(soft=soft).all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        models = cls._add_img_to_models(res)
        return models

    @classmethod
    def get_paginate_models_with_img(cls, start, count, q=None, soft=True, *, throw=False):
        """分页查询带图片资源的多个模型数据(支持搜索)"""
        statement = db.session.query(cls, File.path).filter(
            cls.img_id == File.id,
        ).filter_by(soft=soft)
        if q:
            q = '%{}%'.format(q)
            statement = statement.filter(cls.name.ilike(q))
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        models = cls._add_img_to_models(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def get_models_by_ids_with_img(cls, ids, soft=True, with_for_update=False, *, throw=False):
        """根据多个ID查询多个带图片资源的模型数据"""
        res = db.session.query(cls, File.path).filter(
            cls.img_id == File.id,
            cls.id.in_(ids),
        ).filter_by(soft=soft)
        if with_for_update:
            res = res.with_for_update()
        res = res.all()
        if not res:
            if not throw:
                return []
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        models = cls._add_img_to_models(res)
        return models

    @classmethod
    def get_file_url(cls, file_relative_path):
        """根据图片表中相对URL合成可访问URL"""
        site_main = current_app.config.get('SITE_DOMAIN')
        file_url = site_main + os.path.join(current_app.static_url_path, file_relative_path)
        return file_url

    @classmethod
    def _add_img_to_model(cls, model, img_relative_url):
        model.image = cls.get_file_url(img_relative_url)
        model._fields.append('image')
        return model

    @classmethod
    def _add_img_to_models(cls, data):
        """添加多个图片资源到多个模型"""
        res = []
        for item in data:
            model = cls._add_img_to_model(*item)
            res.append(model)
        return res

    @classmethod
    def add_model(cls, data, commit=True, *, throw=False):
        """添加模型"""
        if not data.get('name'):
            raise ParameterException(msg='要添加的数据中没有name属性')
        model = cls.query.filter_by(name=data.get('name')).first()
        if model is not None:
            if not throw:
                return False
            else:
                raise ParameterException(msg='相关资源已存在')
        model = cls.create(**data, commit=commit)
        return model

    @classmethod
    def edit_model(cls, id, data, commit=True, *, throw=False):
        """编辑模型"""
        if not data.get('name'):
            raise ParameterException(msg='要更改的数据中没有name属性')
        model = cls.query.filter_by(name=data.get('name')).filter(cls.id != id).first()
        if model is not None:
            if not throw:
                return False
            else:
                raise ParameterException(msg='相同名称资源已存在')
        model = cls.query.filter_by(id=id, soft=True).first()
        if not model:
            if not throw:
                return False
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        model.update(**data, commit=commit)
        return model

    @classmethod
    def remove_model(cls, id, commit=True, *, throw=False):
        """删除模型"""
        model = cls.query.filter_by(id=id, soft=True).first()
        if not model:
            if not throw:
                return False
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        model.hard_delete(commit=commit)
        return True

    @classmethod
    def hide_model(cls, id, commit=True, *, throw=False):
        """删除模型(软删除)"""
        model = cls.query.filter_by(id=id, soft=True).first()
        if not model:
            if not throw:
                return False
            else:
                raise NotFound(msg='相关资源未添加或已隐藏')
        model.delete(commit=commit)
        return True

    @classmethod
    def show_model(cls, id, commit=True, *, throw=False):
        """恢复模型(模型只能是软删除)"""
        model = cls.query.filter_by(id=id).filter(cls.delete_time != None).first()
        if not model:
            if not throw:
                return False
            else:
                raise NotFound(msg='相关资源未添加或已显示')
        model.update(delete_time=None, commit=commit)
        return True
