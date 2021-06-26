# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Union

from six import string_types

from utils.feishu.dt_enum import MessageType, UrgentType
from utils.feishu.dt_message import CardAction, CardHeader, CardURL, MessageAt, MessageImage, MessageLink, MessageText
from utils.feishu.exception import LarkInvalidArguments

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


def _send_all_message(self,
                      open_id='',
                      root_id='',
                      open_chat_id='',
                      employee_id='',
                      email='',
                      msg_type=MessageType.text,
                      content=None,
                      content_key='content'):
    """发消息

    :type open_id: str
    :type root_id: str
    :type open_chat_id: str
    :type employee_id: str
    :type email: str
    :type msg_type: MessageType
    :type content: Dict[str, Any]
    :type content_key: str

    :rtype str
    """
    url = self._gen_request_url('/open-apis/message/v3/send/')
    body = {
        'msg_type': msg_type.value,
        content_key: content
    }
    if open_id:
        body['open_id'] = open_id
    elif open_chat_id:
        body['open_chat_id'] = open_chat_id
    elif employee_id:
        body['employee_id'] = employee_id
    elif email:
        body['email'] = email

    if root_id:
        body['root_id'] = root_id

    res = self._post(url, body, with_tenant_token=True)
    return res['open_message_id']


class _Send(object):
    __to = {}  # type: Dict[string_types, Any]
    __open_lark = None
    __root_id = ''

    def __init__(self, open_lark, to, root_id=''):
        self.__to = to
        self.__open_lark = open_lark
        self.__root_id = root_id

    def __dir__(self):
        """dir(x)

        :rtype Iterable[str]
        """
        return ['send_card', 'send_image', 'send_post', 'send_share_chat', 'send_text']

    def send_text(self, text):
        """发送文本消息

        :param text: 文本
        :return: 发送成功的消息 open_message_id
        """
        body = deepcopy(self.__to)
        if self.__root_id:
            body['root_id'] = self.__root_id
        body['msg_type'] = MessageType.text
        body['content'] = {
            'text': text
        }

        return _send_all_message(self.__open_lark, **body)

    def send_image(self, image_key):
        """发送图片消息

        :param image_key: 图片的 key，可以通过 upload_image 接口上传文件获取
        :return: 发送成功的消息 open_message_id
        """
        body = deepcopy(self.__to)
        if self.__root_id:
            body['root_id'] = self.__root_id
        body['msg_type'] = MessageType.image
        body['content'] = {
            'image_key': image_key
        }

        return _send_all_message(self.__open_lark, **body)

    def send_share_chat(self, open_chat_id):
        """分享群聊卡片

        :param open_chat_id: 群聊的 open_chat_id
        :type open_chat_id: str
        :return: 发送成功的消息 open_message_id
        """
        body = deepcopy(self.__to)
        if self.__root_id:
            body['root_id'] = self.__root_id
        body['msg_type'] = MessageType.share_chat
        body['content'] = {
            'share_open_chat_id': open_chat_id
        }

        return _send_all_message(self.__open_lark, **body)

    def send_post(self,
                  zh_cn_title,
                  zh_cn_content,
                  en_us_title=None,
                  en_us_content=None):
        """发送富文本消息

        :param zh_cn_title: 中文标题
        :type zh_cn_title: str
        :param zh_cn_content: 中文内容，是 MessageText, MessageAt, MessageImage, MessageLink 的二维数组
        :type zh_cn_content: List[List[Union[MessageText, MessageAt, MessageImage, MessageLink]]]
        :param en_us_title: 英文标题
        :type en_us_title: str
        :param en_us_content: 英文内容，是 MessageText, MessageAt, MessageImage, MessageLink 的二维数组
        :type en_us_content: List[List[Union[MessageText, MessageAt, MessageImage, MessageLink]]]
        :return: 发送成功的消息 open_message_id
        """
        if not zh_cn_title and not en_us_title and not zh_cn_content and not en_us_content:
            raise LarkInvalidArguments(msg='send post message with empty content')

        body = deepcopy(self.__to)
        if self.__root_id:
            body['root_id'] = self.__root_id
        body['msg_type'] = MessageType.post
        body['content'] = {
            'post': {
                'zh_cn': {
                    'title': zh_cn_title,
                    'content': [list(map(lambda cls: cls.as_post_dict(), i)) for i in zh_cn_content],
                }
            }
        }
        if en_us_title is not None or en_us_content is not None:
            body['content']['post']['en_us'] = {}
            if en_us_title is not None:
                body['content']['post']['en_us']['title'] = en_us_title
            if en_us_content is not None:
                body['content']['post']['en_us']['content'] = \
                    [list(map(lambda cls: cls.as_post_dict(), i)) for i in en_us_content]

        return _send_all_message(self.__open_lark, **body)

    def send_card(self,
                  card_link=None,
                  header=None,
                  content=None,
                  actions=None):
        """发送卡片消息

        :param card_link: 卡片消息的链接，是 CardURL
        :type card_link: CardURL
        :param header: 卡片消息的头部，是 CardHeader
        :type header: CardHeader
        :param content: 卡片消息的内容，是 MessageText, MessageAt, MessageImage, MessageLink 中任意一个的二维数组
        :type content: List[List[Union[MessageText, MessageAt, MessageImage, MessageLink]]]
        :param actions: 卡片消息的按钮，是 CardAction 的列表
        :type actions: List[CardAction]
        :return: 发送成功的消息 open_message_id
        """
        card = {}  # type: Dict[string_types, Any]
        if card_link:
            card['card_link'] = card_link.as_card_dict()
        if header:
            card['header'] = header.as_dict()
        if content:
            card['content'] = [list(map(lambda cls: cls.as_card_dict(), i)) for i in content]
        if actions:
            card['actions'] = [i.as_dict() for i in actions]

        body = deepcopy(self.__to)
        if self.__root_id:
            body['root_id'] = self.__root_id
        body['msg_type'] = MessageType.card
        body['content'] = {'card': card}

        return _send_all_message(self.__open_lark, **body)

    def send_forward_post(self, title, post):
        """转发富文本消息，富文本消息来自消息监听内容

        :param title: 监听到的标题
        :type title: str
        :param post: 监听到的富文本内容
        :return: 发送成功的消息 open_message_id
        """
        body = deepcopy(self.__to)
        if self.__root_id:
            body['root_id'] = self.__root_id
        body['msg_type'] = MessageType.forward
        body['content'] = {
            'title': title,
            'text': post,
        }

        return _send_all_message(self.__open_lark, **body)


