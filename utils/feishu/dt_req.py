# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import List

import attr

from utils.feishu.dt_contact import DepartmentUserCustomAttr, EmployeeType
from utils.feishu.dt_help import to_json, to_json_decorator
from utils.feishu.helper import pop_or_none


@to_json_decorator
@attr.s
class CreateDepartmentRequest(object):
    parent_id = attr.ib(type=str)  # 父部门 ID
    name = attr.ib(type=str)  # 部门名称
    # 自定义部门 ID。只能在创建部门时指定，不支持更新。企业内必须唯一，若不填该参数，将自动生成。不区分大小写，长度为 1 ~ 64 个字符。
    # 只能由数字、字母和 "_-@." 四种字符组成，且第一个字符必须是数字或字母
    id = attr.ib(type=str, default='')
    # 部门负责人 ID，支持通过 leader_user_id 或 leader_open_id 设置部门负责人，请求同时传递两个参数时按 leader_user_id 处理
    leader_open_id = attr.ib(type=str, default='')
    leader_user_id = attr.ib(type=str, default='')
    create_group_chat = attr.ib(type=bool, default=False)  # 是否同时创建部门群，默认为 false，不创建部门群


@to_json_decorator
@attr.s
class CreateUserRequest(object):
    """创建用户所需要的参数
    """

    # 必填
    name = attr.ib(type=str)  # 用户名
    mobile = attr.ib(type=str)  # 用户手机号
    # 新增用户所在部门，仅支持一个用户在一个部门下，需要有加入部门的通讯录权限
    department_ids = attr.ib(type=List[str])  # type: List[str]

    # 可选

    # 用户邮箱地址
    email = attr.ib(type=str, default=None)
    # 手机号码可见性，true 为可见，false 为不可见，目前默认为 true。不可见时，组织员工将无法查看该员工的手机号码
    mobile_visible = attr.ib(type=bool, default=None)
    # 用户所在城市
    city = attr.ib(type=str, default=None)
    # 用户所在国家
    country = attr.ib(type=str, default=None)
    # 性别，1:男，2:女
    gender = attr.ib(type=int, default=None)
    employee_type = attr.ib(type=EmployeeType, default=None)  # 员工类型。1:正式员工；2:实习生；3:外包；4:劳务；5:顾问
    join_time = attr.ib(type=int, default=None)  # 入职时间
    # 直接领导信息，支持通过 leader_user_id 或者 leader_open_id 设置直接领导，同时传递两个参数时按参数 leader_user_id 处理
    leader_open_id = attr.ib(type=str, default=None)
    leader_user_id = attr.ib(type=str, default=None)  # v1 需要转成 employee
    # 用户企业内唯一标识。
    # 自定义唯一标识不区分大小写，长度为 1 ~ 64 个字符。只能由数字、字母和 "_-@.“ 四种字符组成，且第一个字符必须是数字或字母。
    # 创建用户时可指定该唯一标识，指定的唯一标识不能修改。
    user_id = attr.ib(type=str, default=None)  # v1 需要转成 employee
    # 工号
    employee_no = attr.ib(type=str, default=None)
    # 是否发送邀请通知。该字段为 true 时， 添加用户成功后会往相应的邮箱或者 mobile 发送邀请通知
    need_send_notification = attr.ib(type=bool, default=None)
    # 自定义用户属性。
    # 该字段仅当企业管理员在企业管理后台开启了“允许开放平台API调用”时有效。
    # 传入的每个自定义用户属性需要包含平台生成的属性ID和要设置的属性值。
    # 当企业管理后台未开启“允许开放平台API调用”，以及传入的自定义用户属性 ID 不存在或者非法时，会忽略该条属性设置信息。
    custom_attrs = attr.ib(type=List[DepartmentUserCustomAttr],
                           default=attr.Factory(list))  # type: List[DepartmentUserCustomAttr]
    # 工位
    work_station = attr.ib(type=str, default=None)

    def v1_json(self):
        d = to_json(self)
        d['leader_employee_id'] = pop_or_none(d, 'leader_user_id')
        d['employee_id'] = pop_or_none(d, 'user_id')
        custom_attrs = pop_or_none(d, 'custom_attrs')
        custom = {}
        for i in custom_attrs:
            attr_id = pop_or_none(i, 'id')
            custom[attr_id] = i
        d['custom_attrs'] = custom
        return d


@to_json_decorator
@attr.s
class UpdateUserRequest(object):
    """更新用户所需要的参数
    """
    # 下面两个，必填一个
    user_id = attr.ib(type=str, default=None)
    open_id = attr.ib(type=str, default=None)

    # 选填
    name = attr.ib(type=str, default=None)  # 用户名
    mobile = attr.ib(type=str, default=None)  # 用户手机号
    # 新增用户所在部门，仅支持一个用户在一个部门下，需要有加入部门的通讯录权限
    department_ids = attr.ib(type=List[str], default=attr.Factory(list))  # type: List[str]
    is_frozen = attr.ib(type=bool, default=None)  # 是否冻结用户
    # 用户邮箱地址
    email = attr.ib(type=str, default=None)
    # 手机号码可见性，true 为可见，false 为不可见，目前默认为 true。不可见时，组织员工将无法查看该员工的手机号码
    mobile_visible = attr.ib(type=bool, default=None)
    # 用户所在城市
    city = attr.ib(type=str, default=None)
    # 用户所在国家
    country = attr.ib(type=str, default=None)
    # 性别，1:男，2:女
    gender = attr.ib(type=int, default=None)
    employee_type = attr.ib(type=EmployeeType, default=None)  # 员工类型。1:正式员工；2:实习生；3:外包；4:劳务；5:顾问
    join_time = attr.ib(type=int, default=None)  # 入职时间
    # 直接领导信息，支持通过 leader_user_id 或者 leader_open_id 设置直接领导，同时传递两个参数时按参数 leader_user_id 处理
    leader_open_id = attr.ib(type=str, default=None)
    leader_user_id = attr.ib(type=str, default=None)  # v1 需要转成 employee
    # 用户企业内唯一标识。
    # 自定义唯一标识不区分大小写，长度为 1 ~ 64 个字符。只能由数字、字母和 "_-@.“ 四种字符组成，且第一个字符必须是数字或字母。
    # 创建用户时可指定该唯一标识，指定的唯一标识不能修改。
    # 工号
    employee_no = attr.ib(type=str, default=None)
    # 是否发送邀请通知。该字段为 true 时， 添加用户成功后会往相应的邮箱或者 mobile 发送邀请通知
    need_send_notification = attr.ib(type=bool, default=None)
    # 自定义用户属性。
    # 该字段仅当企业管理员在企业管理后台开启了“允许开放平台API调用”时有效。
    # 传入的每个自定义用户属性需要包含平台生成的属性ID和要设置的属性值。
    # 当企业管理后台未开启“允许开放平台API调用”，以及传入的自定义用户属性 ID 不存在或者非法时，会忽略该条属性设置信息。
    custom_attrs = attr.ib(type=List[DepartmentUserCustomAttr],
                           default=attr.Factory(list))  # type: List[DepartmentUserCustomAttr]
    # 工位
    work_station = attr.ib(type=str, default=None)

    def v1_json(self):
        d = to_json(self)
        d['employee_id'] = pop_or_none(d, 'user_id')
        d['leader_employee_id'] = pop_or_none(d, 'leader_user_id')
        custom_attrs = pop_or_none(d, 'custom_attrs')
        custom = {}
        for i in custom_attrs:
            attr_id = pop_or_none(i, 'id')
            custom[attr_id] = i
        d['custom_attrs'] = custom
        return d
