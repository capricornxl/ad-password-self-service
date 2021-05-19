# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import hmac
import time
from hashlib import sha256
from urllib.parse import quote

import requests
from dingtalk.client import AppKeyClient
from pwdselfservice import cache_storage

from pwdselfservice.local_settings import DING_APP_KEY, DING_APP_SECRET, DING_CORP_ID, DING_URL, DING_MO_APP_ID, DING_MO_APP_SECRET


class DingDingOps(object):
    def __init__(self, corp_id=DING_CORP_ID, app_key=DING_APP_KEY, app_secret=DING_APP_SECRET, mo_app_id=DING_MO_APP_ID, mo_app_secret=DING_MO_APP_SECRET, storage=cache_storage):
        self.corp_id = corp_id
        self.app_key = app_key
        self.app_secret = app_secret
        self.mo_app_id = mo_app_id
        self.mo_app_secret = mo_app_secret
        self.storage = storage

    @property
    def _client_connect(self):
        """
        钉钉连接器
        :return:
        """
        return AppKeyClient(corp_id=self.corp_id, app_key=self.app_key, app_secret=self.app_secret)

    def get_union_id_by_code(self, code):
        """
        通过移动应用接入扫码返回的临时授权码，使用临时授权码换取用户的unionid
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
        try:
            if resp['errcode'] != 0:
                return False, 'get_union_id_by_code: %s' % str(resp)
            else:
                return True, resp["user_info"]["unionid"]
        except Exception:
            return False, 'get_union_id_by_code: %s' % str(resp)

    def get_user_id_by_code(self, code):
        """
        通过code获取用户的userid
        :param id:  用户在当前钉钉开放平台账号范围内的唯一标识
        :return:
        """
        _status, union_id = self.get_union_id_by_code(code)
        if _status:
            return True, self._client_connect.user.get_userid_by_unionid(union_id).get('userid')
        else:
            return False, 'get_user_id_by_code: %s' % str(union_id)

    def get_user_detail_by_user_id(self, user_id):
        """
        通过user_id 获取用户详细信息
        user_id –  用户ID
        :return:
        """
        try:
            return True, self._client_connect.user.get(user_id)
        except Exception as e:
            return False, 'get_user_detail_by_user_id: %s' % str(e)

        except (KeyError, IndexError) as k_error:
            return False, 'get_user_detail_by_user_id: %s' % str(k_error)