class _To(object):
    __open_lark = None
    __root_id = ''
    __to = {}  # type: Dict[string_types, string_types]

    def __init__(self, open_lark, root_id=''):
        self.__open_lark = open_lark
        self.__root_id = root_id

    def __dir__(self):
        """
        :rtype Iterable[str]
        """
        return [
            'to_email',
            'to_open_id',
            'to_employee_id',
            'to_open_chat_id'
        ]

    def to_email(self, email):
        """发送到哪个 email 的用户处

        :param email: email
        :return: 链式调用对象，可以调用 send 方法
        """
        self.__to = {'email': email}
        return _Send(open_lark=self.__open_lark, to=self.__to, root_id=self.__root_id)

    def to_open_id(self, open_id):
        """发送到哪个 open_id 的用户处

        :param open_id: open_id
        :return: 链式调用对象，可以调用 send 方法
        """
        self.__to = {'open_id': open_id}
        return _Send(open_lark=self.__open_lark, to=self.__to, root_id=self.__root_id)

    def to_employee_id(self, employee_id):
        """发送到哪个 employee_id 的用户处

        :param employee_id: employee_id
        :return: 链式调用对象，可以调用 send 方法
        """
        self.__to = {'employee_id': employee_id}
        return _Send(open_lark=self.__open_lark, to=self.__to, root_id=self.__root_id)

    def to_open_chat_id(self, open_chat_id):
        """发送到哪个 open_chat_id 的用户处

        :param open_chat_id: open_chat_id
        :return: 链式调用对象，可以调用 send 方法
        """
        self.__to = {'open_chat_id': open_chat_id}
        return _Send(open_lark=self.__open_lark, to=self.__to, root_id=self.__root_id)


