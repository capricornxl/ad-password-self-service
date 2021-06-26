# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from utils.feishu.dt_code import Chat, DetailChat
from utils.feishu.dt_help import make_datatype
from utils.feishu.exception import LarkInvalidArguments

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark
    from six import string_types


class APIChatMixin(object):
    def get_chat_info(self, chat_id):
        """获取会话信息，包括和机器人的私聊 + 群聊

        :type self: OpenLark
        :param chat_id: 会话的 ID
        :type chat_id str
        :return: 会话信息
        :rtype: DetailChat

        获取群名称、群主 ID、成员列表 ID 等群基本信息。

        https://open.feishu.cn/document/ukTMukTMukTM/uMTO5QjLzkTO04yM5kDN
        """
        url = self._gen_request_url('/open-apis/chat/v4/info/?chat_id=' + chat_id)
        res = self._get(url, with_tenant_token=True)
        chat = res['data']
        return make_datatype(DetailChat, chat)

    def get_chat_list_of_bot(self, page_size=100, page_token=None):
        """获取机器人所在的群列表

        :type self: OpenLark
        :param page_size: 分页大小，最大支持 200；默认为 100
        :type page_size: int
        :param page_token: 分页标记，分页查询还有更多群时会同时返回新的 page_token, 下次遍历可采用该 page_token 获取更多
        :type page_token:str
        :return: 有更多群， 下次分页的参数，群的列表
        :rtype: Tuple[bool, str, List[Chat]]

        获取机器人所在的群列表。

        https://open.feishu.cn/document/ukTMukTMukTM/uITO5QjLykTO04iM5kDN
        """
        url = self._gen_request_url('/open-apis/chat/v4/list?page_size={}'.format(page_size))
        if page_token:
            url = '{}&page_token={}'.format(url, page_token)
        res = self._get(url, with_tenant_token=True)
        data = res['data']
        has_more = data.get('has_more')  # type: bool
        page_token = data.get('page_token')  # type: str
        chats = [make_datatype(Chat, i) for i in data.get('groups', [])]
        return has_more, page_token, chats

    def get_chat_list_of_user(self, user_access_token, query_key=None, page_size=100, page_token=None):
        """获取用户所在的群列表

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param query_key: 搜索的关键词
        :type query_key: str
        :param page_size: 分页大小，最大支持 200；默认为 100
        :type page_size: int
        :param page_token: 分页标记，分页查询还有更多群时会同时返回新的 page_token, 下次遍历可采用该 page_token 获取更多群
        :type page_token:
        :return: 有更多群， 下次分页的参数，群的列表
        :rtype: (bool, str, list[Chat])

        获取用户所在的群列表：https://open.feishu.cn/document/ukTMukTMukTM/uQzMwUjL0MDM14CNzATN

        搜索用户所在的群列表：https://open.feishu.cn/document/ukTMukTMukTM/uUTOyUjL1kjM14SN5ITN
        """
        if query_key:
            url = self._gen_request_url('/open-apis/chat/v4/search?page_size={}'.format(page_size))
        else:
            url = self._gen_request_url('/open-apis/user/v4/group_list?page_size={}'.format(page_size))

        if page_token:
            url = '{}&page_token={}'.format(url, page_token)
        if query_key:
            url = '{}&query={}'.format(url, query_key)

        res = self._get(url, auth_token=user_access_token)

        data = res['data']
        has_more = data.get('has_more')
        page_token = data.get('page_token')
        chats = [make_datatype(Chat, i) for i in data.get('groups', [])]
        return has_more, page_token, chats

    def create_chat(self,
                    open_ids=None,
                    user_ids=None,
                    name=None,
                    description=None,
                    en_name=None,
                    ja_name=None):
        """机器人创建群并拉用户进群

        :type self: OpenLark
        :param open_ids: 成员 open_id 列表
        :type open_ids: list[str]
        :param user_ids: 成员 user_id 列表
        :type user_ids: list[str]
        :param name: 群的名称
        :type name: str
        :param description: 群描述
        :type description: str
        :param en_name: 群的英文名称
        :type en_name: str
        :param ja_name: 群的日文名称
        :type ja_name: str
        :return: open_chat_id, invalid_open_ids, invalid_user_ids
        :rtype: Tuple[str, list[str], list[str]]

        https://open.feishu.cn/document/ukTMukTMukTM/ukDO5QjL5gTO04SO4kDN
        """
        if not open_ids and not user_ids:
            raise LarkInvalidArguments(msg='open_ids or user_ids cannot empty')

        url = self._gen_request_url('/open-apis/chat/v4/create/')
        body = {}  # type: Dict[string_types, Any]
        if open_ids:
            body['open_ids'] = open_ids
        if user_ids:
            body['user_ids'] = user_ids
        if name:
            body['name'] = name
        if description:
            body['description'] = description
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if en_name or ja_name:
            body['i18n_names'] = {
                "zh_cn": name,
                "en_us": en_name,
                'ja_jp': ja_name,
            }

        res = self._post(url, body, with_tenant_token=True)
        data = res['data']
        open_chat_id = data.get('chat_id', '')  # type: str
        invalid_open_ids = data.get('invalid_open_ids', [])  # type: List[str]
        invalid_user_ids = data.get('invalid_user_ids', [])  # type: List[str]

        return open_chat_id, invalid_open_ids, invalid_user_ids

    def update_chat_info(self,
                         chat_id,
                         owner_user_id=None,
                         owner_open_id=None,
                         name=None,
                         en_name=None,
                         ja_name=None):
        """更新群信息

        :type self: OpenLark
        :param chat_id: 群 ID
        :type chat_id: str
        :param owner_user_id: 群主的 open_id
        :type owner_user_id: str
        :param owner_open_id: 群主的 user_id
        :type owner_open_id: str
        :param name: 群的名称
        :type name: str
        :param en_name: 群的英文名称
        :type en_name: str
        :param ja_name: 群的日文名称
        :type ja_name: str
        :return: open_chat_id, invalid_open_ids, invalid_user_ids
        :rtype: Tuple[str, list[str], list[str]]

        更新群名称、转让群主等。

        https://open.feishu.cn/document/ukTMukTMukTM/uYTO5QjL2kTO04iN5kDN
        """
        url = self._gen_request_url('/open-apis/chat/v4/update/')
        body = {
            'chat_id': chat_id,
        }  # type: Dict[string_types, Any]
        if owner_user_id:
            body['owner_user_id'] = owner_user_id
        if owner_open_id:
            body['owner_open_id'] = owner_open_id
        if name:
            body['name'] = name
        if name is not None:
            body['name'] = name
        if en_name or ja_name:
            body['i18n_names'] = {
                'zh_cn': name,
                'en_us': en_name,
                'ja_jp': ja_name,
            }

        self._post(url, body, with_tenant_token=True)

    def invite_user_to_chat(self,
                            chat_id,
                            open_ids=None,
                            user_ids=None):
        """机器人拉用户进群

        :type self: OpenLark
        :param chat_id: 群 ID
        :type chat_id: str
        :param open_ids: 需要加入群的用户的 open_id 列表
        :type open_ids: list[str]
        :param user_ids: 需要加入群的用户的 employee_id 列表
        :type user_ids: list[str]
        :return: invalid_open_ids, invalid_user_ids
        :rtype: Tuple[list[str], list[str]]

        机器人拉用户进群，机器人必须在群里

        https://open.feishu.cn/document/ukTMukTMukTM/uMjMxEjLzITMx4yMyETM
        """
        url = self._gen_request_url('/open-apis/chat/v4/chatter/add/')
        if not open_ids and not user_ids:
            raise LarkInvalidArguments(msg='[invite_user_to_chat] empty open_ids and user_ids')
        if not open_ids:
            open_ids = None
        if not user_ids:
            user_ids = None
        body = {'chat_id': chat_id, 'open_ids': open_ids, 'user_ids': user_ids}
        res = self._post(url, body, with_tenant_token=True)
        data = res['data']
        invalid_open_ids = data.get('invalid_open_ids', [])
        invalid_user_ids = data.get('invalid_user_ids', [])
        return invalid_open_ids, invalid_user_ids

    def remove_user_from_chat(self,
                              chat_id,
                              open_ids=None,
                              user_ids=None):
        """机器踢人出群

        :type self: OpenLark
        :param chat_id: 群 ID
        :type chat_id: str
        :param open_ids: 需要踢出群的用户的 open_id 列表
        :type open_ids: list[str]
        :param user_ids: 需要踢出群的用户的 user_ids 列表
        :type user_ids: list[str]
        :return: invalid_open_ids, invalid_employee_ids
        :rtype: Tuple[list[str], list[str]]

        机器人踢用户出群，机器人必须是群主

        https://open.feishu.cn/document/ukTMukTMukTM/uADMwUjLwADM14CMwATN
        """
        if not open_ids and not user_ids:
            raise LarkInvalidArguments(msg='[remove_user_from_chat] empty open_ids and user_ids')

        if not open_ids:
            open_ids = None
        if not user_ids:
            user_ids = None
        url = self._gen_request_url('/open-apis/chat/v4/chatter/delete/')
        body = {'chat_id': chat_id, 'open_ids': open_ids, 'user_ids': user_ids}

        res = self._post(url, body, with_tenant_token=True)
        data = res['data']

        invalid_open_ids = data.get('invalid_open_ids', [])  # type: List[str]
        invalid_user_ids = data.get('invalid_user_ids', [])  # type: List[str]

        return invalid_open_ids, invalid_user_ids

    def invite_bot_to_chat(self, chat_id):
        """邀请机器人加群

        :type self: OpenLark
        :param chat_id: 群的 ID
        :type chat_id: str

        拉机器人进群，机器人的owner需要已经在群里。

        https://open.feishu.cn/document/ukTMukTMukTM/uYDO04iN4QjL2gDN
        """
        url = self._gen_request_url('/open-apis/bot/v4/add')
        body = {'chat_id': str(chat_id)}
        self._post(url, body, with_tenant_token=True)

    def remove_bot_from_chat(self, chat_id):
        """把机器人从群里踢掉

        :type self: OpenLark
        :param chat_id: 群的 ID
        :type chat_id: str

        机器人的owner需要已经在群里

        https://open.feishu.cn/document/ukTMukTMukTM/ucDO04yN4QjL3gDN
        """
        url = self._gen_request_url('/open-apis/bot/v4/remove')
        body = {'chat_id': str(chat_id)}
        self._post(url, body, with_tenant_token=True)

    def disband_chat(self, chat_id):
        """机器人解散群，机器人需要是群主

        :type self: OpenLark
        :param chat_id: 群的 ID
        :type chat_id: str

        机器人解散群(机器人需要是群主)

        https://open.feishu.cn/document/ukTMukTMukTM/uUDN5QjL1QTO04SN0kDN
        """
        url = self._gen_request_url('/open-apis/chat/v4/disband')
        body = {'chat_id': str(chat_id)}
        self._post(url, body, with_tenant_token=True)

    def is_user_in_chat(self, user_access_token, chat_ids):
        """判断用户是否在群里

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param chat_ids: 群的chat_id数组
        :type chat_ids: list[str]

        判断用户是否在群里。

        https://open.feishu.cn/document/ukTMukTMukTM/uUzM3UjL1MzN14SNzcTN
        """

        url = self._gen_request_url(
            '/open-apis/chat/v4/is_user_in?' + '&'.join(['chat_ids={}'.format(i) for i in chat_ids]))
        res = self._get(url, auth_token=user_access_token)
        in_chat_ids = res['data'].get('in_chat', [])  # type: List[str]
        return in_chat_ids
