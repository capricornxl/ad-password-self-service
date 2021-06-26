# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from utils.feishu.dt_code import OAuthCodeToSessionResp, User
from utils.feishu.dt_help import make_datatype

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIOAuthMixin(object):
    def gen_oauth_url(self, state=''):
        """生成 OAuth 授权链接，请求身份验证

        :type self: OpenLark
        :param state: 用来维护请求和回调状态的附加字符串，在授权完成回调时会附加此参数，
                      应用可以根据此字符串来判断上下文关系
        :return: 跳转链接
        :rtype: str

        应用请求用户身份验证时，需按如下方式构造登录链接，并跳转至此链接。飞书客户端内用户免登，系统浏览器内用户需完成扫码登录。

        特别需要注意的是：老 api 获取的 expire_in 是时间戳，新 api 获取的 expire_in 是秒数

        https://open.feishu.cn/document/ukTMukTMukTM/ukzN4UjL5cDO14SO3gTN
        """
        url = '/open-apis/authen/v1/index?redirect_uri={}&app_id={}&state={}'

        return self._gen_request_url(url.format(self.oauth_redirect_uri, self.app_id, state))

    def oauth_code_2_session(self, code):
        """获取登录用户身份

        :type self: OpenLark
        :param code: 扫码登录后会自动 302 到 redirect_uri 并带上此参数
        :type code: str
        :return: OAuthCodeToSessionResp
        :rtype: OAuthCodeToSessionResp

        Web 扫码后拿到的 code 换取用户信息，通过此接口获取登录用户身份。

        特别需要注意的是：老 api 获取的 expire_in 是时间戳，新 api 获取的 expire_in 是秒数

        https://open.feishu.cn/document/ukTMukTMukTM/uEDO4UjLxgDO14SM4gTN
        """
        url = self._gen_request_url('/open-apis/authen/v1/access_token')

        body = {
            'app_access_token': self.app_access_token,
            'grant_type': 'authorization_code',
            'code': code,
        }
        res = self._post(url, body)

        return make_datatype(OAuthCodeToSessionResp, res.get('data') or {})

    def refresh_user_session(self, refresh_token):
        """刷新用户扫码登录后获取的 access_token

        :type self: OpenLark
        :param refresh_token: 扫码登录后会拿到这个值
        :type refresh_token: str
        :return: OAuthCodeToSessionResp
        :rtype: OAuthCodeToSessionResp

        刷新用户 token

        特别需要注意的是：老 api 获取的 expire_in 是时间戳，新 api 获取的 expire_in 是秒数

        https://open.feishu.cn/document/ukTMukTMukTM/uQDO4UjL0gDO14CN4gTN
        """
        url = self._gen_request_url('/open-apis/authen/v1/refresh_access_token')

        body = {
            "app_access_token": self.app_access_token,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        res = self._post(url, body)

        return make_datatype(OAuthCodeToSessionResp, res.get('data') or {})

    def oauth_get_user(self, user_access_token):
        """获取用户信息

        :type self: OpenLark
        :param user_access_token:

        此接口仅用于获取登录用户的信息。 调用此接口需要在 Header 中带上 user_access_token。

        https://open.feishu.cn/document/ukTMukTMukTM/uIDO4UjLygDO14iM4gTN
        """
        url = self._gen_request_url('/open-apis/authen/v1/user_info')
        res = self._get(url, auth_token=user_access_token)
        data = res['data']

        data['avatar_url'] = data.get('avatar') or data.get('avatar_url')
        data['user_id'] = data.get('user_id') or data.get('employee_id')
        return make_datatype(User, data)
