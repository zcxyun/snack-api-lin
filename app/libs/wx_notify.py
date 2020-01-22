from datetime import datetime

from flask import current_app, request

from app.libs.enum import OrderStatus
from app.libs.wx_helper import WxHelper
from app.libs.wx_msg import WxMessage
from app.models.order import Order


class WxNotify:

    @staticmethod
    def notify_process():
        fail_dict = {
            'return_code': 'FAIL',
            'return_msg': 'FAIL'
        }
        success_dict = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }
        mina_config = current_app.config['WE_CHAT']
        wx_helper = WxHelper(merchant_key=mina_config['PAY_KEY'])

        xml_fail = wx_helper.dict_2_xml(fail_dict)
        xml_success = wx_helper.dict_2_xml(success_dict)
        header = {'Content-Type': 'application/xml'}
        fail_res = (xml_fail, header)
        success_res = (xml_success, header)

        # 微信返回代码不对
        notify_data = wx_helper.xml_2_dict(request.data)
        current_app.logger.info(notify_data)
        if notify_data['return_code'] != 'SUCCESS' or notify_data['result_code'] != 'SUCCESS':
            return fail_res

        # 数据签名不一致
        notify_sign = notify_data['sign']
        notify_data.pop('sign')
        sign = wx_helper.create_sign(notify_data)
        if notify_sign != sign:
            return fail_res

        # 根据微信返回的订单号查询订单不存在
        order_no = notify_data['out_trade_no']
        order = Order.query.filter_by(order_no=order_no).first()
        if not order:
            return fail_res

        # 相关订单总金额不一致
        if int(order.total_price * 100) != int(notify_data['total_fee']):
            return fail_res

        # 相关订单不是待支付状态, 可能已经支付过了
        if order.order_status_enum != OrderStatus.UNPAID:
            return success_res

        # 更新相关订单状态和支付时间
        order.update(order_status=OrderStatus.UNDELIVERED, pay_time=datetime.now(), commit=True)

        # 发送模板消息
        access_token = wx_helper.get_access_token()
        WxMessage(order, access_token).send_tpl_message()
        return success_res
