from lin.redprint import Redprint

banner_api = Redprint('banner')


@banner_api.route('/home', methods=['GET'])
def home_banner():
    pass