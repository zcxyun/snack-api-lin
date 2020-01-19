from gevent import monkey
monkey.patch_all()
import multiprocessing
debug = True
loglevel = 'debug'
bind = 'http://localhost:5000'  # 绑定与Nginx通信的端口
pidfile = 'glogs/gunicorn.pid'
logfile = 'glogs/debug.log'
workers = multiprocessing.cpu_count()
worker_class = 'gevent' # 默认为阻塞模式，最好选择gevent模式