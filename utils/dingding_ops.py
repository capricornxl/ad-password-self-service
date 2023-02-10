# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk.client import AppKeyClient
from pwdselfservice import cache_storage

import os

APP_ENV = os.getenv('APP_ENV')

if APP_ENV == 'dev':
    from conf.local_settings_dev import *
else:
    from conf.local_settings import *


class DingDingOps(AppKeyClient):
    def __init__(self, corp_id=DING_CORP_ID, app_key=DING_APP_KEY, app_secret=DING_APP_SECRET, mo_app_id=DING_MO_APP_ID,
                 mo_app_secret=DING_MO_APP_SECRET,
                 storage=cache_storage):
        super().__init__(corp_id, app_key, app_secret, storage)
        self.corp_id = corp_id
        self.app_key = app_key
        self.app_secret = app_secret
        self.mo_app_id = mo_app_id
        self.mo_app_secret = mo_app_secret
        self.storage = storage

    def get_user_id_by_code(self, code):
        """
        通过code获取用户的 userid
        :return:
        """
        user_id_data = self.user.getuserinfo(code)
        if user_id_data.get('errcode') == 0:
            user_id = user_id_data.get('userid')
            return True, user_id
        else:
            return False, '通过临时Code换取用户ID失败: %s' % str(user_id_data)

    def get_user_detail_by_user_id(self, user_id):
        """
        通过user_id 获取用户详细信息
        user_id –  用户ID
        :return:
        """
        try:
            return True, self.user.get(user_id)
        except Exception as e:
            return False, 'get_user_detail_by_user_id: %s' % str(e)

        except (KeyError, IndexError) as k_error:
            return False, 'get_user_detail_by_user_id: %s' % str(k_error)

    def get_user_detail(self, code, home_url):
        """
        临时授权码换取userinfo
        """
        _status, user_id = self.get_user_id_by_code(code)
        # 判断 user_id 在本企业钉钉/微信中是否存在
        if not _status:
            context = {
                'global_title': TITLE,
                'msg': '获取userid失败，错误信息：{}'.format(user_id),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return False, context, user_id
        detail_status, user_info = self.get_user_detail_by_user_id(user_id)
        if not detail_status:
            context = {
                'global_title': TITLE,
                'msg': '获取用户信息失败，错误信息：{}'.format(user_info),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return False, context, user_info
        return True, user_id, user_info
