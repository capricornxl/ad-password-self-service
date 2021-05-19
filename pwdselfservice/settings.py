import os
from pwdselfservice.local_settings import REDIS_PASSWORD, REDIS_LOCATION

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nxnm3#&2tat_c2i6%$y74a)t$(3irh^gpwaleoja1kdv30fmcm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# 创建日志的路径
LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如果地址不存在，则会自动创建log文件夹
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    'version': 1,
    # 此选项开启表示禁用部分日志，不建议设置为True
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(module)s.%(funcName)s %(lineno)d: %(message)s'
            # 日志格式
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(pathname)s %(module)s.%(funcName)s %(lineno)d: %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            # 过滤器，只有当setting的DEBUG = True时生效
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            # 日志保存文件
            'filename': '%s/log.log' % LOG_PATH,
            # 日志格式，与上边的设置对应选择
            'formatter': 'verbose'
                }
    },
    'loggers': {
        'django': {
            # 日志记录器
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}


# SESSION
# 只有在settings.SESSION_SAVE_EVERY_REQUEST 为True时才有效
SESSION_SAVE_EVERY_REQUEST = True
# 过期时间分钟
SESSION_COOKIE_AGE = 300
# False 会话cookie可以在用户浏览器中保持有效期。True：关闭浏览器，则Cookie失效。
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# 建议配置，阻止 javascript 对会话数据的访问，提高安全性。
# SESSION_COOKIE_HTTPONLY= True


INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'resetpwd',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pwdselfservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pwdselfservice.wsgi.application'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
# STATIC_ROOT = 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
