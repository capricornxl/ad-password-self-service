# -*- coding: utf-8 -*-
import os
# Build paths inside the config like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_ENV = os.getenv('APP_ENV')

# ============================================================================
# 检测是否为 Django 主进程（避免重复打印初始化信息）
# ============================================================================
# Django runserver 会启动两个进程：主进程（监控文件变化）和子进程（实际运行服务）
# RUN_MAIN 环境变量只在子进程中存在
IS_MAIN_PROCESS = os.environ.get('RUN_MAIN') == 'true'

# ============================================================================
# 配置管理系统初始化（失败则终止启动）
# ============================================================================
try:
    from utils.config import init_config
    if not APP_ENV:
        if IS_MAIN_PROCESS:
            print("未设置环境变量APP_ENV，使用'config.yaml'!")
        CONFIG_FILE = os.path.join(BASE_DIR, 'conf/config.yaml')
    else:
        CONFIG_FILE = os.path.join(BASE_DIR, f'conf/config.{APP_ENV}.yaml')
    init_config(CONFIG_FILE)
    if IS_MAIN_PROCESS:
        print(f"配置系统初始化完成: {CONFIG_FILE}")
except Exception as e:
    error_msg = f"""
{'='*70}
致命错误：配置系统初始化失败
{'='*70}
配置文件: {os.path.join(BASE_DIR, 'conf/config.yaml')}
错误详情: {e}

请检查：
  1. 配置文件是否存在: conf/config.yaml
  2. YAML语法是否正确（缩进、冒号、引号）
  3. 环境变量是否已设置（如 LDAP_HOST, LDAP_DOMAIN 等）

{'='*70}
"""
    print(error_msg)
    raise SystemExit(1)  # 终止启动

# ============================================================================
# 日志系统初始化（失败则终止启动）
# ============================================================================
try:
    from utils.logger_factory import LoggerFactory
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'conf/logging_config.yaml')
    LoggerFactory.setup_logging(LOGGING_CONFIG_FILE)
    if IS_MAIN_PROCESS:
        print(f"日志系统初始化完成: {LOGGING_CONFIG_FILE}")
except Exception as e:
    error_msg = f"""
{'='*70}
致命错误：日志系统初始化失败
{'='*70}
配置文件: {os.path.join(BASE_DIR, 'conf/logging_config.yaml')}
错误详情: {e}

请检查：
  1. 配置文件是否存在: conf/logging_config.yaml
  2. YAML语法是否正确
  3. 日志目录是否可写: log/

{'='*70}
"""
    print(error_msg)
    raise SystemExit(1)  # 终止启动

# ============================================================================
# 调试模式配置
# ============================================================================
APP_ENV = os.getenv('APP_ENV')
if APP_ENV == 'dev':
    DEBUG = True
else:
    DEBUG = False

# ============================================================================
# SECRET_KEY配置（必须从配置文件加载，不允许使用默认值）
# ============================================================================
try:
    from utils.config import get_config
    config = get_config()
    SECRET_KEY = config.get('app.secret_key')
    
    # 验证SECRET_KEY是否有效
    if not SECRET_KEY or len(SECRET_KEY) < 32:
        raise ValueError("SECRET_KEY配置无效：必须至少32个字符")
    
    if IS_MAIN_PROCESS:
        print(f"SECRET_KEY加载完成: {'*' * 10}...{SECRET_KEY[-4:]}")  # 仅显示后4位
    
except Exception as e:
    error_msg = f"""
{'='*70}
致命错误：SECRET_KEY加载失败
{'='*70}
错误详情: {e}

解决方法：
  1. 确保 conf/config.yaml 中配置了 app.secret_key
  2. SECRET_KEY必须至少32个字符
  3. 建议使用随机生成的复杂字符串
{'='*70}
"""
    print(error_msg)
    raise SystemExit(1)  # 终止启动

ALLOWED_HOSTS = ['*']

# CSRF信任的源（从配置文件动态读取）
# 解决跨域 POST 请求时 "Origin checking failed" 错误
try:
    from utils.config import get_config
    _config = get_config()
    _home_url = _config.get('oauth.home_url', '')
    if _home_url:
        # 支持 http 和 https 协议
        CSRF_TRUSTED_ORIGINS = [
            f'https://{_home_url}',
            f'http://{_home_url}',
        ]
    else:
        # 如果没有配置 home_url，允许所有源（仅开发环境）
        CSRF_TRUSTED_ORIGINS = []
except Exception:
    CSRF_TRUSTED_ORIGINS = []

# 创建日志的路径
LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如果地址不存在，则会自动创建log文件夹
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

# 使用新的LoggerFactory配置日志系统（已在初始化部分处理）

