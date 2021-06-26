# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum


class MessageType(Enum):
    """消息的类型

    支持：文本、图片、富文本、分享群聊卡片、卡片消息
    """
    text = 'text'  # 文本
    image = 'image'  # 图片
    post = 'post'  # 富文本
    share_chat = 'share_chat'  # 分享群名片
    card = 'interactive'  # 卡片消息
    forward = 'forward'  # 转发消息


class UrgentType(Enum):
    """消息加急类型

    支持：飞书内部、短信、电话
    """
    app = 'app'  # 飞书内部
    sms = 'sms'  # 短信
    phone = 'phone'  # 电话


class I18NType(Enum):
    """国际化消息的类型

    支持：中文、英文、日文
    """
    zh_cn = 'zh_cn'
    ja_jp = 'ja_jp'
    en_us = 'en_us'


class ImageColor(Enum):
    """卡片消息头部的颜色
    """
    orange = 'orange'
    red = 'red'
    yellow = 'yellow'
    gray = 'gray'
    blue = 'blue'
    green = 'green'


class MethodType(Enum):
    """卡片消息按钮的请求类型
    """
    post = 'post'  # 发送 post 请求
    get = 'get'  # 发送 get 请求
    jump = 'jump'  # 跳转到指定 url


class CalendarRole(Enum):
    reader = 'reader'  # 订阅者，可查看日程详情
    free_busy_reader = 'free_busy_reader'  # 游客，只能看到"忙碌/空闲"


class CalendarEventVisibility(Enum):
    """日历的日程的可见性

    支持：仅向他人显示是否“忙碌”；公开，显示日程详情；仅自己可见
    """
    default = 'default'  # 默认，仅向他人显示是否“忙碌”
    public = 'public'  # 公开，显示日程详情
    private = 'private'  # 仅自己可见


class ApprovalUploadFileType(Enum):
    image = 'image'
    attachment = 'attachment'


class EventType(Enum):
    """事件类型

    https://open.feishu.cn/document/uYjL24iN/uUTNz4SN1MjL1UzM
    """
    url_verification = 'url_verification'  # 这是一个验证请求
    app_ticket = 'app_ticket'  # 租户管理员开通 ISV 应用后，会定时发送 app_ticket 事件到监听地址
    app_open = 'app_open'  # 当企业管理员在管理员后台开通应用时推送事件
    message = 'message'  # 接收用户发送给应用的消息，包括与机器人直接对话或者在群聊中与机器人交流
    user_add = 'user_add'  # 通讯录变更
    user_update = 'user_update'
    user_leave = 'user_leave'
    dept_add = 'dept_add'
    dept_update = 'dept_update'
    dept_delete = 'dept_delete'
    contact_scope_change = 'contact_scope_change'
    approval = 'approval'  # 审批通过
    leave_approval = 'leave_approval'  # 请假审批
    work_approval = 'work_approval'  # 加班审批
    shift_approval = 'shift_approval'  # 换班审批
    remedy_approval = 'remedy_approval'  # 补卡审批
    trip_approval = 'trip_approval'  # 出差审批
    remove_bot = 'remove_bot'  # 移除机器人
    add_bot = 'add_bot'  # 添加机器人
    p2p_chat_create = 'p2p_chat_create'  # 用户第一次打开这个机器人的会话界面

    add_user_to_chat = 'add_user_to_chat'  # 用户进群
    remove_user_from_chat = 'remove_user_from_chat'  # 用户出群
    revoke_add_user_from_chat = 'revoke_add_user_from_chat'  # 撤销加人

    unknown = 'unknown'


class ApprovalInstanceStatus(Enum):
    pending = 'PENDING'  # 待审核
    approved = 'APPROVED'  # 已通过
    rejected = 'REJECTED'  # 已拒绝
    canceled = 'CANCELED'  # 已取消
    deleted = 'DELETED'  # 已取消


class ApprovalTaskStatus(Enum):
    pending = 'PENDING'  # 审批中
    approved = 'APPROVED'  # 通过
    rejected = 'REJECTED'  # 拒绝
    transfered = 'TRANSFERRED'  # 已转交
    canceled = 'DONE'  # 完成


class ApprovalTaskTypeStatus(Enum):
    or_sign = 'OR'  # 或签，一名负责人通过即可通过审批节点
    and_sign = 'AND'  # 或签，需所有负责人通过才能通过审批节点
    auto_pass = 'AUTO_PASS'  # 自动通过
    auto_reject = 'AUTO_REJECT'  # 自动拒绝
    sequential = 'SEQUENTIAL'  # 按照顺序


class ApprovalTimelineType(Enum):
    """动态类型"""
    start = 'START'  # 审批开始
    passed = 'PASS'  # 通过
    reject = 'REJECT'  # 拒绝
    auto_pass = 'AUTO_PASS'  # 自动通过
    auto_reject = 'AUTO_REJECT'  # 自动拒绝
    remove_repeat = 'REMOVE_REPEAT'  # 去重
    transfer = 'TRANSFER'  # 转交
    add_approver_before = 'ADD_APPROVER_BEFORE'  # 前加签
    add_approver = 'ADD_APPROVER'  # 并加签
    add_approver_after = 'ADD_APPROVER_AFTER'  # 后加签
    delete_approver = 'DELETE_APPROVER'  # 减签
    rollback_selected = 'ROLLBACK_SELECTED'  # 指定回退
    rollback = 'ROLLBACK'  # 全部回退
    cancel = 'CANCEL'  # 撤回
    delete = 'DELETE'  # 删除
    cc = 'CC'  # 抄送


class PayPricePlanType(Enum):
    """价格方案类型
    """
    trial = 'trial'  # 试用
    permanent = 'permanent'  # 一次性付费
    per_year = 'per_year'  # 企业年付费
    per_month = 'per_month'  # 企业月付费
    per_seat_per_year = 'per_seat_per_year'  # 按人按年付费
    per_seat_per_month = 'per_seat_per_month'  # 按人按月付费
    permanent_count = 'permanent_count'  # 按次付费


class PayBuyType(Enum):
    """购买类型
    """
    buy = 'buy'  # 普通购买
    # 升级购买：仅price_plan_type为per_year、per_month、per_seat_per_year、per_seat_per_month时可升级购买
    upgrade = 'upgrade'
    renew = 'renew'  # 续费购买


class PayStatus(Enum):
    """订单当前状态
    """
    normal = 'normal'  # 正常
    refund = 'refund'  # 已退款
    all = 'all'  # 全部，查询的时候会用到


class MeetingReplyStatus(Enum):
    """回复状态，NOT_CHECK_IN 表示未签到，ENDED_BEFORE_DUE 表示提前结束
    """
    not_check_in = 'NOT_CHECK_IN'  # 未签到
    ended_before_due = 'ENDED_BEFORE_DUE'  # 提前结束
