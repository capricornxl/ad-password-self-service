# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Dict, List

from utils.feishu.dt_code import SimpleUser
from utils.feishu.dt_contact import (ContactAsyncTaskResult, Department, DepartmentUser, DepartmentUserCustomAttr, Role,
                               SimpleDepartment)
from utils.feishu.dt_help import make_datatype
from utils.feishu.dt_req import CreateDepartmentRequest, CreateUserRequest, UpdateUserRequest
from utils.feishu.exception import LarkInvalidArguments, OpenLarkException, gen_exception
from utils.feishu.helper import join_dict, join_url

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIContactMixin(object):
    def get_contact_scope(self):
        """获取通讯录授权范围

        :type self: OpenLark
        :return: is_visible_to_all, department_ids, users
        :rtype: (bool, list[str], list[SimpleUser])

        该接口用于获取应用被授权可访问的通讯录范围，包括可访问的部门列表及用户列表。

        授权范围为全员时，返回的部门列表为该企业所有的一级部门；
        否则返回的部门为管理员在设置授权范围时勾选的部门（不包含勾选部门的子部门）。

        https://open.feishu.cn/document/ukTMukTMukTM/ugjNz4CO2MjL4YzM

        https://bytedance.feishu.cn/docs/doccnOcR1fnxBACchoY9tlg7Amg#
        """
        url = self._gen_request_url('/open-apis/contact/v2/scope/get')
        res = self._get(url, with_tenant_token=True)
        data = res['data']
        department_ids = data.get('authed_departments', [])  # type: List[str]
        users = [make_datatype(SimpleUser, i) for i in data.get('authed_users', [])]  # type: List[SimpleUser]
        is_visible_to_all = '0' in department_ids

        return is_visible_to_all, department_ids, users

    def create_department(self, parent_id, name, custom_id=None, leader_open_id=None, leader_user_id=None,
                          create_group_chat=False):
        """新增部门

        :type self: OpenLark
        :param parent_id: 父部门 ID
        :type parent_id: str
        :param name: 部门名称
        :type name: str
        :param name: 部门名称
        :type name: str
        :param custom_id: 自定义部门 ID。
            该字段企业内必须唯一，不区分大小写，长度为 1 ~ 64 个字符。只能由数字、字母和“_-@.”四种字符组成，且第一个字符必须是数字或字母。
            创建部门时指定的 ID 后续不允许修改，不指定该字段由系统自动生成 ID，系统生成的 ID 仅允许修改一次。
        :type custom_id: str
        :param leader_open_id: 部门领导 ID，支持通过 leader_user_id 或者 leader_open_id 设置部门领导，
            请求同时传递两个参数时按 leader_user_id 处理
        :type leader_open_id: str
        :param leader_user_id: 部门领导 ID，支持通过 leader_user_id 或者 leader_open_id 设置部门领导，
            请求同时传递两个参数时按 leader_user_id 处理
        :type leader_user_id: str
        :param create_group_chat: 是否同时创建部门群，默认不创建部门群
        :type create_group_chat: bool
        :return: 创建后的部门
        :rtype: Department

        该接口用于向通讯录中增加新的部门。

        调用该接口需要具有该部门父部门的通讯录操作权限。

        应用商店应用无权限调用接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uYzNz4iN3MjL2czM
        """
        url = self._gen_request_url('/open-apis/contact/v1/department/add')
        body = {
            'name': name,
            'parent_id': parent_id,
        }
        body = join_dict(body, [
            ('id', custom_id),
            ('leader_open_id', leader_open_id),
            ('leader_employee_id', leader_user_id),
            ('create_group_chat', create_group_chat)
        ])
        res = self._post(url, body=body, with_tenant_token=True)

        return _make_v1_department_info(res)  # type: Department

    def batch_create_department(self, create_params):
        """批量新增部门

        :type self: OpenLark
        :param create_params: 批量创建参数
        :type create_params: list[CreateDepartmentRequest]
        :return: 生成的异步任务 ID，使用「查询批量任务执行状态」查询状态
        :rtype: str

        该接口用于向通讯录中批量新增多个部门。

        调用该接口需要具有所有新增部门父部门的通讯录写入权限。

        应用商店应用无权限调用此接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uMDOwUjLzgDM14yM4ATN
        """
        url = self._gen_request_url('/open-apis/contact/v2/department/batch_add')
        body = []
        for i in create_params:
            if isinstance(i, CreateDepartmentRequest):
                i = i.json()
            d = {}
            for k, v in i.items():
                if v:
                    d[k] = v
            body.append(d)
        body = {
            'departments': body,
        }

        res = self._post(url, body=body, with_tenant_token=True)
        return res['data'].get('task_id')  # type: str

    def delete_department(self, department_id):
        """删除部门

        :type self: OpenLark
        :param department_id: 待删除部门 ID
        :type department_id: str

        该接口用于从通讯录中删除部门。

        调用该接口需要具有该部门或者其所在部门的通讯录权限。

        应用商店应用无权限调用此接口。

        https://open.feishu.cn/document/ukTMukTMukTM/ugzNz4CO3MjL4czM
        """
        url = self._gen_request_url('/open-apis/contact/v1/department/delete')
        body = {
            'id': department_id
        }
        self._post(url, body=body, with_tenant_token=True)

    def update_department(self, department_id, parent_id=None, name=None, custom_id=None, leader_open_id=None,
                          leader_user_id=None, create_group_chat=None):
        """更新部门

        :type self: OpenLark
        :param department_id: 部门ID
        :type department_id: str
        :param parent_id: 父部门 ID
        :type parent_id: str
        :param name: 部门名称
        :type name: str
        :param name: 部门名称
        :type name: str
        :param custom_id: 仅允许创建部门时未指定自定义 ID 的部门修改该 ID一次。新的自定义部门 ID。
            该字段企业内必须唯一，不区分大小写，长度为 1 ~ 64 个字符。只能由数字、字母和“_-@.”四种字符组成，且第一个字符必须是数字或字母。
            创建部门时指定的 ID 后续不允许修改，不指定该字段由系统自动生成 ID，系统生成的 ID 仅允许修改一次。
        :type custom_id: str
        :param leader_open_id: 部门领导 ID，支持通过 leader_user_id 或者 leader_open_id 设置部门领导，
            请求同时传递两个参数时按 leader_user_id 处理
        :type leader_open_id: str
        :param leader_user_id: 部门领导 ID，支持通过 leader_user_id 或者 leader_open_id 设置部门领导，
            请求同时传递两个参数时按 leader_user_id 处理
        :type leader_user_id: str
        :param create_group_chat: 是否同时创建部门群，默认不创建部门群
        :type create_group_chat: bool
        :return: 创建后的部门
        :rtype: Department

        该接口用于更新通讯录中部门的信息。

        调用该接口需要具有该部门父部门的通讯录操作权限。

        应用商店应用无权限调用接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uczNz4yN3MjL3czM
        """
        url = self._gen_request_url('/open-apis/contact/v1/department/update')
        body = join_dict({}, [
            ('id', department_id),
            ('name', name),
            ('parent_id', parent_id),
            ('leader_open_id', leader_open_id),
            ('leader_employee_id', leader_user_id),
            ('create_group_chat', create_group_chat),
            ('new_id', custom_id),
        ])
        res = self._post(url, body=body, with_tenant_token=True)

        return _make_v1_department_info(res)  # type: Department

    def get_department(self, department_id):
        """获取部门详情

        :type self: OpenLark
        :param department_id: 部门ID
        :type department_id: str
        :return: 创建后的部门
        :rtype: Department

        该接口用于获取部门详情信息。

        https://open.feishu.cn/document/ukTMukTMukTM/uAzNz4CM3MjLwczM
        """
        url = self._gen_request_url('/open-apis/contact/v1/department/info/get')
        url = join_url(url, [('department_id', department_id)], sep='?')
        res = self._get(url, with_tenant_token=True)

        return _make_v1_department_info(res)  # type: Department

    def get_child_department_simple_list(self, department_id, page_size=20, page_token='', fetch_child=False):
        """获取当前部门子部门列表

        :type self: OpenLark
        :param department_id: 部门 ID
        :type department_id: str
        :param page_size: 分页大小，最大支持 100
        :type page_size: str
        :param page_token: 分页标记，分页查询还有更多群时会同时返回新的 page_token, 下次遍历可采用该 page_token 获取更多
        :type page_token: str
        :param fetch_child: 是否递归返回子部门列表，默认不递归
        :type fetch_child: bool
        :return: has_more, page_token, departments
        :rtype: (bool, str, list[SimpleDepartment])

        获取当前部门子部门列表

        https://open.feishu.cn/document/ukTMukTMukTM/ugzN3QjL4czN04CO3cDN

        https://bytedance.feishu.cn/docs/doccnOcR1fnxBACchoY9tlg7Amg#
        """
        url = self._gen_request_url('/open-apis/contact/v2/department/simple/list')
        qs = [
            ('id', department_id),
            ('page_size', page_size),
            ('page_token', page_token),
            ('fetch_child', fetch_child)
        ]
        url = join_url(url, qs, sep='?')
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        has_more = data.get('has_more', False)
        page_token = data.get('page_token', '')
        department_ids = [make_datatype(SimpleDepartment, i) for i in data.get('departments', [])]
        return has_more, page_token, department_ids

    def get_child_department_id_list(self, department_id):
        """获取子部门 ID 列表

        :type self: OpenLark
        :param department_id: 部门 ID
        :type department_id str
        :return: 部门 ID 列表
        :rtype: list[str]

        该接口用于获取子部门 ID 列表，只返回授权的部门列表。

        企业根部门 ID 为 0，当参数指定的部门为根部门时，如果授权范围为全员，返回该企业的所有一级部门；
        否则返回管理员在设置通讯录授权范围时勾选的部门（不包含子部门）。
        指定获取特定部门（部门 ID 非 0）的部门列表时，需要具有该部门的通讯录授权，返回部门列表为该部门所有的子部门。

        https://open.feishu.cn/document/ukTMukTMukTM/ukjNz4SO2MjL5YzM
        """
        url = self._gen_request_url('/open-apis/contact/v1/department/list?department_id=' + department_id)
        res = self._get(url, with_tenant_token=True)
        department_ids = res.get('data', {}).get('departments_list', [])  # type: List[str]
        return department_ids

    def batch_get_department_detail(self, department_ids):
        """批量获取部门详情，只返回权限范围内的部门。

        :type self: OpenLark
        :param department_ids: 部门 ID 列表
        :type department_ids: list[str]
        :return: departments, errors
        :rtype: (dict[str, Department], dict[str, OpenLarkException])

        批量获取部门详情，只返回权限范围内的部门。

        https://open.feishu.cn/document/ukTMukTMukTM/uczN3QjL3czN04yN3cDN

        https://bytedance.feishu.cn/docs/doccnOcR1fnxBACchoY9tlg7Amg#
        """
        if isinstance(department_ids, str):
            department_ids = [department_ids]

        qs = '&'.join(['ids={}'.format(i) for i in department_ids])
        url = self._gen_request_url('/open-apis/contact/v2/department/detail/batch_get?' + qs)
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        departments = {}  # type: Dict[str, Department]
        for i in data.get('departments', []):
            dept = make_datatype(Department, i)  # type: Department
            departments[dept.id] = dept

        errors = {}  # type: Dict[str, OpenLarkException]
        for i in data.get('errors', []):
            e = gen_exception(code=i.get('code'), url='', msg=i.get('msg'))
            errors[i.get('id', '')] = e
        return departments, errors

    def get_department_simple_user_list(self, department_id, page_size=20, page_token='', fetch_child=False):
        """获取部门用户 ID 列表

        :type self: OpenLark
        :param department_id: 部门 ID
        :type department_id: str
        :param page_size: 分页大小，最大支持 100
        :type page_size: str
        :param page_token: 分页标记，分页查询还有更多群时会同时返回新的 page_token, 下次遍历可采用该 page_token 获取更多
        :type page_token: str
        :param fetch_child: 是否递归返回子部门列表，默认不递归
        :type fetch_child: bool
        :return: has_more, page_token, users
        :rtype: (bool, str, list[SimpleUser])

        获取部门用户列表，需要有该部门的通讯录授权

        https://open.feishu.cn/document/ukTMukTMukTM/uEzNz4SM3MjLxczM

        https://bytedance.feishu.cn/docs/doccnOcR1fnxBACchoY9tlg7Amg#
        """
        url = self._gen_request_url('/open-apis/contact/v2/department/user/list')
        qs = [
            ('id', department_id),
            ('page_size', page_size),
            ('page_token', page_token),
            ('fetch_child', fetch_child)
        ]
        url = join_url(url, qs, sep='?')
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        has_more = data.get('has_more', False)
        page_token = data.get('page_token', '')
        users = [make_datatype(SimpleUser, i) for i in data.get('users', [])]
        return has_more, page_token, users

    def get_department_detail_user_list(self, department_id, page_size=20, page_token='', fetch_child=False):
        """获取部门用户详情列表

        :type self: OpenLark
        :param department_id: 部门 ID
        :type department_id: str
        :param page_size: 分页大小，最大支持 100
        :type page_size: str
        :param page_token: 分页标记，分页查询还有更多群时会同时返回新的 page_token, 下次遍历可采用该 page_token 获取更多
        :type page_token: str
        :param fetch_child: 是否递归返回子部门列表，默认不递归
        :type fetch_child: bool
        :return: has_more, page_token, departments
        :rtype: (bool, str, list[DepartmentUser])

        获取部门用户详情，需要有该部门的通讯录授权。

        https://open.feishu.cn/document/ukTMukTMukTM/uYzN3QjL2czN04iN3cDN

        https://bytedance.feishu.cn/docs/doccnOcR1fnxBACchoY9tlg7Amg#
        """
        url = self._gen_request_url('/open-apis/contact/v2/department/user/detail/list')
        qs = [
            ('id', department_id),
            ('page_token', page_token),
            ('page_size', page_size),
            ('fetch_child', fetch_child),
        ]

        url = join_url(url, qs, sep='?')
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        has_more = data.get('has_more', False)
        page_token = data.get('page_token', '')
        users = [make_datatype(DepartmentUser, i) for i in data.get('users', [])]
        return has_more, page_token, users

    def create_user(self, create_user_request):
        """新增用户

        :type self: OpenLark
        :param create_user_request: 创建参数
        :type create_user_request: CreateUserRequest
        :return: user
        :rtype: DepartmentUser

        该接口用于向通讯录中新增用户。

        调用该接口需要具有用户所在部门的通讯录写入权限。

        应用商店应用无权限调用此接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uMzNz4yM3MjLzczM
        """
        url = self._gen_request_url('/open-apis/contact/v1/user/add')

        if isinstance(create_user_request, CreateUserRequest):
            create_user_request = create_user_request.v1_json()  # type: dict

        body = join_dict({}, list(create_user_request.items()))
        res = self._post(url, body=body, with_tenant_token=True)

        user_info = res['data'].get('user_info', {})
        return _make_v1_user(user_info)

    def batch_create_user(self, create_user_request_list):
        """批量新增用户

        :type self: OpenLark
        :param create_user_request_list: 创建参数
        :type create_user_request_list: list[CreateUserRequest]
        :return: task_id
        :rtype: str

        该接口用于向通讯录中批量新增多个用户。

        调用该接口需要具有用户所在部门的通讯录写入权限。

        应用商店应用无权限调用此接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uMzNz4yM3MjLzczM
        """
        url = self._gen_request_url('/open-apis/contact/v2/user/batch_add')

        users = []
        need_send_notification = None
        for create_user_request in create_user_request_list:
            if isinstance(create_user_request, CreateUserRequest):
                create_user_request = create_user_request.json()
            if isinstance(create_user_request, dict) and 'need_send_notification' in create_user_request:
                if create_user_request['need_send_notification'] is not None:
                    need_send_notification = need_send_notification or create_user_request['need_send_notification']
                del create_user_request['need_send_notification']
            users.append(create_user_request)

        body = {
            'users': users,
            'need_send_notification': need_send_notification,
        }
        res = self._post(url, body=body, with_tenant_token=True)
        return res['data'].get('task_id')  # type: str

    def delete_user(self, user_user_id=None, user_open_id=None,
                    department_chat_acceptor_user_id=None,
                    department_chat_acceptor_open_id=None,
                    external_chat_acceptor_user_id=None,
                    external_chat_acceptor_open_id=None,
                    docs_acceptor_user_id=None,
                    docs_acceptor_open_id=None,
                    calendar_acceptor_user_id=None,
                    calendar_acceptor_open_id=None,
                    application_acceptor_user_id=None,
                    application_acceptor_open_id=None):
        """删除用户

        :type self: OpenLark
        :param user_user_id: 被删除用户，请求至少包含被删除用户的 user_id 或者 open_id 之一，同时传递两个参数时按 user_id 处理
        :type user_user_id: str
        :param user_open_id: 被删除用户，请求至少包含被删除用户的 user_id 或者 open_id 之一，同时传递两个参数时按 user_id 处理
        :type user_open_id: str
        :param department_chat_acceptor_user_id: 部门群接收者，
            被删除用户为部门群群主时，转让群主给指定接收者，不指定接收者则默认转让给群内第一个入群的人
        :type department_chat_acceptor_user_id: str
        :param department_chat_acceptor_open_id: 部门群接收者，
            被删除用户为部门群群主时，转让群主给指定接收者，不指定接收者则默认转让给群内第一个入群的人
        :type department_chat_acceptor_open_id: str
        :param external_chat_acceptor_user_id: 外部群接收者，
            被删除用户为外部群群主时，转让群主给指定接收者，不指定接收者则默认转让给群内与被删除用户在同一组织的第一个入群的人，
            如果组织内只有该用户在群里，则解散外部群
        :type external_chat_acceptor_user_id: str
        :param external_chat_acceptor_user_id: 外部群接收者，
            被删除用户为外部群群主时，转让群主给指定接收者，不指定接收者则默认转让给群内与被删除用户在同一组织的第一个入群的人，
            如果组织内只有该用户在群里，则解散外部群
        :type external_chat_acceptor_user_id: str
        :param external_chat_acceptor_open_id: 文档接收者
            用户被删除时，其拥有的文档转让给接收者，不指定接收者则默认转让给直接领导，如果无直接领导则直接删除文档资源
        :type external_chat_acceptor_open_id: str
        :param docs_acceptor_user_id: 文档接收者
            用户被删除时，其拥有的文档转让给接收者，不指定接收者则默认转让给直接领导，如果无直接领导则直接删除文档资源
        :type docs_acceptor_user_id: str
        :param docs_acceptor_open_id: 文档接收者
            用户被删除时，其拥有的文档转让给接收者，不指定接收者则默认转让给直接领导，如果无直接领导则直接删除文档资源
        :type docs_acceptor_open_id: str
        :param calendar_acceptor_user_id: 日程接收者
            用户被删除时，其拥有的日程转让给接收者，不指定接收者则默认转让给直接领导，如果无直接领导则直接删除日程资源
        :type calendar_acceptor_user_id: str
        :param calendar_acceptor_open_id: 日程接收者
            用户被删除时，其拥有的日程转让给接收者，不指定接收者则默认转让给直接领导，如果无直接领导则直接删除日程资源
        :type calendar_acceptor_open_id: str
        :param application_acceptor_user_id: 应用接收者
            用户被删除时，其创建的应用转让给接收者，不指定接收者则默认转让给直接领导，如果无直接领导则不会转移应用，会造成应用不可用
        :type application_acceptor_user_id: str
        :param application_acceptor_open_id: 应用接收者
            用户被删除时，其创建的应用转让给接收者，不指定接收者则默认转让给直接领导，如果无直接领导则不会转移应用，会造成应用不可用
        :type application_acceptor_open_id: str

        该接口用于从通讯录中删除用户。

        调用该接口需要具有该用户或者用户所在部门的通讯录权限。

        应用商店应用无权限调用接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uUzNz4SN3MjL1czM
        """
        if not user_user_id and not user_open_id:
            raise LarkInvalidArguments(msg='empty user user_id and open_id')

        url = self._gen_request_url('/open-apis/contact/v1/user/delete')
        body = {
            'employee_id': user_user_id,
            'open_id': user_open_id,
            'department_chat_acceptor': {
                'employee_id': department_chat_acceptor_user_id,
                'open_id': department_chat_acceptor_open_id,
            },
            'external_chat_acceptor': {
                'employee_id': external_chat_acceptor_user_id,
                'open_id': external_chat_acceptor_open_id,
            },
            'docs_acceptor': {
                'employee_id': docs_acceptor_user_id,
                'open_id': docs_acceptor_open_id,
            },
            'calendar_acceptor': {
                'employee_id': calendar_acceptor_user_id,
                'open_id': calendar_acceptor_open_id,
            },
            'application_acceptor': {
                'employee_id': application_acceptor_user_id,
                'open_id': application_acceptor_open_id,
            },
        }

        self._post(url, body=body, with_tenant_token=True)

    def update_user(self, update_user_request):
        """更新用户

        :type self: OpenLark
        :param update_user_request: 创建参数
        :type update_user_request: UpdateUserRequest
        :return: user
        :rtype: DepartmentUser

        该接口用于更新通讯录中用户信息。

        调用该接口需要具有用户所在部门的通讯录写入权限。

        应用商店应用无权限调用此接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uMzNz4yM3MjLzczM
        """
        url = self._gen_request_url('/open-apis/contact/v1/user/update')

        if isinstance(update_user_request, UpdateUserRequest):
            update_user_request = update_user_request.v1_json()

        body = join_dict({}, list(update_user_request.items()))
        self._post(url, body=body, with_tenant_token=True)

    def batch_get_department_detail_user(self, user_ids=None, open_ids=None):
        """批量获取用户详细信息

        :type self: OpenLark
        :param user_ids: 用户 UserID 列表
        :type user_ids: list[str]
        :param open_ids: 用户 OpenID 列表
        :type open_ids: list[str]
        :return: has_more, page_token, departments
        :rtype: (Dict[str, DepartmentUser], Dict[str, OpenLarkException])

        批量获取用户信息详情，需具有用户所在部门或者用户的通讯录权限。

        https://open.feishu.cn/document/ukTMukTMukTM/ugjNz4CO2MjL4YzM

        https://bytedance.feishu.cn/docs/doccnOcR1fnxBACchoY9tlg7Amg#
        """
        if user_ids and open_ids:
            raise LarkInvalidArguments(msg='only need user_ids or open_ids')
        elif not user_ids and not open_ids:
            raise LarkInvalidArguments(msg='need user_ids or open_ids')

        qs = ''
        user_key = ''
        if user_ids:
            qs = '&'.join(['user_ids={}'.format(i) for i in user_ids])
            user_key = 'user_id'
        elif open_ids:
            qs = '&'.join(['open_ids={}'.format(i) for i in open_ids])
            user_key = 'open_id'

        url = self._gen_request_url('/open-apis/contact/v2/user/batch_get')
        url = url + '?' + qs
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        users = {}  # type: Dict[str, DepartmentUser]
        for i in data.get('users', []):
            user = make_datatype(DepartmentUser, i)
            users[getattr(user, user_key)] = user

        errors = {}  # type: Dict[str, OpenLarkException]
        for i in data.get('errors', []):
            e = gen_exception(code=i.get('code'), url='', msg=i.get('msg'))
            errors[i.get('id', '')] = e
        return users, errors

    def get_tenant_custom_attr(self):
        """获取企业自定义属性信息

        :type self: OpenLark
        :return: is_open, attrs
        :rtype: (bool, list[DepartmentUserCustomAttr])

        https://open.feishu.cn/document/ukTMukTMukTM/ucTN3QjL3UzN04yN1cDN

        https://bytedance.feishu.cn/docs/doccnOcR1fnxBACchoY9tlg7Amg#
        """
        url = self._gen_request_url('/open-apis/contact/v2/tenant/custom_attr/get')
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        is_open = data.get('is_open', False)
        attrs = [make_datatype(DepartmentUserCustomAttr, i) for i in data.get('custom_attrs', [])]
        return is_open, attrs

    def get_contact_task(self, task_id):
        """查询批量任务执行状态

        :type self: OpenLark
        :param task_id: 任务id
        :type task_id: str
        :return: result
        :rtype: ContactAsyncTaskResult

        该接口用于查询通讯录异步任务当前的执行状态以及执行结果。

        调用该接口需要具有通讯录写入权限。

        应用商店应用无权限调用此接口。

        https://open.feishu.cn/document/ukTMukTMukTM/uUDOwUjL1gDM14SN4ATN
        """
        url = self._gen_request_url('/open-apis/contact/v2/task/get?task_id={}'.format(task_id))
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        return make_datatype(ContactAsyncTaskResult, data)  # type: ContactAsyncTaskResult

    def get_admin_scope(self, user_id=None, open_id=None):
        """获取应用管理员管理范围

        :type self: OpenLark
        :param user_id:
        :type user_id: str
        :param open_id:
        :type open_id: str
        :return: is_all, department_ids
            当 is_all 为 true 时，不返回 department_ids
        :rtype: (bool, list[str])

        该接口用于获取应用管理员的管理范围，即该应用管理员能够管理哪些部门。

        https://open.feishu.cn/document/ukTMukTMukTM/uMzN3QjLzczN04yM3cDN
        """

        url = self._gen_request_url('/open-apis/contact/v1/user/admin_scope/get')
        if user_id:
            url = '{}?employee_id={}'.format(url, user_id)
        elif open_id:
            url = '{}?open_id={}'.format(url, open_id)
        else:
            raise LarkInvalidArguments(msg='empty user_id and open_id')

        res = self._get(url, with_tenant_token=True)
        data = res['data']

        is_all = data.get('is_all')
        department_ids = data.get('department_list', [])
        return is_all, department_ids

    def get_role_list(self):
        """获取角色列表

        :type self: OpenLark
        :return: role_list
        :rtype: list[Role]

        该接口用于获取企业的用户角色列表。调用该接口的应用需要具有当前企业通讯录的读取或者更新权限。

        https://open.feishu.cn/document/ukTMukTMukTM/uYzMwUjL2MDM14iNzATN
        """

        url = self._gen_request_url('/open-apis/contact/v2/role/list')
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        return [make_datatype(Role, i) for i in data.get('role_list', [])]  # type: List[Role]

    def get_role_user_list(self, role_id, page_size=20, page_token=''):
        """获取角色成员列表

        :type self: OpenLark
        :param role_id: 角色 id
        :type role_id: str
        :param page_size: 分页大小，最大支持 200；默认为 20
        :type page_size: int
        :param page_token: 分页标记，分页查询还有更多群时会同时返回新的 page_token, 下次遍历可采用该 page_token 获取更多
        :type page_token: str
        :return: (has_more, page_token, user_list)
        :rtype: (bool, str, list[SimpleUser])

        该接口用于获取角色下的用户列表，调用该接口需要有该企业的通讯录读权限或写权限。返回结果为该应用通讯录权限范围内的角色成员列表。

        https://open.feishu.cn/document/ukTMukTMukTM/uczMwUjL3MDM14yNzATN
        """

        base = self._gen_request_url('/open-apis/contact/v2/role/members')
        url = join_url(base, [
            ('role_id', role_id),
            ('page_size', page_size),
            ('page_token', page_token),
        ])
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        has_more = data.get('has_more', False)
        page_token = data.get('page_token', '')
        user_list = [make_datatype(SimpleUser, i) for i in data.get('user_list', [])]  # type: List[SimpleUser]
        return has_more, page_token, user_list


def _make_v1_department_info(res):
    """
    :rtype: Department
    """
    department_info = res['data'].get('department_info') or {}
    open_id = department_info.get('leader_open_id')
    user_id = department_info.get('leader_employee_id')
    department_info['leader'] = {
        'open_id': open_id,
        'user_id': user_id,
    }
    return make_datatype(Department, department_info)  # type: Department


def _make_v1_user(user_info):
    """
    :rtype: DepartmentUser
    """

    user_info['user_id'] = user_info.get('employee_id')
    user_info['en_name'] = user_info.get('name_py')
    user_info['avatar'] = {
        'avatar_72': user_info.get('avatar_72'),
        'avatar_240': user_info.get('avatar_240'),
        'avatar_640': user_info.get('avatar_640'),
        'avatar_origin': user_info.get('avatar_url'),
    }
    user_info['leader'] = {
        'user_id': user_info.get('leader_employee_id'),
        'open_id': user_info.get('leader_open_id')
    }

    return make_datatype(DepartmentUser, user_info)  # type: DepartmentUser
