# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging
import time
from typing import Any, Callable, Optional

import requests
from six import string_types

from utils.feishu.api_app_link import APIAppLinkMixin
from utils.feishu.api_application import APIApplicationMixin
from utils.feishu.api_approval import APIApprovalMixin
from utils.feishu.api_bot import APIBotMixin
from utils.feishu.api_calendar import APICalendarMixin
from utils.feishu.api_callback import APICallbackMixin
from utils.feishu.api_chat import APIChatMixin
from utils.feishu.api_contact import APIContactMixin
from utils.feishu.api_drive_comment import APIDriveCommentMixin
from utils.feishu.api_drive_doc import APIDriveDocMixin
from utils.feishu.api_drive_file import APIDriveFileMixin
from utils.feishu.api_drive_folder import APIDriveFolderMixin
from utils.feishu.api_drive_permission import APIDrivePermissionMixin
from utils.feishu.api_drive_sheet import APIDriveSheetMixin
from utils.feishu.api_drive_suite import APIDriveSuiteMixin
from utils.feishu.api_duty import APIDutyMixin
from utils.feishu.api_file import APIFileMixin
from utils.feishu.api_id import APIIDMixin
from utils.feishu.api_image import APIImageMixin
from utils.feishu.api_meeting_room import APIMeetingRoomMixin
from utils.feishu.api_message import APIMessageMixin
from utils.feishu.api_mina import APIMinaMixin
from utils.feishu.api_oauth import APIOAuthMixin
from utils.feishu.api_pay import APIPayMixin
from utils.feishu.api_user import APIUserMixin
from utils.feishu.exception import LarkGetAppTicketFail, LarkInvalidArguments, LarkUnknownError, gen_exception
from utils.feishu.helper import to_native
from utils.feishu.internal_cache import _Cache

logger = logging.getLogger('feishu')


def _gen_default_token_getter_setter():
    cache = _Cache(maxsize=1024, ttl=3600)

    def _getter(key):
        return cache.get(key=key)

    def _setter(key, value, ttl):
        cache.set(key=key, value=value, ttl=ttl)

    return _getter, _setter


