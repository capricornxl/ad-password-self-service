# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Tuple

from utils.feishu.exception import LarkInvalidArguments, OpenLarkException

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


# https://open.feishu.cn/document/ukTMukTMukTM/uIzMxEjLyMTMx4iMzETM

class APIIDMixin(object):
    def email_to_id(self, email):
        """邮箱转 open_id 和 user_id

        :type self: OpenLark
        :param email: 用户的邮箱
        :type email: str
        :return: open_id, user_id
        :rtype: Tuple[str, str]

        根据用户邮箱获取用户 open_id 和 user_id。

        user_id 需要申请 user_id 的权限才能获取到

        https://open.feishu.cn/document/ukTMukTMukTM/uEDMwUjLxADM14SMwATN
        """
        url = self._gen_request_url('/open-apis/user/v3/email2id')
        body = {'email': email}
        res = self._post(url, body, with_tenant_token=True)

        open_id = res.get('open_id', '')  # type: str
        user_id = res.get('employee_id', '')  # type: str
        return open_id, user_id

    def open_id_to_user_id(self, open_id):
        """open_id 转 user_id

        :type self: OpenLark
        :param open_id: open_id
        :type open_id: str
        :return:  user_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/openid2uid/')
        body = {'open_id': open_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('user_id')

    def user_id_to_open_id(self, user_id):
        """user_id 转 open_id

        :type self: OpenLark
        :param user_id: user_id
        :type user_id: str
        :return: open_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/uid2openid/')
        body = {'user_id': user_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('open_id')

    def employee_id_to_user_id(self, employee_id):
        """employee_id 转 user_id

        :type self: OpenLark
        :param employee_id: employee_id
        :type employee_id: str
        :return: user_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/eid2uid/')
        body = {'employee_id': employee_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('user_id')

    def user_id_to_employee_id(self, user_id):
        """user_id 转 employee_id

        :type self: OpenLark
        :param user_id: user_id
        :type user_id: str
        :return: employee_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/uid2eid/')
        body = {'user_id': user_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('employee_id')

    def chat_id_to_open_chat_id(self, chat_id):
        """chat_id 转 open_chat_id

        :type self: OpenLark
        :param chat_id: chat_id
        :type chat_id: str
        :return: open_chat_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/cid2ocid/')
        body = {'chat_id': chat_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('open_chat_id')

    def open_chat_id_to_chat_id(self, open_chat_id):
        """open_chat_id 转 chat_id

        :type self: OpenLark
        :param open_chat_id: open_chat_id
        :type open_chat_id: str
        :return: chat_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/ocid2cid/')
        body = {'open_chat_id': open_chat_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('chat_id')

    def message_id_to_open_message_id(self, message_id):
        """message_id 转 open_message_id

        :type self: OpenLark
        :param message_id: message_id
        :type message_id: str
        :return: open_message_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/mid2omid/')
        body = {'message_id': message_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('open_message_id')

    def open_message_id_to_message_id(self, open_message_id):
        """open_message_id 转 message_id

        :type self: OpenLark
        :param open_message_id: open_message_id
        :type open_message_id: str
        :return: message_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/omid2mid/')
        body = {'open_message_id': open_message_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('message_id')

    def department_id_to_open_department_id(self, department_id):
        """department_id 转 open_department_id

        :type self: OpenLark
        :param department_id: department_id
        :type department_id: str
        :return: open_department_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/did2odid/')
        body = {'department_id': department_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('open_department_id')

    def open_department_id_to_department_id(self, open_department_id):
        """open_department_id 转 department_id

        :type self: OpenLark
        :param open_department_id: open_department_id
        :type open_department_id: str
        :return: department_id
        :rtype: str
        """
        url = self._gen_request_url('/open-apis/exchange/v3/odid2did/')
        body = {'open_department_id': open_department_id}
        res = self._post(url, body, with_tenant_token=True)
        return res.get('department_id')

    def get_chat_id_between_user_bot(self, open_id='', user_id=''):
        """获取机器人和用户的 chat_id

        :type self: OpenLark
        :param open_id: open_id
        :type open_id: str
        :param user_id: user_id
        :return: open_chat_id, chat_id
        :rtype: Tuple[str, str]

        https://lark-open.bytedance.net/document/ukTMukTMukTM/uYjMxEjL2ITMx4iNyETM
        """
        if open_id:
            url = self._gen_request_url('/open-apis/chat/v3/p2p/id?open_id={}'.format(open_id))
        elif user_id:
            url = self._gen_request_url('/open-apis/chat/v3/p2p/id?user_id={}'.format(user_id))
        else:
            raise OpenLarkException(msg='[get_chat_id_between_user_bot] empty open_id and user_id')

        res = self._get(url, with_tenant_token=True)
        open_chat_id = res.get('open_chat_id', '')  # type: str
        chat_id = res.get('chat_id', '')  # type: str
        return open_chat_id, chat_id

    def get_chat_id_between_users(self, to_user_id,
                                  open_id='',
                                  user_id=''):
        """获取用户和用户的之前的 chat_id

        :type self: OpenLark
        :param to_user_id: 到谁的 open_id
        :type to_user_id: str
        :param open_id: 从谁来的 open_id
        :type open_id: str
        :param user_id: 从谁来的 user_id
        :type user_id: str
        :return: 两个人之间的 open_chat_id, chat_id
        :rtype: Tuple[str, str]

        仅头条内部用户可用 需要申请权限才能获取 @fanlv

        open_id 和 user_id 传一个就行

        https://lark-open.bytedance.net/document/ukTMukTMukTM/uYjMxEjL2ITMx4iNyETM

        """
        if open_id:
            url = self._gen_request_url('/open-apis/chat/v3/p2p/id?open_id={}&chatter={}'.format(open_id, to_user_id))
        elif user_id:
            url = self._gen_request_url('/open-apis/chat/v3/p2p/id?user_id={}&chatter={}'.format(user_id, to_user_id))
        else:
            raise LarkInvalidArguments(msg='[get_chat_id_between_users] empty open_id and user_id')

        res = self._get(url, with_tenant_token=True)
        open_chat_id = res.get('open_chat_id', '')  # type: str
        chat_id = res.get('chat_id', '')  # type: str
        return open_chat_id, chat_id
