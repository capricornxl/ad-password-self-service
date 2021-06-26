# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from enum import Enum
from typing import List

import attr

from utils.feishu.dt_code import I18NTitle, SimpleUser
from utils.feishu.dt_help import to_json_decorator, to_lower_converter


@to_json_decorator
@attr.s
class SimpleDepartment(object):
    """部门对象
    """
    id = attr.ib(type=str, default='')
    name = attr.ib(type=str, default='')
    parent_id = attr.ib(type=str, default='')


@to_json_decorator
@attr.s
class DepartmentUnit(object):
    # 部门对应单元
    id = attr.ib(type=str, default='')  # 单元ID
    unit_type = attr.ib(type=str, default='')  # 单元类型
    unit_name = attr.ib(type=str, default='')  # 单元名称


@to_json_decorator
@attr.s
class Department(object):
    chat_id = attr.ib(type=str, default='')  # 部门群ID
    dept_units = attr.ib(type=list, default=attr.Factory(list))  # type: List[DepartmentUnit]
    has_child = attr.ib(type=bool, default=False)  # 是否有子部门
    id = attr.ib(type=str, default='')  # 部门ID
    leader = attr.ib(type=SimpleUser, default=None)  # 部门负责人信息
    member_count = attr.ib(type=int, default=0)  # 部门成员数量
    name = attr.ib(type=str, default='')  # 部门名称
    parent_id = attr.ib(type=str, default='')  # 父部门 ID
    status = attr.ib(type=int, default=0)  # 部门状态，0 无效，1 有效


@to_json_decorator
@attr.s
class DepartmentUserStatus(object):
    is_frozen = attr.ib(type=bool, default=False)  # 用户是否被冻结
    is_resigned = attr.ib(type=bool, default=False)  # 用户是否离职
    is_activated = attr.ib(type=bool, default=False)  # 用户账号是否已激活


@to_json_decorator
@attr.s
class DepartmentUserAvatar(object):
    avatar_72 = attr.ib(type=str, default='')
    avatar_240 = attr.ib(type=str, default='')
    avatar_640 = attr.ib(type=str, default='')
    avatar_origin = attr.ib(type=str, default='')


class EmployeeType(Enum):
    full_time = 1  # 正式员工
    internship = 2  # 实习生
    outsourcing = 3  # 外包
    labor = 4  # 劳务
    consultant = 5  # 顾问


class Gender(Enum):
    # 性别，未设置不返回该字段。1:男；2:女
    man = 1
    woman = 2


@to_json_decorator
@attr.s
class SimpleUserWithPosition(SimpleUser):
    position_code = attr.ib(type=str, default='')  # 岗位标识


@to_json_decorator
@attr.s
class DepartmentUserPosition(object):
    position_code = attr.ib(type=str, default='')  # 岗位标识
    position_name = attr.ib(type=str, default='')  # 岗位名称
    department_id = attr.ib(type=str, default='')  # 岗位对应的部门ID，必须是用户所属的部门中的一个
    is_major = attr.ib(type=bool, default=False)  # 是否为主岗位，每个用户只有一个主岗位
    leader = attr.ib(type=SimpleUserWithPosition, default=None)  # 对应岗位上的直接上级


@to_json_decorator
@attr.s
class DepartmentUserOrder(object):
    """用户的所有部门排序信息，每个部门都有独立的排序信息"""

    department_id = attr.ib(type=str, default='')  # 排序信息对应的部门 ID
    user_order = attr.ib(type=int, default=0)  # 当前用户在对应部门中所有用户间的排序序号
    department_order = attr.ib(type=int, default=0)  # 对应部门在当前用户所有部门间的排序序号


@to_json_decorator
@attr.s
class DepartmentUserCustomAttrValue(object):
    text = attr.ib(type=str, default='')  # 文字属性的值，属性类型为text时，返回此字段
    url = attr.ib(type=str, default='')  # URL 属性的值，属性类型为 href 时，返回此字段
    pc_url = attr.ib(type=str, default='')  # URL 属性的 PC 端 URL 值，属性类型为 href 时，返回此字段


@to_json_decorator
@attr.s
class DepartmentUserCustomAttr(object):
    """用户的自定义属性信息。企业开放了自定义用户属性且为该用户设置了自定义属性的值，才会返回该字段"""

    id = attr.ib(type=str, default='')  # 排序信息对应的部门ID
    type = attr.ib(type=str, default='', converter=to_lower_converter)  # 属性类型，目前有text和href
    value = attr.ib(type=DepartmentUserCustomAttrValue, default=None)  # 属性值
    i18n_names = attr.ib(type=I18NTitle, default=None)  # 国际化属性名称


