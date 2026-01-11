# -*- coding: utf-8 -*-
import os
import sys

from utils.path_tool import BASE_DIR

# ============================================================
# Gunicorn配置文件
# 环境变量优先,默认值作为后备
# ============================================================
# 基础配置
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:9000')
workers = int(os.getenv('GUNICORN_WORKERS', 1))
threads = int(os.getenv('GUNICORN_THREADS', 2))

# 超时配置
timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
graceful_timeout = int(os.getenv('GRACEFUL_TIMEOUT', 300))
keepalive = int(os.getenv('GUNICORN_KEEPALIVE', 65))
wsgi_app = os.getenv('GUNICORN_WSGI_APP', 'config.wsgi:application')

# 日志配置
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
accesslog = "-"  # stdout
errorlog = "-"   # stderr
capture_output = True

# 性能优化
max_requests = int(os.getenv('GUNICORN_MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('GUNICORN_MAX_REQUESTS_JITTER', 100))

# 开发模式
django_env = os.getenv('APP_ENV', '')
reload = True if django_env == 'dev' else os.getenv('GUNICORN_RELOAD', 'false').lower() == 'true'
preload_app = not reload

# 环境变量透传
raw_env = [
    f'DJANGO_SETTINGS_MODULE={os.getenv("DJANGO_SETTINGS_MODULE")}',
    f'DJANGO_RUNNING_ENV={django_env}',
    f'PYTHONPATH={BASE_DIR}',
]

# 启动时打印配置
print("=" * 60)
print("Gunicorn Configuration:")
print(f"  Application: {wsgi_app}")
print(f"  Bind: {bind}")
print(f"  Workers: {workers}")
print(f"  Threads: {threads}")
print(f"  Timeout: {timeout}s")
print(f"  Graceful Timeout: {graceful_timeout}s")
print(f"  Keepalive: {keepalive}s")
print(f"  Log Level: {loglevel}")
print(f"  Reload: {reload}")
print(f"  Preload App: {preload_app}")
print(f"  Django Env: {django_env}")
print("=" * 60)
