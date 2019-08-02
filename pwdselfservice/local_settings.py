# AD配置
AD_HOST = 'abc.com'
AD_LOGIN_USER = 'abc\pwdadmin'
AD_LOGIN_USER_PWD = 'gVykWgNNF0oBQzwmwPp8'
BASE_DN = 'OU=RD,DC=abc,DC=com'

# 钉钉配置
# 钉钉统一接口地址，不可修改。
DING_URL = "https://oapi.dingtalk.com/sns"

# 钉钉企业ID
DING_CORP_ID = 'ding0176902811df32'

# 钉钉E应用
DING_AGENT_ID = '25311eeee'
DING_APP_KEY = 'dingqdzmax324v'
DING_APP_SECRET = 'rnGRJhhw5kVmzykG9mrTDxewmI4e0myPAluMlguYQOaadsf2fhgfdfsx'

# 钉钉移动应用接入
DING_SELF_APP_ID = 'dingoabrzugusdfdf33fgfds'
DING_SELF_APP_SECRET = 'IrH2MedSgesguFjGvFCTjXYBRZDhA5AI4ADQU5710sgLffdsadf32uhgfdsfs'

# Crypty key 通过generate_key生成，可不用修改，如果需要自行生成，请使用Crypto.generate_key自行生成，用于加密页面提交的明文密码
CRYPTO_KEY = b'dp8U9y7NAhCD3MoNwPzPBhBtTZ1uI_WWSdpNs6wUDgs='

# COOKIE 超时，定义多长时间页面失效，单位秒。
TMPID_COOKIE_AGE = 300

# 主页域名，index.html中的钉钉跳转等需要指定域名。
HOME_URL = 'https://pwd.abc.com'