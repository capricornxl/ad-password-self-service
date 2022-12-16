
# ##########################################################################
#  字符串前面的格式编码不要去掉了，主要是为了解决特殊字符被转义的问题。  #
# ##########################################################################

# ########## AD配置，修改为自己的
# AD主机，可以是IP或主机域名，例如可以是: abc.com或172.16.122.1
AD_HOST = r'修改成自己的'

# AD域控的DOMAIN，例如：比如你的域名是abc.com，那么这里的AD_DOMAIN就是：abc
# NTLM认证必须是domain\username
AD_DOMAIN = r'修改成自己的'

# 用于登录AD做用户信息处理的账号，需要有修改用户账号密码或信息的权限。
# AD账号，例如：pwdadmin
AD_LOGIN_USER = r'修改成自己的'
# 密码
AD_LOGIN_USER_PWD = r'修改为自己的'

# BASE DN，账号的查找DN路径，例如：'DC=abc,DC=com'，可以指定到OU之下，例如：'OU=RD,DC=abc,DC=com'。
BASE_DN = r'修改成自己的'

# 是否启用SSL,
# 注意：AD必须使用SSL才能修改密码（这里被坑了N久...）,自行部署下AD的证书服务，并颁发CA证书，重启服务器生效。具体教程百度一下，有很多。
AD_USE_SSL = True
# 连接的端口，如果启用SSL默认是636，否则就是389
AD_CONN_PORT = 636

# 验证的类型
#       钉钉 / 企业微信，自行修改
# 值是：DING /  WEWORK
AUTH_CODE_TYPE = 'DING'

# ########## 钉钉 《如果不使用钉钉扫码，可不用配置》##########
# 钉钉接口主地址，不可修改
DING_URL = r'https://oapi.dingtalk.com'

# 钉钉企业ID <CorpId>，修改为自己的
DING_CORP_ID = '修改为自己的'

# 钉钉企业内部开发，内部H5微应用或小程序，用于读取企业内部用户信息
DING_AGENT_ID = r'修改为自己的'
DING_APP_KEY = r'修改为自己的'
DING_APP_SECRET = r'修改为自己的'

# 移动应用接入 主要为了实现通过扫码拿到用户的unionid
DING_MO_APP_ID = r'修改为自己的'
DING_MO_APP_SECRET = r'修改为自己的'


# ####### 企业微信《如果不使用企业微信扫码，可不用配置》 ##########
# 企业微信的企业ID
WEWORK_CORP_ID = r'修改为自己的'
# 应用的AgentId
WEWORK_AGENT_ID = r'修改为自己的'
# 应用的Secret
WEWORK_AGNET_SECRET = r'修改为自己的'

# Redis配置
# redis的连接地址，redis://<Ip/Host>:<Port>/<数据库>
REDIS_LOCATION = r'redis://127.0.0.1:6379/1'
REDIS_PASSWORD = r'12345678'

# COOKIE超时时间，单位是秒，可不用修改
TMPID_COOKIE_AGE = 300

# 主页域名，钉钉跳转等需要指定域名，格式：pwd.abc.com。
# 如果是自定义安装，请修改成自己的域名
HOME_URL = 'PWD_SELF_SERVICE_DOMAIN'