# ============================================================================
# Django Cache配置（根据config.yaml动态配置，失败则终止启动）
# ============================================================================
try:
    from utils.config import get_config
    config = get_config()
    cache_backend = config.get('cache.backend', 'memory').lower()
    
    if cache_backend == 'database':
        # Database Cache（支持多实例部署，自动检测并创建缓存表）
        cache_table_name = config.get('cache.database.table_name', 'rate_limit_cache')
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': cache_table_name,
            }
        }
        
        # 标记需要自动创建缓存表（在PasswordManagerConfig.ready()中执行）
        CACHE_AUTO_CREATE_TABLE = True
        CACHE_TABLE_NAME = cache_table_name
        
    elif cache_backend == 'file':
        # File-based Cache（持久化存储，适合单机部署）
        cache_location = os.path.join(BASE_DIR, config.get('cache.file.location', 'cache_files'))
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': cache_location,
                'OPTIONS': {
                    'MAX_ENTRIES': config.get('cache.file.max_entries', 1000),
                    'CULL_FREQUENCY': config.get('cache.file.cull_frequency', 3),
                }
            }
        }
        
        # 自动创建缓存目录
        if not os.path.exists(cache_location):
            try:
                os.makedirs(cache_location, exist_ok=True)
                if IS_MAIN_PROCESS:
                    print(f"缓存目录创建成功: {cache_location}")
            except Exception as e:
                if IS_MAIN_PROCESS:
                    print(f"创建缓存目录失败: {e}")
        
        CACHE_AUTO_CREATE_TABLE = False
    else:  # memory（默认）
        # Memory Cache（性能最佳，零配置，推荐单机部署使用）
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': config.get('cache.memory.location', 'rate-limiting'),
                'OPTIONS': {
                    'MAX_ENTRIES': config.get('cache.memory.max_entries', 1000),
                    'CULL_FREQUENCY': config.get('cache.memory.cull_frequency', 3),
                }
            }
        }
        
        CACHE_AUTO_CREATE_TABLE = False
    
    if IS_MAIN_PROCESS:
        print(f"Django Cache配置完成：backend={cache_backend}")
    
except Exception as e:
    error_msg = f"""
{'='*70}
致命错误：Cache配置加载失败
{'='*70}
错误详情: {e}

请检查：
  1. 配置文件中 cache.backend 参数是否正确
  2. 有效值: memory（默认）、database、file
  3. Database模式会自动创建缓存表，无需手动操作

{'='*70}
"""
    print(error_msg)
    raise SystemExit(1)  # 终止启动
# LOGGING配置保留作为备用
LOGGING = {
    'version': 1,
    # 此选项开启表示禁用部分日志，不建议设置为True
    'disable_existing_loggers': False,
}


# SESSION
# 只有在settings.SESSION_SAVE_EVERY_REQUEST 为True时才有效
SESSION_SAVE_EVERY_REQUEST = True
# 过期时间分钟
SESSION_COOKIE_AGE = 300
# False 会话cookie可以在用户浏览器中保持有效期。True：关闭浏览器，则Cookie失效。
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# session使用的存储方式
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.password_manager',
]

# CACHES配置已在上面动态配置部分完成，此处不再重复定义

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# ============================================================================
# LDAP安全验证（失败则根据模式决定是否终止启动）
# ============================================================================
try:
    from utils.ldap.factory import LDAPFactory
    from utils.ldap.security_validator import LDAPSecurityValidator
    from utils.ldap.errors import LDAPException
    
    config = get_config()
    
    # 检查是否启用安全验证
    if config.get('ldap.security.validate_permissions_on_startup', True):
        if IS_MAIN_PROCESS:
            print("="*70)
            print("正在验证LDAP服务账号权限...")
            print("="*70)
        
        try:
            # 创建LDAP适配器
            ldap_type = config.get('ldap.type', 'ad')
            if IS_MAIN_PROCESS:
                print(f"LDAP类型: {ldap_type.upper()}")
            
            adapter = LDAPFactory.create_adapter(ldap_type)
            
            # 创建安全验证器
            validator = LDAPSecurityValidator(adapter)
            
            # 验证服务账号权限
            is_valid, message = validator.validate_service_account()
            
            if IS_MAIN_PROCESS:
                if is_valid:
                    print(f"{message}")
                else:
                    print(f"\n{message}\n")
                    
                    # 根据验证模式决定是否终止
                    validation_mode = config.get('ldap.security.validation_mode', 'warning')
                    
                    if validation_mode == 'strict':
                        error_msg = f"""
{'='*70}
致命错误：服务账号权限验证失败（严格模式）
{'='*70}
{message}

解决方法：
  1. 使用专用服务账号（非Domain Admins/Enterprise Admins）
  2. 创建自定义组并授予必要权限
  3. 将服务账号添加到推荐组
  4. 或在config.yaml中修改validation_mode为'warning'

{'='*70}
"""
                        print(error_msg)
                        raise SystemExit(1)  # 终止启动
                    elif validation_mode == 'warning':
                        print("  警告模式：权限存在风险，但允许继续启动")
                        print("  建议：修改服务账号或调整配置")
                
                print("="*70)
            
        except LDAPException as e:
            error_msg = f"""
{'='*70}
错误：LDAP权限验证失败
{'='*70}
{e.get_log_message()}

可能原因：
  1. LDAP连接失败
  2. 服务账号无法查询自身组信息
  3. 配置错误

{'='*70}
"""
            print(error_msg)
            
            # 严格模式下终止启动
            if config.get('ldap.security.validation_mode', 'warning') == 'strict':
                raise SystemExit(1)
        
        except Exception as e:
            print(f"权限验证异常: {e}")
            
            # 严格模式下终止启动
            if config.get('ldap.security.validation_mode', 'warning') == 'strict':
                raise SystemExit(1)
    else:
        if IS_MAIN_PROCESS:
            print("LDAP权限验证已禁用")

except ImportError as e:
    if IS_MAIN_PROCESS:
        print(f" LDAP模块导入失败: {e}")
        print("  如果不使用LDAP功能，可以忽略此警告")

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

# ============================================================================
# 启动信息汇总（仅在主进程显示）
# ============================================================================
if IS_MAIN_PROCESS:
    print("\n" + "="*70)
    print("Django 应用初始化完成")
    print("="*70)
    print(f"环境: {APP_ENV or 'production'}")
    print(f"调试模式: {'开启' if DEBUG else '关闭'}")
    print(f"配置文件: {CONFIG_FILE}")
    print(f"缓存后端: {config.get('cache.backend', 'memory')}")
    print("="*70 + "\n")
