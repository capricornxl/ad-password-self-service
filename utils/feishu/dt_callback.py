# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import List

import attr

from utils.feishu.dt_code import SimpleUser
from utils.feishu.dt_help import to_json_decorator


@to_json_decorator
@attr.s
class EventMessageMergeForward(object):
    root_id = attr.ib(type=str, default=None)
    parent_id = attr.ib(type=str, default=None)
    open_chat_id = attr.ib(type=str, default=None)
    msg_type = attr.ib(type=str, default=None)
    open_id = attr.ib(type=str, default=None)
    open_message_id = attr.ib(type=str, default=None)
    is_mention = attr.ib(type=bool, default=None)
    image_key = attr.ib(type=str, default=None)
    image_url = attr.ib(type=str, default=None)
    create_time = attr.ib(type=int, default=None)


@to_json_decorator
@attr.s
class EventMessage(object):
    """消息事件
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)  # 租户 key
    type = attr.ib(type=str, default=None)

    # 消息事件公共
    root_id = attr.ib(type=str, default=None)  # 回复的祖先消息id
    parent_id = attr.ib(type=str, default=None)  # 回复的消息id
    open_chat_id = attr.ib(type=str, default=None)  # 本次消息所发生的对话，注意：私聊也有这个
    chat_type = attr.ib(type=str, default=None)  # 私聊private，群聊group
    msg_type = attr.ib(type=str, default=None)  # 消息类型
    open_id = attr.ib(type=str, default=None)
    open_message_id = attr.ib(type=str, default=None)  # 本校消息的 id
    is_mention = attr.ib(type=bool, default=None)

    # 文本消息、富文本消息含有的
    text = attr.ib(type=str, default='')  # 文本（text 和 post）
    text_without_at_bot = attr.ib(type=str, default='')  # 消息内容，会过滤掉at你的机器人的内容（text 和 post）

    # 富文本消息
    image_keys = attr.ib(type=List[str], default=attr.Factory(list))  # image_key的列表（post）
    title = attr.ib(type=str, default='')  # 标题（post）

    # 图片消息独有的
    image_height = attr.ib(type=str, default='')  # 图片高度（image）
    image_width = attr.ib(type=str, default='')  # 图片宽度（image）
    image_url = attr.ib(type=str, default='')  # 图片的url（image）
    image_key = attr.ib(type=str, default='')  # 图片的key（image）

    # 合并转发消息，（日历卡片、投票消息、会话记录等不支持合并转发）
    msg_list = attr.ib(type=List[EventMessageMergeForward], default=attr.Factory(list))  # 合并转发消息的每个消息体


@to_json_decorator
@attr.s
class EventApproval(object):
    """"审批通过

    订阅审批定义后，该定义产生的审批实例在结束时，会推送事件消息。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    definition_code = attr.ib(type=str, default=None)  # 审批定义Code
    definition_name = attr.ib(type=str, default=None)  # 审批定义名称
    instance_code = attr.ib(type=str, default=None)  # 审批实例Code
    start_time = attr.ib(type=int, default=None)  # 审批发起时间，10位秒级
    end_time = attr.ib(type=int, default=None)  # 审批结束时间，10位秒级
    event = attr.ib(type=str, default=None)  # 审批结果 approve:通过 reject:拒绝 cancel:取消


@to_json_decorator
@attr.s
class EventLeaveApproval(object):
    """"请假审批

    请假审批通过后， 开放平台推送 leave_approval 事件到请求网址。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    instance_code = attr.ib(type=str, default=None)  # 审批实例Code
    employee_id = attr.ib(type=str, default=None)  # 用户id
    start_time = attr.ib(type=int, default=None)  # 审批发起时间，10位秒级
    end_time = attr.ib(type=int, default=None)  # 审批结束时间，10位秒级
    leave_type = attr.ib(type=str, default=None)  # 请假类型
    leave_unit = attr.ib(type=int, default=None)  # 请假单位：1：半天，2：一天
    leave_start_time = attr.ib(type=str, default=None)  # 请假开始时间 "2018-12-01 12:00:00"
    leave_end_time = attr.ib(type=str, default=None)  # 请假结束时间
    leave_interval = attr.ib(type=int, default=None)  # 请假时长，单位（秒）
    leave_reason = attr.ib(type=str, default=None)  # 请假事由


@to_json_decorator
@attr.s
class EventWorkApproval(object):
    """加班审批

    加班审批通过后推送消息，开放平台推送 work_approval 事件到请求网址。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    instance_code = attr.ib(type=str, default=None)  # 审批实例Code
    employee_id = attr.ib(type=str, default=None)  # 用户id
    start_time = attr.ib(type=int, default=None)  # 审批发起时间，10位秒级
    end_time = attr.ib(type=int, default=None)  # 审批结束时间，10位秒级
    work_type = attr.ib(type=str, default=None)  # 加班类型
    work_start_time = attr.ib(type=str, default=None)  # 加班开始时间  2018-12-01 12:00:00
    work_end_time = attr.ib(type=str, default=None)  # 加班结束时间
    work_interval = attr.ib(type=int, default=None)  # 加班时长，单位（秒）
    work_reason = attr.ib(type=str, default=None)  # 加班事由


