from ldap3 import *
from pwdselfservice.local_settings import *


def __ad_connect():
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
    return conn.search(base_dn, condition, attributes=attributes)


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
    return conn.search(base_dn, condition, attributes=attributes)


def ad_get_user_displayname_by_mail(user_mail_addr):
    conn = __ad_connect()
    conn.search(BASE_DN, '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=[
        'displayName'])
    user_displayname = conn.entries[0]['displayName']
    conn.unbind()
    return user_displayname


def ad_get_user_dn_by_mail(user_mail_addr):
    conn = __ad_connect()
    conn.search(BASE_DN,
                '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=['distinguishedName'])
    user_dn = conn.entries[0]['distinguishedName']
    return user_dn


def ad_get_user_status_by_mail(user_mail_addr):
    conn = __ad_connect()
    conn.search(BASE_DN,
                '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=['userAccountControl'])
    user_account_control = conn.entries[0]['userAccountControl']
    return user_account_control


def ad_unlock_user_by_mail(user_mail_addr):
    conn = __ad_connect()
    user_dn = ad_get_user_dn_by_mail(user_mail_addr)
    result = conn.extend.microsoft.unlock_account(user="%s" % user_dn)
    conn.unbind()
    return result


def ad_reset_user_pwd_by_mail(user_mail_addr, new_password):
    conn = __ad_connect()
    user_dn = ad_get_user_dn_by_mail(user_mail_addr)
    result = conn.extend.microsoft.modify_password(user="%s" % user_dn, new_password="%s" % new_password)
    conn.unbind()
    return result


def ad_modify_user_pwd_by_mail(user_mail_addr, old_password, new_password):
    conn = __ad_connect()
    user_dn = ad_get_user_dn_by_mail(user_mail_addr)
    result = conn.extend.microsoft.modify_password(user="%s" % user_dn, new_password="%s" % new_password,
                                                   old_password="%s" % old_password)
    conn.unbind()
    return result


def ad_get_user_locked_status_by_mail(user_mail_addr):
    conn = __ad_connect()
    conn.search(BASE_DN, '(&(objectclass=person)(mail=' + user_mail_addr + '))', attributes=['lockoutTime'])
    locked_status = conn.entries[0]['lockoutTime']
    print(locked_status)
    if '1601-01-01' in str(locked_status):
        return 0
    else:
        return locked_status
