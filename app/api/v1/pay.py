from lin.redprint import Redprint

from app.libs.wx_notify import WxNotify

pay_api = Redprint('pay')


@pay_api.route('/notify', methods=['POST'])
def pay_notify():
    return WxNotify.notify_process()
