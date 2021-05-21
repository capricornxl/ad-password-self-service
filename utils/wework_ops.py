#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @FileName：     WEWORK_ops.py
# @Software:      
# @Author:         Leven Xiang
# @Mail:           xiangle0109@outlook.com
# @Date：          2021/5/18 16:55
from __future__ import absolute_import, unicode_literals

import os

from pwdselfservice import cache_storage
from utils.storage.cache import WeWorkCache
from utils.wework_api.abstract_api import *

APP_ENV = os.getenv('APP_ENV')
if APP_ENV == 'dev':
    from conf.local_settings_dev import *
else:
    from conf.local_settings import *

CORP_API_TYPE = {
    'GET_ACCESS_TOKEN': ['/cgi-bin/gettoken', 'GET'],
    'USER_CREATE': ['/cgi-bin/user/create?access_token=ACCESS_TOKEN', 'POST'],
    'USER_GET': ['/cgi-bin/user/get?access_token=ACCESS_TOKEN', 'GET'],
    'USER_UPDATE': ['/cgi-bin/user/update?access_token=ACCESS_TOKEN', 'POST'],
    'USER_DELETE': ['/cgi-bin/user/delete?access_token=ACCESS_TOKEN', 'GET'],
    'USER_BATCH_DELETE': ['/cgi-bin/user/batchdelete?access_token=ACCESS_TOKEN', 'POST'],
    'USER_SIMPLE_LIST': ['/cgi-bin/user/simplelist?access_token=ACCESS_TOKEN', 'GET'],
    'USER_LIST': ['/cgi-bin/user/list?access_token=ACCESS_TOKEN', 'GET'],
    'USERID_TO_OPENID': ['/cgi-bin/user/convert_to_openid?access_token=ACCESS_TOKEN', 'POST'],
    'OPENID_TO_USERID': ['/cgi-bin/user/convert_to_userid?access_token=ACCESS_TOKEN', 'POST'],
    'USER_AUTH_SUCCESS': ['/cgi-bin/user/authsucc?access_token=ACCESS_TOKEN', 'GET'],

    'DEPARTMENT_CREATE': ['/cgi-bin/department/create?access_token=ACCESS_TOKEN', 'POST'],
    'DEPARTMENT_UPDATE': ['/cgi-bin/department/update?access_token=ACCESS_TOKEN', 'POST'],
    'DEPARTMENT_DELETE': ['/cgi-bin/department/delete?access_token=ACCESS_TOKEN', 'GET'],
    'DEPARTMENT_LIST': ['/cgi-bin/department/list?access_token=ACCESS_TOKEN', 'GET'],

    'TAG_CREATE': ['/cgi-bin/tag/create?access_token=ACCESS_TOKEN', 'POST'],
    'TAG_UPDATE': ['/cgi-bin/tag/update?access_token=ACCESS_TOKEN', 'POST'],
    'TAG_DELETE': ['/cgi-bin/tag/delete?access_token=ACCESS_TOKEN', 'GET'],
    'TAG_GET_USER': ['/cgi-bin/tag/get?access_token=ACCESS_TOKEN', 'GET'],
    'TAG_ADD_USER': ['/cgi-bin/tag/addtagusers?access_token=ACCESS_TOKEN', 'POST'],
    'TAG_DELETE_USER': ['/cgi-bin/tag/deltagusers?access_token=ACCESS_TOKEN', 'POST'],
    'TAG_GET_LIST': ['/cgi-bin/tag/list?access_token=ACCESS_TOKEN', 'GET'],

    'BATCH_JOB_GET_RESULT': ['/cgi-bin/batch/getresult?access_token=ACCESS_TOKEN', 'GET'],

    'BATCH_INVITE': ['/cgi-bin/batch/invite?access_token=ACCESS_TOKEN', 'POST'],

    'AGENT_GET': ['/cgi-bin/agent/get?access_token=ACCESS_TOKEN', 'GET'],
    'AGENT_SET': ['/cgi-bin/agent/set?access_token=ACCESS_TOKEN', 'POST'],
    'AGENT_GET_LIST': ['/cgi-bin/agent/list?access_token=ACCESS_TOKEN', 'GET'],

    'MENU_CREATE': ['/cgi-bin/menu/create?access_token=ACCESS_TOKEN', 'POST'],
    'MENU_GET': ['/cgi-bin/menu/get?access_token=ACCESS_TOKEN', 'GET'],
    'MENU_DELETE': ['/cgi-bin/menu/delete?access_token=ACCESS_TOKEN', 'GET'],

    'MESSAGE_SEND': ['/cgi-bin/message/send?access_token=ACCESS_TOKEN', 'POST'],
    'MESSAGE_REVOKE': ['/cgi-bin/message/revoke?access_token=ACCESS_TOKEN', 'POST'],

    'MEDIA_GET': ['/cgi-bin/media/get?access_token=ACCESS_TOKEN', 'GET'],

    'GET_USER_INFO_BY_CODE': ['/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN', 'GET'],
    'GET_USER_DETAIL': ['/cgi-bin/user/getuserdetail?access_token=ACCESS_TOKEN', 'POST'],

    'GET_TICKET': ['/cgi-bin/ticket/get?access_token=ACCESS_TOKEN', 'GET'],
    'GET_JSAPI_TICKET': ['/cgi-bin/get_jsapi_ticket?access_token=ACCESS_TOKEN', 'GET'],

    'GET_CHECKIN_OPTION': ['/cgi-bin/checkin/getcheckinoption?access_token=ACCESS_TOKEN', 'POST'],
    'GET_CHECKIN_DATA': ['/cgi-bin/checkin/getcheckindata?access_token=ACCESS_TOKEN', 'POST'],
    'GET_APPROVAL_DATA': ['/cgi-bin/corp/getapprovaldata?access_token=ACCESS_TOKEN', 'POST'],

    'GET_INVOICE_INFO': ['/cgi-bin/card/invoice/reimburse/getinvoiceinfo?access_token=ACCESS_TOKEN', 'POST'],
    'UPDATE_INVOICE_STATUS':
        ['/cgi-bin/card/invoice/reimburse/updateinvoicestatus?access_token=ACCESS_TOKEN', 'POST'],
    'BATCH_UPDATE_INVOICE_STATUS':
        ['/cgi-bin/card/invoice/reimburse/updatestatusbatch?access_token=ACCESS_TOKEN', 'POST'],
    'BATCH_GET_INVOICE_INFO':
        ['/cgi-bin/card/invoice/reimburse/getinvoiceinfobatch?access_token=ACCESS_TOKEN', 'POST'],

    'APP_CHAT_CREATE': ['/cgi-bin/appchat/create?access_token=ACCESS_TOKEN', 'POST'],
    'APP_CHAT_GET': ['/cgi-bin/appchat/get?access_token=ACCESS_TOKEN', 'GET'],
    'APP_CHAT_UPDATE': ['/cgi-bin/appchat/update?access_token=ACCESS_TOKEN', 'POST'],
    'APP_CHAT_SEND': ['/cgi-bin/appchat/send?access_token=ACCESS_TOKEN', 'POST'],

    'MINIPROGRAM_CODE_TO_SESSION_KEY': ['/cgi-bin/miniprogram/jscode2session?access_token=ACCESS_TOKEN', 'GET'],
}


