# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import hmac
import time
from hashlib import sha256
from urllib.parse import quote

import requests
from dingtalk.client import AppKeyClient

from pwdselfservice.local_settings import DING_APP_KEY, DING_APP_SECRET, DING_CORP_ID, DING_URL, DING_MO_APP_ID, DING_MO_APP_SECRET


class DingDingOps(object):
    def __init__(self, corp_id=DING_CORP_ID, app_key=DING_APP_KEY, app_secret=DING_APP_SECRET, mo_app_id=DING_MO_APP_ID, mo_app_secret=DING_MO_APP_SECRET):
        self.corp_id = corp_id
        self.app_key = app_key
        self.app_secret = app_secret
        self.mo_app_id = mo_app_id
        self.mo_app_secret = mo_app_secret

    @property
    def ding_client_connect(self):
        """
        钉钉连接器
        :return:
        """
        return AppKeyClient(corp_id=self.corp_id, app_key=self.app_key, app_secret=self.app_secret)

    @property
    def ding_get_access_token(self):
        """
        获取企业内部应用的access_token
        :return:
        """
        return self.ding_client_connect.access_token

    def ding_get_dept_user_list_detail(self, dept_id, offset, size):
        """
        获取部门中的用户列表详细清单
        :param dept_id: 部门ID
        :param offset:  偏移量（可理解为步进量）
        :param size: 一次查询多少个
        :return:
        """
        return self.ding_client_connect.user.list(department_id=dept_id, offset=offset, size=size)

    def ding_get_union_id_by_code(self, code):
        """
        通过移动应用接入扫码返回的临时授权码，获取用户的unionid
        :param code:
        :return:
        """
        # token = self.ding_get_access_token
        time_stamp = int(round(time.time() * 1000))
        # 时间戳
        # 通过appSecret计算出来的签名值，该参数值在HTTP请求参数中需要urlEncode(因为签名中可能包含特殊字符+)。
        signature = quote(base64.b64encode(hmac.new(
            self.mo_app_secret.encode('utf-8'),
            str(time_stamp).encode('utf-8'),
            digestmod=sha256).digest()).decode("utf-8"))
        # accessKey 是 登录开发者后台，选择应用开发 > 移动接入应用 > 登录所看到应用的appId。
        url = '{}/sns/getuserinfo_bycode?accessKey={}&signature={}&timestamp={}'.format(DING_URL, self.mo_app_id, signature, time_stamp)
        resp = requests.post(
            url=url,
            json=dict(tmp_auth_code=code),
        )
        resp = resp.json()
        print(resp)
        try:
            if resp['errcode'] != 0:
                return False, 'ding_get_union_id_by_code: %s' % str(resp)
            else:
                return True, resp["user_info"]["unionid"]
        except Exception:
            return False, 'ding_get_union_id_by_code: %s' % str(resp)

    def ding_get_userid_by_union_id(self, union_id):
        """
        通过unionid获取用户的userid
        :param union_id:  用户在当前钉钉开放平台账号范围内的唯一标识
        :return:
        """
        try:
            return True, self.ding_client_connect.user.get_userid_by_unionid(union_id)['userid']
        except Exception as e:
            return False, 'ding_get_union_id_by_code: %s' % str(e)

        except (KeyError, IndexError) as k_error:
            return False, 'ding_get_union_id_by_code: %s' % str(k_error)

    @property
    def ding_get_org_user_count(self):
        """
        企业员工数量
        only_active – 是否包含未激活钉钉的人员数量
        :return:
        """
        return self.ding_client_connect.user.get_org_user_count('only_active')

    def ding_get_userinfo_detail(self, user_id):
        """
        通过user_id 获取用户详细信息
        user_id –  用户ID
        :return:
        """
        try:
            return True, self.ding_client_connect.user.get(user_id)
        except Exception as e:
            return False, 'ding_get_union_id_by_code: %s' % str(e)

        except (KeyError, IndexError) as k_error:
            return False, 'ding_get_union_id_by_code: %s' % str(k_error)


if __name__ == '__main__':
    start = time.time()
    d = DingDingOps().ding_client_connect
    unicode = ''
    # print(d.)
    end = time.time()
    print("running:" + str(round((end - start), 3)))