@to_json_decorator
@attr.s
class EventShiftApproval(object):
    """换班审批

    换班审批通过后推送消息，开放平台推送 shift_approval 事件到请求网址。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    instance_code = attr.ib(type=str, default=None)  # 审批实例Code
    employee_id = attr.ib(type=str, default=None)  # 用户id
    start_time = attr.ib(type=int, default=None)  # 审批发起时间，10位秒级
    end_time = attr.ib(type=int, default=None)  # 审批结束时间，10位秒级
    shift_time = attr.ib(type=str, default=None)  # 换班时间 2018-12-01 12:00:00
    return_time = attr.ib(type=str, default=None)  # 还班时间 2018-12-01 12:00:00
    shift_reason = attr.ib(type=str, default=None)  # 换班事由


@to_json_decorator
@attr.s
class EventRemedyApproval(object):
    """补卡审批

    补卡审批通过后， 开放平台推送 remedy_approval 事件到请求网址。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    instance_code = attr.ib(type=str, default=None)  # 审批实例Code
    employee_id = attr.ib(type=str, default=None)  # 用户id
    start_time = attr.ib(type=int, default=None)  # 审批发起时间
    end_time = attr.ib(type=int, default=None)  # 审批结束时间
    remedy_time = attr.ib(type=str, default=None)  # 补卡时间 2018-12-01 12:00:00
    remedy_reason = attr.ib(type=str, default=None)  # 补卡原因


@to_json_decorator
@attr.s
class EventTripApprovalSchedule(object):
    trip_start_time = attr.ib(type=str, default=None)  # 行程开始时间，"2018-12-01 12:00:00"
    trip_end_time = attr.ib(type=str, default=None)  # 行程结束时间，"2018-12-01 12:00:00"
    trip_interval = attr.ib(type=int, default=None)  # 行程时长（秒）
    departure = attr.ib(type=str, default=None)  # 出发地
    destination = attr.ib(type=str, default=None)  # 目的地
    transportation = attr.ib(type=str, default=None)  # 目的地
    trip_type = attr.ib(type=str, default=None)  # 单程/往返
    remark = attr.ib(type=str, default=None)  # 备注


