#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @FileName：     feishu_ops.py
# @Software:      
# @Author:         Leven Xiang
# @Mail:           xiangle0109@outlook.com
# @Date：          2021/5/20 15:28
from __future__ import absolute_import, unicode_literals

import os

from utils.feishu import OpenLark as FeiShu
from utils.storage.memorystorage import MemoryStorage
from pwdselfservice import cache_storage
from utils.feishu.helper import to_native

APP_ENV = os.getenv('APP_ENV')
if APP_ENV == 'dev':
    from conf.local_settings_dev import *
else:
    from conf.local_settings import *


class FeiShuOps(FeiShu):
    def __init__(self, corp_id=None, app_id=FEISHU_APP_ID, app_secret=FEISHU_APP_SECRET, token_store=cache_storage):
        super().__init__(app_id, app_secret)
        self.corp_id = corp_id
        self.app_id = app_id
        self.app_secret = app_secret
        self.token_store = token_store or MemoryStorage()
        self.token_store.prefix = "feishu:%s" % ("app_id:%s" % self.app_id)

    @property
    def app_access_token(self):
        """
        重写app_access_token，使用自己的token_storage
        """
        key_app_access_token = 'app_token'.format(self.app_id)

        cache_token = self.token_store.get(key_app_access_token)
        if cache_token:
            return to_native(cache_token)

        body = {
            'app_id': self.app_id,
            'app_secret': self.app_secret
        }
        if self.is_isv:
            url = self._gen_request_url('/open-apis/auth/v3/app_access_token/')
            body['app_ticket'] = self.app_ticket
        else:
            url = self._gen_request_url('/open-apis/auth/v3/app_access_token/internal/')

        res = self._post(url, body)
        app_access_token = res['app_access_token']
        expire = res['expire']

        if expire <= 360:
            return app_access_token

        self.token_store.set(key_app_access_token, app_access_token, expire - 100)
        return app_access_token


if __name__ == '__main__':
    fs = FeiShuOps()
    print(fs.get_user(user_id='4g924c3b'))

