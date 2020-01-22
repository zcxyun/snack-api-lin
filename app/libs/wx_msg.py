import json

import requests
from flask import current_app
from lin.exception import NotFound

from app.libs.error_code import WxTplMsgException
from app.libs.utils import datetime_format
from app.models.member import Member


class WxMessage:

    def __init__(self, order, access_token, tpl_jump_page=''):
        if order and access_token:
            self._send_url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={}'.format(access_token)

            self._touser = self._get_openid_by_order(order)
            self._template_id = current_app.config['WE_CHAT']['TPL_MSG_ID']
            self._page = tpl_jump_page
            self._form_id = order.prepay_id
            self._data = self._prepare_msg_data(order)
            self._emphasisKeyWord = 'keyword2.DATA'

    def send_tpl_message(self):
        headers = {'content-type': 'application/json'}
        params = {
            "touser": self._touser,
            "template_id": self._template_id,
            "page": self._page,
            "form_id": self._form_id,
            "data": self._data
        }
        r = requests.post(url=self._send_url, data=json.dumps(params), headers=headers)
        r.encoding = 'utf-8'
        if r.status_code != 200 or not r.text:
            raise WxTplMsgException()
        if r.get('errcode') and r.get('errmsg'):
            raise WxTplMsgException(msg=r.get('errmsg'))
        current_app.logger.info(r.text)
        return True

    @staticmethod
    def _prepare_msg_data(order):
        data = {
            'keyword1': {
                'value': '顺风速运'
            },
            'keyword2': {
                'value': order.snap_name,
                'color': '#27408B'
            },
            'keyword3': {
                'value': order.order_no
            },
            'keyword4': {
                'value': datetime_format()
            }
        }
        return data

    def _get_openid_by_order(self, order):
        member = Member.get_model(order.member_id)
        if not member:
            raise NotFound(msg='相关会员不存在')
        return member.openid
