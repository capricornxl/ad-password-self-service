# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from utils.feishu.dt_code import MinaCodeToSessionResp
from utils.feishu.dt_help import make_datatype

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIMinaMixin(object):
    def mina_code_2_session(self, code):
        """通过login接口获取到登录凭证后，开发者可以通过服务器发送请求的方式获取 session_key 和 openId 等

        :type self: OpenLark
        :param code: 登录时获取的 code
        :type code: str
        :return: MinaCodeToSessionResp
        :type: MinaCodeToSessionResp
        :rtype MinaCodeToSessionResp

        https://open.feishu.cn/document/ukTMukTMukTM/ukjM04SOyQjL5IDN
        """
        hosts = {
            1: 'https://mina.bytedance.com/openapi/tokenLoginValidate',
            0: 'https://mina-staging.bytedance.net/openapi/tokenLoginValidate',
        }
        url = hosts[int(not self.is_staging)]
        app_access_token = self.app_access_token

        body = {'token': app_access_token, 'code': code}
        res = self._post(url, body)

        return make_datatype(MinaCodeToSessionResp, res)
