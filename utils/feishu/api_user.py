# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, List

from utils.feishu.dt_code import SimpleUser, User
from utils.feishu.dt_help import make_datatype
from utils.feishu.exception import LarkInvalidArguments
from utils.feishu.helper import pop_or_none

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIUserMixin(object):
    def get_user(self, open_id='', user_id=''):
        """获取用户信息

        :type self: OpenLark
        :param open_id: 用户的 open_id
        :type open_id: str
        :param user_id: 用户的 user_id
        :type user_id: str
        :return: User 对象
        :rtype: User

        https://open.feishu.cn/document/ukTMukTMukTM/ukjMwUjL5IDM14SOyATN
        """
        if open_id:
            url = self._gen_request_url('/open-apis/user/v3/info?open_id={}'.format(open_id))
        elif user_id:
            url = self._gen_request_url('/open-apis/user/v3/info?employee_id={}'.format(user_id))
        else:
            raise LarkInvalidArguments(msg='[get_user] empty open_id and user_id')

        res = self._get(url, with_tenant_token=True)
        res['user_id'] = pop_or_none(res, 'employee_id')
        return make_datatype(User, res)

    def get_users_by_mobile_email(self, emails=None, mobiles=None):
        """获取用户信息

        :type self: OpenLark
        :param emails: 邮箱列表
        :type emails: list[str]
        :param mobiles: 手机列表
        :type mobiles: list[str]
        :return: 邮箱的用户字典，邮箱不存在的列表，手机的用户字典，手机不存在的列表
        :rtype: (dict[str, list[SimpleUser]], list[str], dict[str, list[SimpleUser]], list[str])

        根据用户邮箱或手机号查询用户 open_id 和 user_id，支持批量查询。

        只能查询到应用可用性范围内的用户 ID。

        调用该接口需要具有 “获取用户 ID” 权限。

        https://open.feishu.cn/document/ukTMukTMukTM/uUzMyUjL1MjM14SNzITN
        """

        qs = '&'.join(['mobiles=' + i for i in (mobiles or [])] + ['emails=' + i for i in (emails or [])])
        url = self._gen_request_url('/open-apis/user/v1/batch_get_id?' + qs)

        res = self._get(url, with_tenant_token=True)
        data = res['data']
        email_users = data.get('email_users', {})
        email_users = {k: [make_datatype(SimpleUser, vv) for vv in v] for k, v in
                       email_users.items()}  # type: dict[str, List[SimpleUser]]
        emails_not_exist = data.get('emails_not_exist', [])  # type: List[str]
        mobile_users = data.get('mobile_users', {})
        mobile_users = {k: [make_datatype(SimpleUser, vv) for vv in v] for k, v in
                        mobile_users.items()}  # type: dict[str, List[SimpleUser]]
        mobiles_not_exist = data.get('mobiles_not_exist', [])  # type: List[str]
        return email_users, emails_not_exist, mobile_users, mobiles_not_exist
