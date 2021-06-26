# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import hashlib
import json
import logging
from typing import TYPE_CHECKING, Any, Dict

from Crypto.Cipher import AES

from utils.feishu.dt_callback import (EventAppOpen, EventApproval, EventAppTicket, EventContactDepartment, EventContactScope,
                                      EventContactUser, EventLeaveApproval, EventMessage, EventP2PCreateChat,
                                      EventRemedyApproval, EventRemoveAddBot, EventShiftApproval, EventTripApproval,
                                      EventUserInAndOutChat, EventWorkApproval)
from utils.feishu.dt_enum import EventType
from utils.feishu.dt_help import make_datatype
from utils.feishu.exception import LarkInvalidArguments, LarkInvalidCallback
from utils.feishu.helper import pop_or_none

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark

logger = logging.getLogger('feishu')


class _AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(_AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data  # pragma: no cover

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)
        return self.decrypt(enc).decode('utf8')


def get_event_type(body):
    """
    :param body:
    :type body: Dict[string_types, typing.Union[Any, Dict[string_types, Any]]]
    :return:
    """
    t = body.get('type')

    if t == 'event_callback':
        t = body.get('event', {}).get('type')
        return {
            'app_ticket': EventType.app_ticket,  # DONE
            'app_open': EventType.app_open,
            'message': EventType.message,  # DONE
            'user_add': EventType.user_add,
            'user_update': EventType.user_update,
            'user_leave': EventType.user_leave,
            'dept_add': EventType.dept_add,
            'dept_update': EventType.dept_update,
            'dept_delete': EventType.dept_delete,
            'contact_scope_change': EventType.contact_scope_change,
            'approval': EventType.approval,
            'leave_approval': EventType.leave_approval,
            'work_approval': EventType.work_approval,
            'shift_approval': EventType.shift_approval,
            'remedy_approval': EventType.remedy_approval,
            'trip_approval': EventType.trip_approval,
            'remove_bot': EventType.remove_bot,
            'add_bot': EventType.add_bot,
            'p2p_chat_create': EventType.p2p_chat_create,
        }.get(t, EventType.unknown)

    return {
        'url_verification': EventType.url_verification,
    }.get(t, EventType.unknown)


