from gevent import monkey
monkey.patch_all()
import multiprocessing
debug = False
reload = True
loglevel = 'info'
bind = 'localhost:5000'  # 绑定与Nginx通信的端口
pidfile = 'glogs/gunicorn.pid'
errorlog = 'glogs/error.log'
accesslog = 'glogs/access.log'
workers = multiprocessing.cpu_count() * 2 + 1
#workers = 1
worker_class = 'gevent' # 默认为阻塞模式，最好选择gevent模式
