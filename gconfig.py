from gevent import monkey
monkey.patch_all()
import multiprocessing
debug = True
loglevel = 'debug'
bind = '127.0.0.1:8000'  # 绑定与Nginx通信的端口
pidfile = 'glogs/gunicorn.pid'
logfile = 'glogs/debug.log'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent' # 默认为阻塞模式，最好选择gevent模式