class APICallbackMixin(object):
    """订阅事件

    飞书中很多操作都会产生事件，应用可以订阅这些事件来与飞书进行高度整合，可以在开发者后台进行事件订阅配置来监听事件。

    已经有的事件类型：

    - 审批通过
    - 收到消息（必须单聊或者是艾特机器人）
    - 推送 app_ticket

    https://open.feishu.cn/document/uYjL24iN/uUTNz4SN1MjL1UzM
    """

    def handle_callback(
            self,
            body,
            handle_message=None,
            handle_app_ticket=None,
            handle_approval=None,
            handle_leave_approval=None,
            handle_work_approval=None,
            handle_shift_approval=None,
            handle_remedy_approval=None,
            handle_trip_approval=None,
            handle_app_open=None,
            handle_contact_user=None,
            handle_contact_department=None,
            handle_contact_scope=None,
            handle_remove_add_bot=None,
            handle_p2p_chat_create=None,
            handle_user_in_out_chat=None,
    ):
        """处理机器人回调

        :type self: OpenLark
        :param body: 回调的消息主题
        :type body: Dict[string_types, Any]
        :param handle_message: 消息的回调 - 处理函数
        :type handle_message: Callable[[str, str, 'EventMessage', Dict[str, Any]], Any]
        :param handle_app_ticket: app_ticket 事件 - 处理函数
        :type handle_app_ticket: Callable[[str, str, 'EventAppTicket', Dict[str, Any]], Any]
        :param handle_approval:
        :type handle_approval: Callable[[str, str, 'EventApproval', Dict[str, Any]], Any]
        :param handle_leave_approval:
        :type handle_leave_approval: Callable[[str, str, 'EventLeaveApproval', Dict[str, Any]], Any]
        :param handle_work_approval:
        :type handle_work_approval: Callable[[str, str, 'EventWorkApproval', Dict[str, Any]], Any]
        :param handle_shift_approval:
        :type handle_shift_approval: Callable[[str, str, 'EventShiftApproval', Dict[str, Any]], Any]
        :param handle_remedy_approval:
        :type handle_remedy_approval: Callable[[str, str, 'EventRemedyApproval', Dict[str, Any]], Any]
        :param handle_trip_approval:
        :type handle_trip_approval: Callable[[str, str, 'EventTripApproval', Dict[str, Any]], Any]
        :param handle_app_open:
        :type handle_app_open: Callable[[str, str, 'EventAppOpen', Dict[str, Any]], Any]
        :param handle_contact_user:
        :type handle_contact_user: Callable[[str, str, 'EventContactUser', Dict[str, Any]], Any]
        :param handle_contact_department:
        :type handle_contact_department: Callable[[str, str, 'EventContactDepartment', Dict[str, Any]], Any]
        :param handle_contact_scope:
        :type handle_contact_scope: Callable[[str, str, 'EventContactScope', Dict[str, Any]], Any]
        :param handle_remove_add_bot:
        :type handle_remove_add_bot: Callable[[str, str, 'EventRemoveAddBot', Dict[str, Any]], Any]
        :param handle_p2p_chat_create:
        :type handle_p2p_chat_create: Callable[[str, str, 'EventP2PCreateChat', Dict[str, Any]], Any]
        :param handle_user_in_out_chat:
        :type handle_user_in_out_chat: Callable[[str, str, 'EventUserInAndOutChat', Dict[str, Any]], Any]
        """
        if not isinstance(body, dict):
            raise LarkInvalidArguments(msg='回调参数需要是字典')

        if 'encrypt' in body:
            body = json.loads(self.decrypt_string(body['encrypt']))

        if not self.verification_token:
            raise LarkInvalidArguments(msg='回调需要 verification_token 参数')

        token = body.get('token')
        if token != self.verification_token:
            raise LarkInvalidCallback(msg='token: {} 不合法'.format(token))

        event_type = get_event_type(body)
        if event_type == EventType.url_verification:
            return {'challenge': body.get('challenge')}

        msg_uuid = body.get('uuid', '')  # type: str
        msg_timestamp = body.get('ts', '')  # type: str
        json_event = body.get('event', {})  # type: Dict[str, Any]

        logger.info('[callback] uuid=%s, ts=%s, event=%s', msg_uuid, msg_timestamp, json_event)

        if event_type == EventType.approval:
            # 审批通过
            if handle_approval:
                event_approval = make_datatype(EventApproval, json_event)
                return handle_approval(msg_uuid, msg_timestamp, event_approval, json_event)
            return

        if event_type == EventType.leave_approval:
            # 请假审批
            if handle_leave_approval:
                event_leave_approval = make_datatype(EventLeaveApproval, json_event)
                return handle_leave_approval(msg_uuid, msg_timestamp, event_leave_approval, json_event)
            return

        if event_type == EventType.work_approval:
            # 加班审批
            if handle_work_approval:
                event_work_approval = make_datatype(EventWorkApproval, json_event)
                return handle_work_approval(msg_uuid, msg_timestamp, event_work_approval, json_event)
            return

        if event_type == EventType.shift_approval:
            # 换班审批
            if handle_shift_approval:
                event_shift_approval = make_datatype(EventShiftApproval, json_event)
                return handle_shift_approval(msg_uuid, msg_timestamp, event_shift_approval, json_event)
            return

        if event_type == EventType.remedy_approval:
            # 补卡审批
            if handle_remedy_approval:
                event_remedy_approval = make_datatype(EventRemedyApproval, json_event)
                return handle_remedy_approval(msg_uuid, msg_timestamp, event_remedy_approval, json_event)
            return

        if event_type == EventType.trip_approval:
            # 出差审批
            if handle_trip_approval:
                event_trip_approval = make_datatype(EventTripApproval, json_event)
                return handle_trip_approval(msg_uuid, msg_timestamp, event_trip_approval, json_event)
            return

        if event_type == EventType.app_open:
            # 开通应用
            if handle_app_open:
                event_app_open = make_datatype(EventAppOpen, json_event)
                return handle_app_open(msg_uuid, msg_timestamp, event_app_open, json_event)
            return

        if event_type in [EventType.user_add, EventType.user_leave, EventType.user_update]:
            # 通讯录用户相关变更事件，包括 user_add, user_update 和 user_leave 事件类型
            if handle_contact_user:
                event_contact_user = make_datatype(EventContactUser, json_event)
                return handle_contact_user(msg_uuid, msg_timestamp, event_contact_user, json_event)
            return

        if event_type in [EventType.dept_add, EventType.dept_delete, EventType.dept_update]:
            # 通讯录部门相关变更事件，包括 dept_add, dept_update 和 dept_delete
            if handle_contact_department:
                event_contact_department = make_datatype(EventContactDepartment, json_event)
                return handle_contact_department(msg_uuid, msg_timestamp, event_contact_department, json_event)
            return

        if event_type == EventType.contact_scope_change:
            # 变更权限范围
            if handle_contact_scope:
                event_contact_scope = make_datatype(EventContactScope, json_event)
                return handle_contact_scope(msg_uuid, msg_timestamp, event_contact_scope, json_event)
            return

        if event_type == EventType.message:
            # 收到消息（必须单聊或者是艾特机器人）的回调
            if handle_message:
                event = make_datatype(EventMessage, json_event)  # type: EventMessage
                return handle_message(msg_uuid, msg_timestamp, event, json_event)
            return

        if event_type in [EventType.remove_bot, EventType.add_bot]:
            # 机器人被移出群聊/机器人被邀请进入群聊
            if handle_remove_add_bot:
                event_remove_add_bot = make_datatype(EventRemoveAddBot, json_event)
                return handle_remove_add_bot(msg_uuid, msg_timestamp, event_remove_add_bot, json_event)
            return

        if event_type == EventType.app_ticket:
            # 下发 app_ticket
            event_app_ticket = make_datatype(EventAppTicket, json_event)
            self.update_app_ticket(event_app_ticket.app_ticket)
            if handle_app_ticket:
                return handle_app_ticket(msg_uuid, msg_timestamp, event_app_ticket, json_event)
            return

        if event_type == EventType.p2p_chat_create:
            # 机器人和用户的会话第一次创建
            if handle_p2p_chat_create:
                event_chat_create = make_datatype(EventP2PCreateChat, json_event)
                return handle_p2p_chat_create(msg_uuid, msg_timestamp, event_chat_create, json_event)
            return

        if event_type in [EventType.add_user_to_chat, EventType.remove_user_from_chat,
                          EventType.revoke_add_user_from_chat]:
            # 用户进群和出群
            if handle_user_in_out_chat:
                event_in_and_out_chat = make_datatype(EventUserInAndOutChat, json_event)
                return handle_user_in_out_chat(msg_uuid, msg_timestamp, event_in_and_out_chat, json_event)
            return

        logger.warning('[callback][unknown event] uuid=%s, ts=%s, event=%s', msg_uuid, msg_timestamp, event_type)
        return {
            'message': 'event: {} not handle'.format(event_type),
            'msg_uuid': msg_uuid,
            'msg_timestamp': msg_timestamp,
            'json_event': json_event,
        }

    def handle_card_message_callback(self, body, handle=None):
        """处理卡片消息的回调

        :type self: OpenLark
        :type body: Dict[string_types, Any]
        :type handle: Callable[[str, str, str, str, str, Dict[str, Any]], Any]
        """
        if not isinstance(body, dict):
            raise LarkInvalidArguments(msg='回调参数需要是字典')

        if 'encrypt' in body:
            body = json.loads(self.decrypt_string(body['encrypt']))

        event_type = get_event_type(body)
        if event_type == EventType.url_verification:
            if not self.verification_token:
                raise LarkInvalidArguments(msg='回调需要 verification_token 参数')

            token = body.get('token')
            if token != self.verification_token:
                raise LarkInvalidCallback(msg='token: {} 不合法'.format(token))

            return {'challenge': body.get('challenge')}

        open_id = pop_or_none(body, 'open_id')
        employee_id = pop_or_none(body, 'employee_id')
        open_message_id = pop_or_none(body, 'open_message_id')
        tenant_key = pop_or_none(body, 'tenant_key')
        tag = pop_or_none(body, 'tag')
        return handle(tenant_key, open_id, employee_id, open_message_id, tag, body)

    def decrypt_string(self, s):
        """

        :type self: OpenLark
        :param s:
        :return:
        """
        if not self.encrypt_key:
            raise LarkInvalidArguments(msg='需要 encrypt_key 参数')
        return _AESCipher(self.encrypt_key).decrypt_string(s)