@to_json_decorator
@attr.s
class EventTripApproval(object):
    """出差审批

    出差审批通过后推送消息，开放平台推送 trip_approval 事件到请求网址。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    instance_code = attr.ib(type=str, default=None)  # 审批实例Code
    employee_id = attr.ib(type=str, default=None)  # 用户id
    start_time = attr.ib(type=int, default=None)  # 审批发起时间
    end_time = attr.ib(type=int, default=None)  # 审批结束时间

    trip_interval = attr.ib(type=int, default=None)  # 行程总时长（秒）
    trip_reason = attr.ib(type=str, default=None)  # 出差事由
    trip_peers = attr.ib(type=List[str], default=attr.Factory(list))  # 同行人
    schedules = attr.ib(type=List[EventTripApprovalSchedule], default=attr.Factory(list))


@to_json_decorator
@attr.s
class EventAppOpenUser(object):
    open_id = attr.ib(type=str, default=None)  # 申请者的open_id
    user_id = attr.ib(type=str, default=None)  # 申请者的user_id


@to_json_decorator
@attr.s
class EventAppOpen(object):
    """开通应用

    当企业管理员在管理员后台开通应用时，开放平台推送 app_open 事件到请求网址。
    """
    app_id = attr.ib(type=str, default=None)  # 应用ID
    tenant_key = attr.ib(type=str, default=None)  # 企业ID
    type = attr.ib(type=str, default=None)  # 事件类型
    applicants = attr.ib(type=List[EventAppOpenUser], default=attr.Factory(list))  # 申请者的open_id
    installer = attr.ib(type=EventAppOpenUser, default=None)  # 申请者的user_id


@to_json_decorator
@attr.s
class EventContactUser(object):
    """通讯录变更

    应用申请通讯录读权限，平台会自动给相应应用订阅通讯录变更事件。

    通讯录用户相关变更事件，包括 user_add, user_update 和 user_leave 事件类型
    """
    type = attr.ib(type=str, default=None)  # 事件类型，包括 user_add, user_update, user_leave
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)  # 企业标识
    open_id = attr.ib(type=str, default=None)
    employee_id = attr.ib(type=str, default='')  # 企业自建应用返回


@to_json_decorator
@attr.s
class EventContactDepartment(object):
    """通讯录变更

    应用申请通讯录读权限，平台会自动给相应应用订阅通讯录变更事件。

    通讯录部门相关变更事件，包括 dept_add, dept_update 和 dept_delete
    """
    type = attr.ib(type=str, default=None)  # 事件类型，包括 dept_add,dept_update,dept_delete
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)  # 企业标识
    open_department_id = attr.ib(type=str, default=None)  # 部门的Id


@to_json_decorator
@attr.s
class EventContactScope(object):
    """当企业管理员在企业管理后台变更权限范围时，开放平台通知 contact_scope_change 到请求网址
    """
    type = attr.ib(type=str, default=None)  # 事件类型
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)  # 企业标识


@to_json_decorator
@attr.s
class EventRemoveAddBotI18NTitle(object):
    en_us = attr.ib(type=str, default=None)
    zh_cn = attr.ib(type=str, default=None)


@to_json_decorator
@attr.s
class EventAppTicket(object):
    """app_ticket 事件

    对于应用商店应用，开放平台会定时发送 app_ticket 事件到请求网址，应用通过该 app_ticket 获取 app_access_token。
    """
    app_id = attr.ib(type=str, default=None)
    app_ticket = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)


@to_json_decorator
@attr.s
class EventRemoveAddBot(object):
    """机器人被移出群聊/机器人被邀请进入群聊

    机器人被邀请进入群聊时/被从群聊中移除时，平台推送 add_bot/remove_bot 通知事件到请求网址。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    chat_name = attr.ib(type=str, default=None)  # 群名称
    chat_owner_employee_id = attr.ib(type=str, default=None)  # 群主的employee_id（如果群主是机器人则没有这个字段）
    chat_owner_name = attr.ib(type=str, default=None)  # 群主名称
    chat_owner_open_id = attr.ib(type=str, default=None)  # 群主的open_id
    open_chat_id = attr.ib(type=str, default=None)
    operator_employee_id = attr.ib(type=str, default=None)  # 操作者的emplolyee_id
    operator_name = attr.ib(type=str, default=None)  # 操作者姓名
    operator_open_id = attr.ib(type=str, default=None)  # 操作者的open_id
    owner_is_bot = attr.ib(type=bool, default=False)  # 群主是否是机器人
    chat_i18n_names = attr.ib(type=EventRemoveAddBotI18NTitle, default=None)  # 群名称国际化字段


@to_json_decorator
@attr.s
class EventP2PCreateChatUser(object):
    open_id = attr.ib(type=str, default=None)
    user_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)


@to_json_decorator
@attr.s
class EventP2PCreateChat(object):
    """会话第一次创建的事件

    机器人和用户的会话第一次创建的时候会发送通知。
    """
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)

    chat_id = attr.ib(type=str, default=None)  # 机器人和用户的会话id
    # 如果是机器人发起的，operator里面是机器人的open_id。如果是用户发起operator里面是用户的open_id和user_id
    operator = attr.ib(type=EventP2PCreateChatUser, default=None)
    user = attr.ib(type=EventP2PCreateChatUser, default=None)


@to_json_decorator
@attr.s
class EventUserInAndOutChat(object):
    """用户进出群聊
    """

    # ISV 应用没有 “user_id” 字段
    app_id = attr.ib(type=str, default=None)
    tenant_key = attr.ib(type=str, default=None)

    # 用户进群 add_user_to_chat"
    # 用户出群 remove_user_from_chat
    # 撤销加人 revoke_add_user_from_chat
    type = attr.ib(type=str, default=None)

    chat_id = attr.ib(type=str, default=None)

    # 用户主动退群的话，operator 就是user自己
    operator = attr.ib(type=SimpleUser, default=None)
    users = attr.ib(type=List[SimpleUser], default=attr.Factory(list))
