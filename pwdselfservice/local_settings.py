# AD配置，修改为自己的
# AD主机，可以是IP或主机域名，例如可以是:abc.com或172.16.122.1
AD_HOST = '修改为自己的'

# 用于登录AD做用户信息验证的账号， 需要有修改用户账号密码的权限。
# 账号格式使用DOMAIN\USERNAME，例如：abc\pwdadmin
AD_LOGIN_USER = '修改为自己的'

# 密码
AD_LOGIN_USER_PWD = '修改为自己的'

# BASE DN，账号的查找DN路径，例如：'DC=abc,DC=com'，可以指定到OU之下，例如：'OU=RD,DC=abc,DC=com'。
BASE_DN = '修改为自己的'

# 钉钉配置
# 钉钉接口地址，不可修改
DING_URL = "https://oapi.dingtalk.com/sns"

# 钉钉企业ID，修改为自己的
DING_CORP_ID = '修改为自己的'

# 钉钉E应用，修改为自己的
DING_AGENT_ID = '修改为自己的'
DING_APP_KEY = '修改为自己的'
DING_APP_SECRET = '修改为自己的'

# 钉钉移动应用接入，修改为自己的
DING_SELF_APP_ID = '修改为自己的'
DING_SELF_APP_SECRET = '修改为自己的'

# Crypty key 通过generate_key生成，可不用修改
CRYPTO_KEY = b'dp8U9y7NAhCD3MoNwPzPBhBtTZ1uI_WWSdpNs6wUDgs='

# COOKIE 超时单位是秒，可不用修改
TMPID_COOKIE_AGE = 300


# 主页域名，index.html中的钉钉跳转等需要指定域名。
HOME_URL = 'PWD_SELF_SERVICE_DOMAIN'