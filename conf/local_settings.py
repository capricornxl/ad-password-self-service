
# ##########################################################################
#  字符串前面的格式编码不要去掉了，主要是为了解决特殊字符被转义的问题。  #
# ##########################################################################

# ########## AD配置，修改为自己的
# AD主机，可以是IP或主机域名，例如可以是: abc.com或172.16.122.1
LDAP_HOST = r'修改成自己的'

# AD域控的DOMAIN，例如：比如你的域名是abc.com，那么这里的LDAP_DOMAIN就是：abc
# NTLM认证必须是domain\username
LDAP_DOMAIN = r'修改成自己的'

# 用于登录AD做用户信息处理的账号，需要有修改用户账号密码或信息的权限。
# AD账号，例如：pwdadmin
LDAP_LOGIN_USER = r'修改成自己的'
# 密码
LDAP_LOGIN_USER_PWD = r'修改为自己的'

# BASE DN，账号的查找DN路径，例如：'DC=abc,DC=com'，可以指定到OU之下，例如：'OU=RD,DC=abc,DC=com'。
# BASE_DN限制得越细，搜索用户的目录也就越小，一般情况下可以通过SEARCH_FILTER来过滤
BASE_DN = r'修改成自己的'

# ldap的search_filter，如果需要修改，请保持用户账号部分为 点位符{0} (代码中通过占位符引入账号)
# 例如，AD的用户账号属性是sAMAccountName，那么匹配的账号请配置成sAMAccountName={0}
#       LDAP中用户账号属性可能是uuid，那么匹配的账号请配置成uuid={0}
#       如果想限制用户在哪个组的才能使用，可以写成这样：
#       r'(&(objectClass=user)(memberof=CN=mis,OU=Groups,OU=OnTheJob,DC=abc,DC=com)(sAMAccountName={0}))', memberof 是需要匹配的组
# 默认配置是AD环境的，查询语句可以自行使用Apache Directory Studio测试后再配置
SEARCH_FILTER = r'(&(objectclass=user)(sAMAccountName={0}))'

# 是否启用SSL,
# 注意：AD中必须使用SSL才能修改密码（这里被坑了N久...）,自行部署下AD的证书服务，并颁发CA证书，重启服务器生效。具体教程百度一下，有很多。
# 如果使用Openldap，这里根据实际情况调整
LDAP_USE_SSL = True
# 连接的端口，如果启用SSL默认是636，否则就是389
LDAP_CONN_PORT = 636

# 验证的类型
#       钉钉 / 企业微信，自行修改
# 值是：DING /  WEWORK
INTEGRATION_APP_TYPE = 'WEWORK'

# ########## 钉钉 《如果不使用钉钉，可不用配置》##########
# 钉钉企业ID <CorpId>，修改为自己的
DING_CORP_ID = '修改为自己的'

# 钉钉企业内部开发，内部H5微应用或小程序，用于读取企业内部用户信息
DING_AGENT_ID = r'修改为自己的'
DING_APP_KEY = r'修改为自己的'
DING_APP_SECRET = r'修改为自己的'

# 移动应用接入 主要为了实现通过扫码拿到用户的unionid
DING_MO_APP_ID = r'修改为自己的'
DING_MO_APP_SECRET = r'修改为自己的'


# ####### 企业微信《如果不使用企业微信，可不用配置》 ##########
# 企业微信的企业ID
WEWORK_CORP_ID = r'修改为自己的'
# 应用的AgentId
WEWORK_AGENT_ID = r'修改为自己的'
# 应用的Secret
WEWORK_AGNET_SECRET = r'修改为自己的'

# 主页域名，钉钉跳转等需要指定域名，格式：pwd.abc.com。
# 如果是自定义安装，请修改成自己的域名
HOME_URL = 'PWD_SELF_SERVICE_DOMAIN'
# 平台显示的标题
TITLE = 'Self-Service'