class APIMessageMixin(object):
    email = None
    open_id = None

    def batch_send_message(self,
                           department_ids=None,
                           open_ids=None,
                           employee_ids=None,
                           msg_type=MessageType.text,
                           content=None):
        """批量发送消息

        :type self: OpenLark
        :param department_ids: 部门 department_ids
        :type department_ids: List[str]
        :param open_ids: open_ids
        :type open_ids: List[str]
        :param employee_ids: employee_ids
        :type employee_ids: List[str]
        :param msg_type: 消息类型，是 MessageType
        :type msg_type: MessageType
        :param content: 消息内容，请参考文档设置
        :type content: Dict[str, Any]
        :return: 消息 id，和三个数组
        :rtype: Tuple[str, List[str], List[str], List[str]]

        给多个用户或者多个部门发送消息。

        https://open.feishu.cn/document/ukTMukTMukTM/ucDO1EjL3gTNx4yN4UTM
        """
        url = self._gen_request_url('/open-apis/message/v3/batch_send/')
        if department_ids is None:
            department_ids = []
        if open_ids is None:
            open_ids = []
        if employee_ids is None:
            employee_ids = []
        body = {
            "department_ids": department_ids,
            "open_ids": open_ids,
            "employee_ids": employee_ids,
            "msg_type": msg_type.value,
            "content": content
        }
        res = self._post(url=url, body=body, with_tenant_token=True)
        invalid_department_ids = res.get('invalid_department_ids', [])  # type: List[str]
        invalid_open_ids = res.get('invalid_open_ids', [])  # type: List[str]
        invalid_employee_ids = res.get('invalid_employee_ids', [])  # type: List[str]
        message_id = res.get('message_id', '')  # type: str

        return message_id, invalid_department_ids, invalid_open_ids, invalid_employee_ids

    def send_raw_message(self,
                         open_id='',
                         root_id='',
                         open_chat_id='',
                         employee_id='',
                         email='',
                         msg_type=MessageType.text,
                         content=None,
                         content_key='content'):
        """发原始消息

        :type self: OpenLark
        :param open_id: open_id
        :type open_id: str
        :param root_id: 要回复的那条消息的 open_message_id
        :type root_id: str
        :param open_chat_id: 聊天的id，回调中会返回
        :type open_chat_id: str
        :param employee_id: employee_id
        :type employee_id: str
        :param email: email
        :type email: str
        :param msg_type: 消息类型，是 MessageType
        :type msg_type: MessageType
        :param content: 消息内容，请参考文档设置
        :type content: Dict[str, Any]
        :param content_key: 新版本的卡片消息需要设置为 card
        :type content_key: str
        :return: 发送的消息的 open_message_id
        :rtype: str

        https://open.feishu.cn/document/ukTMukTMukTM/uUjNz4SN2MjL1YzM
        """
        return _send_all_message(self,
                                 open_id=open_id,
                                 root_id=root_id,
                                 open_chat_id=open_chat_id,
                                 employee_id=employee_id,
                                 email=email,
                                 msg_type=msg_type,
                                 content=content,
                                 content_key=content_key)

    def reply(self, root_id):
        """

        :type self: OpenLark
        :param root_id:
        :return:
        :rtype _TO
        """
        return _To(self, root_id=root_id)

    def send(self):
        """创建发消息的调用链，返回链式对象

        :type self: OpenLark
        :rtype _To
        """
        return _To(self)

    def urgent_message(self,
                       open_message_id,
                       open_ids,
                       urgent_type=UrgentType.app):
        """消息加急

        :type self: OpenLark
        :param open_message_id: 消息 ID，指定对某条消息进行加急，该 ID 在发送消息后获得
        :type open_message_id: str
        :param urgent_type: 加急类型。目前支持应用内加急（app），短信加急（sms），电话加急（phone）。加急权限需要申请。
        :type urgent_type: UrgentType
        :param open_ids: 用户 open_id 列表，指定该参数对指定用户进行消息加急
        :type open_ids: List[str]
        :return: 非法的用户 ID 列表
        :rtype List[str]

        对指定消息进行加急。

        https://lark-open.bytedance.net/document/ukTMukTMukTM/uYzM04iNzQjL2MDN
        """
        url = self._gen_request_url('/open-apis/message/v3/urgent/')
        body = {
            'open_message_id': open_message_id,
            'urgent_type': urgent_type.value,
            'open_ids': open_ids
        }
        res = self._post(url, body=body, with_tenant_token=True)
        invalid_open_ids = res.get('invalid_open_ids', [])  # type: List[str]
        return invalid_open_ids

    def recall(self, open_message_id):
        """撤回消息

        :type self: OpenLark
        :param open_message_id: 需要撤回的消息id
        :type open_message_id: str

        撤回指定消息。

        https://open.feishu.cn/document/ukTMukTMukTM/ukjN1UjL5YTN14SO2UTN
        """
        url = self._gen_request_url('/open-apis/message/v4/recall/')
        body = {
            'message_id': open_message_id,
        }
        self._post(url, body=body, with_tenant_token=True)

# TODO: 消息卡片安全校验
