# gunicorn.conf.py
bind = '0.0.0.0:8000'
workers = 4
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'