class WeWorkOps(AbstractApi):
    def __init__(self, corp_id=WEWORK_CORP_ID, agent_id=WEWORK_AGENT_ID, agent_secret=WEWORK_AGNET_SECRET, storage=cache_storage, prefix='wework'):
        super().__init__()
        self.corp_id = corp_id
        self.agent_id = agent_id
        self.agent_secret = agent_secret
        self.storage = storage
        self.cache = WeWorkCache(self.storage, "%s:%s" % (prefix, "corp_id:%s" % self.corp_id))

    def access_token(self):
        access_token = self.cache.access_token.get()
        if access_token is None:
            ret = self.get_access_token()
            access_token = ret['access_token']
            expires_in = ret.get('expires_in', 7200)
            self.cache.access_token.set(value=access_token, ttl=expires_in)
        return access_token

    def get_access_token(self):
        return self.http_call(
            CORP_API_TYPE['GET_ACCESS_TOKEN'],
            {
                'corpid': self.corp_id,
                'corpsecret': self.agent_secret,
            })

    def get_user_id_by_code(self, code):
        try:
            return True, self.http_call(
                CORP_API_TYPE['GET_USER_INFO_BY_CODE'],
                {
                    'code': code,
                }).get('UserId')
        except ApiException as e:
            return False, "get_user_id_by_code: {}-{}".format(e.errCode, e.errMsg)
        except Exception as e:
            return False, "get_user_id_by_code: {}".format(e)

    def get_user_detail_by_user_id(self, user_id):
        try:
            return True, self.http_call(
                CORP_API_TYPE['USER_GET'],
                {
                    'userid': user_id,
                })
        except ApiException as e:
            return False, "get_user_detail_by_user_id: {}-{}".format(e.errCode, e.errMsg)
        except Exception as e:
            return False, "get_user_detail_by_user_id: {}".format(e)


if __name__ == '__main__':
    wx = WeWorkOps()
    print(wx.get_user_detail_by_user_id('XiangLe'))
