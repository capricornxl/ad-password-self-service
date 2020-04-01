from dingtalk.client import *
import requests
from pwdselfservice.local_settings import *


def ding_get_access_token():
    """
    获取钉钉access token
    :return:
    """
    resp = requests.get(
        url=DING_URL + "/gettoken",
        params=dict(appid=DING_SELF_APP_ID, appsecret=DING_SELF_APP_SECRET)
    )
    resp = resp.json()
    if resp['access_token']:
        return resp['access_token']
    else:
        return None


def ding_get_persistent_code(code, token):
    """
    获取钉钉当前用户的unionid
    :return:
    """
    resp = requests.post(
        url="%s/get_persistent_code?access_token=%s" % (DING_URL, token),
        json=dict(tmp_auth_code=code),
    )
    resp = resp.json()
    if resp['unionid']:
        return resp['unionid']
    else:
        return None


def ding_client_connect():
    """
    钉钉连接器
    :return:
    """
    client = AppKeyClient(corp_id=DING_CORP_ID, app_key=DING_APP_KEY, app_secret=DING_APP_SECRET)
    return client


def ding_get_dept_user_list_detail(dept_id, offset, size):
    """
    获取部门中的用户列表详细清单
    :param code:
    :return:
    """
    client = ding_client_connect()
    result = client.user.list(department_id=dept_id, offset=offset, size=size)
    return result


def ding_get_userinfo_by_code(code):
    """
    :param code:  requestAuthCode接口中获取的CODE
    :return:
    """
    client = ding_client_connect()
    resutl = client.user.getuserinfo(code)
    return resutl


def ding_get_userid_by_unionid(unionid):
    """
    :param unionid:  用户在当前钉钉开放平台账号范围内的唯一标识
    :return:
    """
    client = ding_client_connect()
    resutl = client.user.get_userid_by_unionid(unionid)
    if resutl['userid']:
        return resutl['userid']
    else:
        return None


def ding_get_org_user_count():
    """
    企业员工数量
    only_active – 是否包含未激活钉钉的人员数量
    :return:
    """
    client = ding_client_connect()
    resutl = client.user.get_org_user_count('only_active')
    return resutl


def ding_get_userinfo_detail(user_id):
    """
    user_id –  用户ID
    :return:
    """
    client = ding_client_connect()
    resutl = client.user.get(user_id)
    return resutl