@to_json_decorator
@attr.s
class DepartmentUser(object):
    name = attr.ib(type=str, default='')  # 用户名
    en_name = attr.ib(type=str, default='')  # 英文名
    user_id = attr.ib(type=str, default='')  # user_id，应用商店应用不返回
    employee_no = attr.ib(type=str, default='')  # 工号
    open_id = attr.ib(type=str, default='')  # open_id
    status = attr.ib(type=DepartmentUserStatus, default=None)  # 用户状态
    employee_type = attr.ib(type=EmployeeType, default=None)  # 员工类型。1:正式员工；2:实习生；3:外包；4:劳务；5:顾问
    avatar = attr.ib(type=DepartmentUserAvatar, default=None)  # 头像
    gender = attr.ib(type=Gender, default=None)  # 性别，未设置不返回该字段。1:男；2:女
    email = attr.ib(type=str, default='')  # 用户邮箱地址，已申请邮箱权限才返回该字段
    mobile = attr.ib(type=str, default='')  # 用户手机号，已申请"获取用户手机号"权限的企业自建应用返回该字段
    country = attr.ib(type=str, default='')  # 用户所在国家
    city = attr.ib(type=str, default='')  # 用户所在城市
    work_station = attr.ib(type=str, default='')  # 工位
    is_tenant_manager = attr.ib(type=bool, default=False)  # 是否是企业超级管理员
    join_time = attr.ib(type=int, default=0)  # 入职时间，未设置不返回该字段
    update_time = attr.ib(type=int, default=0)  # 更新时间
    leader = attr.ib(type=SimpleUser, default=None)  # 用户直接上级
    # 用户所在部门 ID，用户可能同时存在于多个部门
    departments = attr.ib(type=List[str], default=attr.Factory(list))  # type: List[str]
    # 用户岗位
    positions = attr.ib(type=List[DepartmentUserPosition],
                        default=attr.Factory(list))  # type: List[DepartmentUserPosition]
    # 用户的所有部门排序信息，每个部门都有独立的排序信息
    orders = attr.ib(type=List[DepartmentUserOrder], default=attr.Factory(list))  # type: List[DepartmentUserOrder]
    # 用户的自定义属性信息。企业开放了自定义用户属性且为该用户设置了自定义属性的值，才会返回该字段
    custom_attrs = attr.ib(type=List[DepartmentUserCustomAttr],
                           default=attr.Factory(list))  # type: List[DepartmentUserCustomAttr]


@to_json_decorator
@attr.s
class ContactAsyncChildTaskInfo(object):
    # 以下字段适用于在用户操作时

    code = attr.ib(type=int, default=0)  # 子任务返回码，非 0 表示失败
    msg = attr.ib(type=str, default='')  # 子任务返回码的描述
    action = attr.ib(type=int, default=0)  # 子任务进行的操作，1:添加，2:更新，执行失败时没有此字段
    name = attr.ib(type=str, default='')  # 子任务请求名称，用户操作时为用户名，部门操作时为部门名
    email = attr.ib(type=str, default='')  # 请求时的用户邮箱地址
    mobile = attr.ib(type=str, default='')  # 请求时的用户手机号
    user_id = attr.ib(type=str, default='')  # 请求时的用户企业内唯一标识或自动生成的唯一标识
    open_id = attr.ib(type=str, default='')  # 生成的用户open_id，执行失败时没有此字段
    # 请求时的用户所在部门
    departments = attr.ib(type=List[str], default=attr.Factory(list))  # type: List[str]

    # 以下字段适用于在部门操作时

    department_id = attr.ib(type=str, default='')  # 请求时的自定义部门 ID 或生成的部门 ID
    parent_id = attr.ib(type=str, default='')  # 请求时的父部门 ID
    chat_id = attr.ib(type=str, default='')  # 部门群 ID，如果存在部门群则返回该字段


@to_json_decorator
@attr.s
class ContactAsyncTaskResult(object):
    task_id = attr.ib(type=str, default='')  # 异步任务 ID
    type = attr.ib(type=str, default='')  # 任务类型，目前有两种，添加用户为add_user，添加部门为 add_department
    # 任务当前执行状态，小于9:正在执行过程中，9:执行完成，10:执行失败，11:超出当前人数限制无法执行
    status = attr.ib(type=int, default=0)
    progress = attr.ib(type=int, default=0)  # 任务进度百分比
    total_num = attr.ib(type=int, default=0)  # 任务总条数
    success_num = attr.ib(type=int, default=0)  # 任务当前执行成功的条数
    fail_num = attr.ib(type=int, default=0)  # 任务当前执行失败的条数
    create_time = attr.ib(type=int, default=0)  # 任务创建时间，以秒为单位的Unix时间戳
    finish_time = attr.ib(type=int, default=0)  # 任务完成时间，以秒为单位的Unix时间戳，当任务状态小于8时没有此字段
    # 任务执行结果列表，当任务状态不为 9 时没有此字段，执行结果和添加任务时的请求体按顺序对应
    task_info = attr.ib(type=List[ContactAsyncChildTaskInfo],
                        default=attr.Factory(list))  # type: List[ContactAsyncChildTaskInfo]


@to_json_decorator
@attr.s
class Role(object):
    id = attr.ib(type=str, default='')  # 角色 ID
    name = attr.ib(type=str, default='')  # 角色名称
