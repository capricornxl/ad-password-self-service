# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import Any, List

import attr

from utils.feishu.dt_enum import ApprovalInstanceStatus, ApprovalTaskStatus, ApprovalTaskTypeStatus, ApprovalTimelineType
from utils.feishu.dt_help import to_json_decorator


@to_json_decorator
@attr.s
class ApprovalNode(object):
    """审批节点对象
    """
    name = attr.ib(type=str, default='')  # 节点名称
    need_approver = attr.ib(type=bool, default=None)  # 是否发起人自选节点，true - 发起审批时需要提交审批人
    node_id = attr.ib(type=str, default=None)  # 节点 ID
    custom_id = attr.ib(type=str, default=None)  # 节点自定义 ID，如果没有设置则不返回
    node_type = attr.ib(type=str, default=None)  # 审批方式，AND -会签，OR - 或签


@to_json_decorator
@attr.s
class ApprovalForm(object):
    """审批表单字段对象
    """
    id = attr.ib(type=str, default=None)  # 控件 ID
    custom_id = attr.ib(type=str, default=None)  # 控件自定义 ID
    type = attr.ib(type=str, default=None)  # 控件类型
    name = attr.ib(type=str, default=None)  # 控件名称

    # 获取审批定义的时候不会返回，获取实例的时候会返回
    value = attr.ib(type=Any, default=None)  # 表单值


@to_json_decorator
@attr.s
class ApprovalDefinition(object):
    """审批定义对象
    """
    approval_name = attr.ib(type=str, default=None)
    forms = attr.ib(type=List[ApprovalForm], default=attr.Factory(list))  # type: List[ApprovalForm]
    nodes = attr.ib(type=List[ApprovalNode], default=attr.Factory(list))  # type: List[ApprovalNode]


@to_json_decorator
@attr.s
class ApprovalTask(object):
    """审批任务对象
    """
    id = attr.ib(type=str, default=None)  # 任务 ID
    user_id = attr.ib(type=str, default=None)  # 审批人，自动通过、自动拒绝 task user_id 为空
    status = attr.ib(type=ApprovalTaskStatus, default=None)  # 任务状态
    node_id = attr.ib(type=str, default=None)  # task 所属节点 id
    custom_node_id = attr.ib(type=str, default=None)  # task 所属节点自定义 id, 如果没设置自定义 id, 则不返回该字段
    type = attr.ib(type=ApprovalTaskTypeStatus, default=None)  # 任务类型
    start_time = attr.ib(type=int, default=None)  # 创建时间
    end_time = attr.ib(type=int, default=0)  # 结束时间，未完成为 0


@to_json_decorator
@attr.s
class ApprovalComment(object):
    """审批中的评论对象
    """
    id = attr.ib(type=str, default=None)  # 评论 ID
    user_id = attr.ib(type=str, default=None)  # 发表评论用户
    comment = attr.ib(type=str, default=None)  # 评论详情
    create_time = attr.ib(type=int, default=None)  # 创建时间


@to_json_decorator
@attr.s
class ApprovalTimeline(object):
    """审批动态
    """
    type = attr.ib(type=ApprovalTimelineType, default=None)  # 发生时间
    create_time = attr.ib(type=int, default=0)  # 发生时间
    user_id = attr.ib(type=str, default=None)  # 动态产生用户
    # 被抄送人列表
    user_id_list = attr.ib(type=List[str], default=None)  # type: List[str]
    task_id = attr.ib(type=str, default='')  # 产生动态关联的task_id
    comment = attr.ib(type=str, default='')  # 评论详情

    # type类型 - user_id_list 含义
    # TRANSFER - 被转交人
    # ADD_APPROVER_BEFORE - 被加签人
    # ADD_APPROVER - 被加签人
    # ADD_APPROVER_AFTER - 被加签人
    # DELETE_APPROVER - 被减签人

    # type类型 - user_id 含义
    # CC - 抄送人
    ext = attr.ib(type=dict, default=None)  # 动态其他信息，目前包括 user_id_list, user_id


@to_json_decorator
@attr.s
class ApprovalInstance(object):
    """审批实例对象
    """
    approval_code = attr.ib(type=str, default='')  # 审批定义唯一标识
    approval_name = attr.ib(type=str, default='')  # 审批定义名称
    start_time = attr.ib(type=int, default=0)  # 创建时间（毫秒）
    end_time = attr.ib(type=int, default=0)  # 结束时间（毫秒）（未结束为0）
    user_id = attr.ib(type=str, default='')  # 用户ID
    department_id = attr.ib(type=str, default='')  # 部门ID
    status = attr.ib(type=ApprovalInstanceStatus, default=None)  # 实例状态
    form = attr.ib(type=List[ApprovalForm], default=attr.Factory(list))  # type: List[ApprovalForm]
    # 任务列表
    task_list = attr.ib(type=List[ApprovalTask], default=attr.Factory(list))  # type: List[ApprovalTask]
    # 评论列表
    comment_list = attr.ib(type=List[ApprovalComment], default=attr.Factory(list))  # type: List[ApprovalComment]
    # 审批动态
    timeline = attr.ib(type=List[ApprovalTimeline], default=attr.Factory(list))  # type: List[ApprovalTimeline]
    serial_number = attr.ib(type=str, default='')  # 审批编号
