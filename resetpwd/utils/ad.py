from ldap3 import *
from pwdselfservice.local_settings import *


def __ad_connect():
    """
    AD连接器
    :return:
    """
    username = str(AD_LOGIN_USER).lower()
    server = Server(host=AD_HOST, use_ssl=True, port=636, get_info='ALL')
    try:
        conn = Connection(server, auto_bind=True, user=username, password=AD_LOGIN_USER_PWD, authentication='NTLM')
        return conn
    except Exception:
        raise Exception('Server Error. Could not connect to Domain Controller')


def ad_ensure_user_by_sam(username):
    """
    通过sAMAccountName查询某个用户是否在AD中
    :param username:  除去@domain.com 的部分
    :return: True or False
    """
    conn = __ad_connect()
    base_dn = BASE_DN
    condition = '(&(objectclass=person)(mail=' + username + '))'
    attributes = ['sAMAccountName']
    result = conn.search(base_dn, condition, attributes=attributes)
    conn.unbind()
    return result


def ad_ensure_user_by_mail(user_mail_addr):
    """
    通过mail查询某个用户是否在AD中
    :param user_mail_addr:
    :return: True or False
    """
    conn = __ad_connect()
    base_dn = BASE_DN
    condition = '(&(objectclass=person)(mail=' + user_mail_addr + '))'
    attributes = ['mail']
    result = conn.search(base_dn, condition, attributes=attributes)
    conn.unbind()
    return result


def ad_get_user_displayname_by_mail(user_mail_addr):
    """
    通过mail查询某个用户的显示名
    :param user_mail_addr:
    :return: user_displayname
    """
    conn = __ad_connect()
    conn.search(BASE_DN, '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=[
        'displayName'])
    user_displayname = conn.entries[0]['displayName']
    conn.unbind()
    return user_displayname


def ad_get_user_dn_by_mail(user_mail_addr):
    """
    通过mail查询某个用户的完整DN
    :param user_mail_addr:
    :return: DN
    """
    conn = __ad_connect()
    conn.search(BASE_DN,
                '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=['distinguishedName'])
    user_dn = conn.entries[0]['distinguishedName']
    conn.unbind()
    return user_dn


def ad_get_user_status_by_mail(user_mail_addr):
    """
    通过mail查询某个用户的账号状态
    :param user_mail_addr:
    :return: user_account_control code
    """
    conn = __ad_connect()
    conn.search(BASE_DN,
                '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=['userAccountControl'])
    user_account_control = conn.entries[0]['userAccountControl']
    conn.unbind()
    return user_account_control


def ad_unlock_user_by_mail(user_mail_addr):
    """
    通过mail解锁某个用户
    :param user_mail_addr:
    :return:
    """
    conn = __ad_connect()
    user_dn = ad_get_user_dn_by_mail(user_mail_addr)
    result = conn.extend.microsoft.unlock_account(user="%s" % user_dn)
    conn.unbind()
    return result


def ad_reset_user_pwd_by_mail(user_mail_addr, new_password):
    """
    通过mail重置某个用户的密码
    :param user_mail_addr:
    :return:
    """
    conn = __ad_connect()
    user_dn = ad_get_user_dn_by_mail(user_mail_addr)
    result = conn.extend.microsoft.modify_password(user="%s" % user_dn, new_password="%s" % new_password)
    conn.unbind()
    return result


def ad_modify_user_pwd_by_mail(user_mail_addr, old_password, new_password):
    """
    通过mail修改某个用户的密码
    :param user_mail_addr:
    :return:
    """
    conn = __ad_connect()
    user_dn = ad_get_user_dn_by_mail(user_mail_addr)
    result = conn.extend.microsoft.modify_password(user="%s" % user_dn, new_password="%s" % new_password,
                                                   old_password="%s" % old_password)
    conn.unbind()
    return result


def ad_get_user_locked_status_by_mail(user_mail_addr):
    """
    通过mail获取某个用户账号是否被锁定
    :param user_mail_addr:
    :return: 如果结果是1601-01-01说明账号未锁定，返回0
    """
    conn = __ad_connect()
    conn.search(BASE_DN, '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=['lockoutTime'])
    locked_status = conn.entries[0]['lockoutTime']
    conn.unbind()
    if '1601-01-01' in str(locked_status):
        return 0
    else:
        return locked_status