class OpenLark(APIIDMixin,
               APIMinaMixin,
               APIImageMixin,
               APIFileMixin,
               APIMessageMixin,
               APIUserMixin,
               APIBotMixin,
               APIChatMixin,
               APICallbackMixin,
               APIContactMixin,
               APIOAuthMixin,
               APIApprovalMixin,
               APICalendarMixin,
               APIApplicationMixin,
               APIMeetingRoomMixin,
               APIPayMixin,
               APIDutyMixin,
               APIAppLinkMixin,
               APIDriveFolderMixin,
               APIDriveFileMixin,
               APIDriveDocMixin,
               APIDriveCommentMixin,
               APIDriveSuiteMixin,
               APIDriveSheetMixin,
               APIDrivePermissionMixin):
    __app_access_token = ''
    __app_access_token_expire = 0
    __tenant_access_token = ''
    __tenant_access_token_expire = 0
    __key_app_ticket = ''
    __token_setter = None  # type: Callable[[str, str, int], Any]
    __token_getter = None  # type: Callable[[str], Optional[str]]
    is_isv = False
    tenant_key = ''  # type: string_types

    def __init__(self, app_id,
                 app_secret,
                 encrypt_key=None,
                 verification_token='',
                 oauth_redirect_uri='',
                 token_setter=None,
                 token_getter=None,
                 is_isv=False,
                 is_lark=False,
                 tenant_key='',
                 is_staging=False,
                 ignore_ssl=False):
        """构造 OpenLark

        :param app_id: 应用唯一的 ID 标识
        :type app_id: string_types
        :param app_secret: 应用的秘钥，创建 App 的时候由平台生成
        :type app_secret: string_types
        :param encrypt_key: 应用的 AppID，
        :type encrypt_key: string_types
        :param verification_token: 用于验证回调是否是开放平台发送的
        :type verification_token: string_types
        :param oauth_redirect_uri: 用于 OAuth 登录的重定向地址
        :type oauth_redirect_uri: string_types
        :param token_setter: 用于分布式设置 token
        :type token_setter: Callable[[str, str, int], Any]
        :param token_getter: 用于分布式获取 token
        :type token_getter: Callable[[str], Optional[Union[str, bytes]]]
        :param is_isv: 指定本实例是否是 ISV 应用，在获取 tenant_access_token 的时候会使用不同的参数
        :type is_isv: bool
        :param tenant_key: 租户的唯一 ID，如果实例是 ISV 应用，必须指定本参数，在获取 tenant_access_token 的时候会使用不同的参数
        :type tenant_key: string_types
        :param is_staging: 是否是 staging 环境
        :param ignore_ssl: 忽略 ssl
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.oauth_redirect_uri = oauth_redirect_uri
        self.encrypt_key = encrypt_key  # 解密回调数据
        self.verification_token = verification_token  # 回调的时候会有这个字段，校验一致性
        self.is_isv = is_isv  # 是否是 ISV 应用
        self.is_lark = is_lark  # 是 Lark 还是飞书
        self.tenant_key = tenant_key  # 租户 key
        self.is_staging = is_staging
        self.ignore_ssl = ignore_ssl
        self.__key_app_ticket = 'feishu:{}:app_ticket'.format(app_id)

        if is_isv and not tenant_key:
            # 在一开始的时候，是不知道 tenant_key 是多少的，又依赖本库解析参数，所以可以先不设置
            logger.warning('[init_class] 设置 is_isv 的时候，没有设置 tenant_key')

        # 数据是一份的，所以必须同时有或者没有
        if (token_getter and not token_setter) or (not token_getter and token_setter):
            raise LarkInvalidArguments(msg='token_getter / token_setter 必须同时设置或者不设置')

        if not token_setter:
            token_getter, token_setter = _gen_default_token_getter_setter()
        self.__token_getter = token_getter
        self.__token_setter = token_setter

    def _gen_open_exception(self, url, res):
        try:
            msg = res.get('msg') or res.get('message')
            if msg is None:
                if 'code' in res:
                    del res['code']
                if 'error' in res:
                    del res['error']
                msg = json.dumps(res)
        except AttributeError:
            msg = json.dumps(res)

        try:
            code = res.get('code')
            if code is None:
                code = res.get('error')
            if code is None:
                code = LarkUnknownError.code
        except AttributeError:
            code = LarkUnknownError.code

        exception = gen_exception(code, url, msg)
        logger.error('[exception] code=%d, url=%s, msg=%s exception=%s', code, url, msg, exception)
        return exception

    def _base_request(self, method,
                      url,
                      body=None,
                      files=None,
                      with_app_token=False,
                      with_tenant_token=False,
                      auth_token='',
                      raw_content=False,
                      success_code=0):
        headers = {}
        if with_tenant_token:
            token = self.tenant_access_token
            headers['Authorization'] = 'Bearer {}'.format(token)
        elif with_app_token:
            token = self.app_access_token
            headers['Authorization'] = 'Bearer {}'.format(token)
        elif auth_token:
            headers['Authorization'] = 'Bearer {}'.format(auth_token)

        verify = not self.ignore_ssl
        if files and body:
            r = requests.request(method=method, data=body, url=url, files=files, headers=headers, verify=verify)
        elif files:
            r = requests.request(method=method, url=url, files=files, headers=headers, verify=verify)
        elif body:
            headers['Content-Type'] = 'application/json'
            r = requests.request(method=method, url=url, json=body, headers=headers, verify=verify)
        else:
            r = requests.request(method=method, url=url, headers=headers, verify=verify)

        if not raw_content:
            logger.debug('[http] method=%s, url=%s, body=%s, files=%s, status_code=%d, res=%s',
                         method, url, body, files, r.status_code, r.content)

        try:
            res = r.json()
        except Exception:
            if raw_content:
                logger.debug('[http] method=%s, url=%s, body=%s, files=%s, status_code=%d, res is raw',
                             method, url, body, files, r.status_code)
                return r.content

            logger.error('[http] method=%s, url=%s, body=%s, files=%s, status_code=%d, res=%s',
                         method, url, body, files, r.status_code, r.text)
            # 为了记录 error 日志，所以原样抛出
            raise

        code = res.get('code')
        if code is not None and isinstance(code, int) and code != success_code:
            # 抛出 OpenLarkException
            raise self._gen_open_exception(url, res)
        error = res.get('error')
        if error is not None and isinstance(error, int) and error != success_code:
            raise self._gen_open_exception(url, {
                'code': error,
                'msg': res.get('message') or res.get('msg') or res.get('BaseResp', {}).get('StatusMessage')
            })

        if raw_content:
            logger.debug('[http] method=%s, url=%s, body=%s, files=%s, status_code=%d, res is raw',
                         method, url, body, files, r.status_code)
            return r.content

        return res

    def _get(self, url, with_tenant_token=False, with_app_token=False, auth_token='', raw_content=False,
             success_code=0):
        return self._base_request('get', url=url,
                                  with_tenant_token=with_tenant_token,
                                  with_app_token=with_app_token,
                                  auth_token=auth_token,
                                  raw_content=raw_content,
                                  success_code=success_code)

    def _delete(self, url, body=None, with_tenant_token=False, auth_token='', raw_content=False, success_code=0):
        return self._base_request('delete', url=url,
                                  body=body,
                                  with_tenant_token=with_tenant_token,
                                  auth_token=auth_token,
                                  raw_content=raw_content,
                                  success_code=success_code)

    def _patch(self, url, body=None, with_app_token=False, with_tenant_token=False, raw_content=False, success_code=0):
        return self._base_request('patch', url=url,
                                  body=body,
                                  with_app_token=with_app_token,
                                  with_tenant_token=with_tenant_token,
                                  raw_content=raw_content,
                                  success_code=success_code)

    def _post(self, url, body=None, files=None, with_app_token=False, with_tenant_token=False, auth_token='',
              success_code=0):
        return self._base_request('post', url=url,
                                  body=body,
                                  files=files,
                                  with_app_token=with_app_token,
                                  with_tenant_token=with_tenant_token,
                                  auth_token=auth_token,
                                  success_code=success_code)

    def _put(self, url, body=None, files=None, with_app_token=False, with_tenant_token=False, auth_token='',
             success_code=0):
        return self._base_request('put', url=url,
                                  body=body,
                                  files=files,
                                  with_app_token=with_app_token,
                                  with_tenant_token=with_tenant_token,
                                  auth_token=auth_token,
                                  success_code=success_code)

    def _gen_request_url(self, path, app='normal'):
        """

        :type self: OpenLark
        :param path:
        :type path: string_types
        :param app:
        :type app: str
        :return:
        """
        hosts = {
            # lark（非中国区）
            1: {
                # online
                1: {
                    'normal': 'https://open.larksuite.com',
                    'approval': 'https://www.larksuite.com',
                },
                # staging
                0: {
                    'normal': 'https://open.larksuite-staging.com',
                    'approval': 'https://www.larksuite-staging.com',
                }
            },

            # 飞书(中国区)
            0: {
                # online
                1: {
                    'normal': 'https://open.feishu.cn',
                    'approval': 'https://www.feishu.cn',
                },
                # staging
                0: {
                    'normal': 'https://open.feishu-staging.cn',
                    'approval': 'https://www.feishu-staging.cn',
                }
            }
        }
        open_feishu_host = hosts[int(self.is_lark)][int(not self.is_staging)][app]

        return open_feishu_host + path

    @property
    def app_access_token(self):
        """获取 app_access_token

        :rtype str

        https://open.feishu.cn/document/ukTMukTMukTM/uADN14CM0UjLwQTN
        """
        key_app_access_token = 'feishu:{}:app_token'.format(self.app_id)

        cache_token = self.__token_getter(key_app_access_token)
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

        self.__token_setter(key_app_access_token, app_access_token, expire - 100)
        return app_access_token

    @property
    def tenant_access_token(self):
        """获取 tenant_access_token

        :rtype str

        注意：如果是 ISV 应用，那么必须在构造 OpenLark 实例的时候，必须传入 is_isv=True 和 tenant_key

        https://open.feishu.cn/document/ukTMukTMukTM/uMjNz4yM2MjLzYzM
        """

        key_token = 'feishu:tenant_token:{}:{}'.format(self.app_id, self.tenant_key)
        cache_token = self.__token_getter(key_token)
        if cache_token:
            return to_native(cache_token)

        if self.is_isv:
            if not self.tenant_key:
                raise LarkInvalidArguments(msg='[tenant_access_token] '
                                               'must set tenant_key for isv app get tenant_access_token')

            body = {
                'app_access_token': self.app_access_token,
                'tenant_key': self.tenant_key,
            }
            url = self._gen_request_url('/open-apis/auth/v3/tenant_access_token/')
        else:
            body = {
                'app_id': self.app_id,
                'app_secret': self.app_secret
            }
            url = self._gen_request_url('/open-apis/auth/v3/tenant_access_token/internal/')

        res = self._post(url, body)
        tenant_access_token = res['tenant_access_token']
        expire = res['expire']

        if expire <= 360:
            return tenant_access_token

        self.__token_setter(key_token, tenant_access_token, expire - 100)
        return tenant_access_token

    def resend_app_ticket(self):
        """重新推送 app_ticket

        飞书每隔 1 小时会给应用推送一次最新的 app_ticket
        应用也可以主动调用此接口，触发飞书进行及时的重新推送，app_ticket 会推送到回调地址
        resend 后，旧的 app_ticket 会在 5-10 分钟内失效

        https://open.feishu.cn/document/ukTMukTMukTM/uQjNz4CN2MjL0YzM
        """
        url = self._gen_request_url('/open-apis/auth/v3/app_ticket/resend/')
        body = {'app_id': self.app_id, 'app_secret': self.app_secret}
        self._post(url, body=body)

    @property
    def app_ticket(self):
        """获取 app_ticket
        """
        if not self.is_isv:
            raise LarkInvalidArguments(msg='[app_ticket] 非 isv 应用无法调用 app_ticket')

        res = self.__token_getter(self.__key_app_ticket)
        if not res:
            logger.warning('[app_ticket] no found, try resend.')
            self.resend_app_ticket()

            for t in range(3):
                sleep_time = 2 ** t
                logger.warning('[app_ticket] had resend, wait to got app_ticket, time=%d, sleep=%d', t + 1, sleep_time)
                time.sleep(sleep_time)
                res = self.__token_getter(self.__key_app_ticket)
                if res:
                    logger.warning('[app_ticket] resend to got app_ticket not found, time=%d', t + 1)
                    break

        if not res:
            raise LarkGetAppTicketFail()

        if not isinstance(res, string_types):
            raise LarkInvalidArguments(
                msg='response of token_getter must be str or bytes, but got {}'.format(type(res)))
        return to_native(res)

    def update_app_ticket(self, app_ticket):
        """设置新的 app_ticket

        :type self: OpenLark
        :param app_ticket 的来源是从回调中获取
        :type app_ticket: string_types
        """
        if callable(self.__token_setter):
            self.__token_setter(self.__key_app_ticket, app_ticket, 3600)
            return
        logger.warning('call update_app_ticket, but token_setter is not callable')
