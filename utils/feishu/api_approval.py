# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import json
from typing import TYPE_CHECKING, Dict, List, Tuple

from utils.feishu.dt_approval import ApprovalDefinition, ApprovalForm, ApprovalInstance, ApprovalNode
from utils.feishu.dt_enum import ApprovalUploadFileType
from utils.feishu.dt_help import make_datatype
from utils.feishu.exception import LarkInvalidArguments
from utils.feishu.helper import converter_enum, to_file_like

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


def _transfer_locale(locale='zh'):
    return {'zh': 'zh-CN', 'en': 'en-US'}.get(str(locale).lower())


class APIApprovalMixin(object):
    def get_approval_definition(self, definition_code, locale='zh'):
        """查看审批定义

        :type self: OpenLark
        :param definition_code: 审批定义Code，需要有管理员权限，然后在 https://www.feishu.cn/approval/admin/approvalList 创建
        :type definition_code: str
        :param locale: zh or en
        :type locale: str
        :return: 审批定义对象 ApprovalDefinition
        :rtype: ApprovalDefinition

        根据 definition_code 获取某个审批定义的详情，用于构造创建审批实例的请求。

        https://open.feishu.cn/document/ukTMukTMukTM/uADNyUjLwQjM14CM0ITN
        """
        url = self._gen_request_url('/approval/openapi/v2/approval/get', app='approval')
        locale = {'zh': 'zh-CN', 'en': 'en-US'}.get(str(locale).lower())
        body = {'approval_code': definition_code, 'locale': locale}
        res = self._post(url, body, with_tenant_token=True)
        data = res['data']

        approval_name = data['approval_name']
        form = json.loads(data['form'])
        nodes = data['node_list']

        definition = ApprovalDefinition(
            approval_name=approval_name,
            forms=[make_datatype(ApprovalForm, i) for i in form],
            nodes=[make_datatype(ApprovalNode, i) for i in nodes],
        )
        return definition

    def get_approval_instance_code_list(self, approval_code, start_time, end_time, offset=0, limit=100):
        """批量获取审批实例ID

        :type self: OpenLark
        :param approval_code: 审批定义code，需要有管理员权限，然后在 https://www.feishu.cn/approval/admin/approvalList 创建
        :type approval_code: str
        :param start_time: 审批实例创建时间区间，13位毫秒级时间戳
        :type start_time: int
        :param end_time: 审批实例创建时间区间，13位毫秒级时间戳
        :type end_time: int
        :param offset: 分页参数
        :type offset: int
        :param limit: 分页参数（不得大于100）
        :type limit: int
        :return: 审批实例ID数组
        :rtype: list[str]

        根据 approval_code 批量获取审批实例的 instance_code，用于拉取租户下某个审批定义的全部审批实例。 默认以审批创建时间排序。

        https://open.feishu.cn/document/ukTMukTMukTM/uQDOyUjL0gjM14CN4ITN
        """
        url = self._gen_request_url('/approval/openapi/v2/instance/list', app='approval')
        body = {
            'approval_code': approval_code,
            'start_time': start_time,
            'end_time': end_time,
            'offset': offset,
            'limit': limit,
        }
        res = self._post(url, body=body, with_tenant_token=True)
        data = res['data']
        return data.get('instance_code_list', [])  # type: List[str]

    def get_approval_instance(self, instance_code, locale='zh'):
        """获取单个审批实例详情

        :type self: OpenLark
        :param instance_code: 审批实例 code，需要有管理员权限，然后在 https://www.feishu.cn/approval/admin/approvalList 创建
        :type instance_code: str
        :param locale zh 中文，en 英文
        :type locale: str
        :return: 审批实例的对象 ApprovalInstance
        :rtype: ApprovalInstance

        根据 instance_code 获取某个审批实例的详情，instance_code 由【批量获取审批实例】接口获取。

        一般情况下，当实例状态为1，需定期重新拉取，以确保获取到最新的实例详情。

        https://open.feishu.cn/document/ukTMukTMukTM/uEDNyUjLxQjM14SM0ITN
        """
        url = self._gen_request_url('/approval/openapi/v2/instance/get', app='approval')
        body = {'instance_code': instance_code, 'locale': _transfer_locale(locale)}
        res = self._post(url, body=body, with_tenant_token=True)
        data = res['data']
        instance = make_datatype(ApprovalInstance, data)
        return instance

    def create_approval(self,
                        definition_code,
                        employee_id,
                        department_id,
                        form_list,
                        approver_employee_id_list,
                        cc_employee_id_list=None,
                        node_approver_employee_id_list=None):
        """创建审批实例

        :type self: OpenLark
        :param definition_code: 审批定义 code，需要有管理员权限，然后在 https://www.feishu.cn/approval/admin/approvalList 创建
        :type definition_code: str
        :param employee_id: 租户内用户唯一 ID
        :type employee_id: str
        :param department_id: 部门 ID
        :type  department_id: str
        :param form_list: 审批的表单内容
        :type form_list: list[(str, Any)]
        :param approver_employee_id_list: 审批人用户 ID 列表
        :type approver_employee_id_list: list[str]
        :param cc_employee_id_list: 抄送人用户 ID 列表
        :type cc_employee_id_list: list[str]
        :param node_approver_employee_id_list: 发起人自选审批人列表
        :type node_approver_employee_id_list: Dict[str, list[str]]
        :return: 审批实例的 instance_code
        :rtype: str

        创建一个审批实例，调用方需对审批定义的表单有详细了解，将按照定义的表单结构，将表单 Value 通过接口传入。

        https://open.feishu.cn/document/ukTMukTMukTM/uYDO24iN4YjL2gjN
        """
        form = []
        for i in form_list:
            if len(i) != 2:
                raise LarkInvalidArguments(msg='the length of item in a form_list be 2(key and value)')
            form.append({'id': i[0], 'value': i[1]})

        url = self._gen_request_url('/approval/openapi/v1/instance/create', app='approval')
        if not cc_employee_id_list:
            cc_employee_id_list = []
        if not node_approver_employee_id_list:
            node_approver_employee_id_list = {}
        body = {
            'definition_code': definition_code,
            'employee_id': employee_id,
            'department_id': department_id,
            'form': json.dumps(form),
            'approver_employee_id_list': approver_employee_id_list,
            'cc_employee_id_list': cc_employee_id_list,
            'node_approver_employee_id_list': node_approver_employee_id_list,
        }
        res = self._post(url, body=body, with_tenant_token=True)
        return res.get('data', {}).get('instance_code', '')

    def subscribe_approval(self, definition_code):
        """订阅审批事件

        :type self: OpenLark
        :param definition_code: 审批定义Code，需要有管理员权限，然后在 https://www.feishu.cn/approval/admin/approvalList 创建
        :type definition_code: str
        :raise: LarkApprovalSubscriptionExistException 重复订阅会抛错

        订阅 definition_code 后，可以收到该审批定义对应实例的事件通知。

        https://open.feishu.cn/document/ukTMukTMukTM/uUTOwEjL1kDMx4SN5ATM
        """
        url = self._gen_request_url('/approval/openapi/v1/subscription/subscribe', app='approval')
        body = {'definition_code': definition_code}
        self._post(url, body=body, with_tenant_token=True)

    def unsubscribe_approval(self, definition_code):
        """取消订阅审批事件

        :type self: OpenLark
        :param definition_code: 审批定义Code
        :type definition_code: str

        取消订阅 definition_code 后，无法再收到该审批定义对应实例的事件通知。

        https://open.feishu.cn/document/ukTMukTMukTM/uYTOwEjL2kDMx4iN5ATM
        """
        url = self._gen_request_url('/approval/openapi/v1/subscription/unsubscribe', app='approval')
        body = {'definition_code': definition_code}
        self._post(url, body=body, with_tenant_token=True)

    def approve_approval(self,
                         approval_code,
                         instance_code,
                         user_id,
                         task_id,
                         comment=None):
        """审批任务同意

        :type self: OpenLark
        :param approval_code: 审批定义 code
        :type approval_code: str
        :param instance_code: 审批实例 code
        :type instance_code: str
        :param user_id: 操作用户的 user_id(v3 接口的 employee_id)
        :type user_id: str
        :param task_id: 任务id
        :type task_id: str
        :param comment: 意见
        :type comment: str

        对于单个审批任务进行同意操作。同意后审批流程会流转到下一个审批人。

        https://open.feishu.cn/document/ukTMukTMukTM/uMDNyUjLzQjM14yM0ITN
        """
        url = self._gen_request_url('/approval/openapi/v2/instance/approve', app='approval')
        body = {
            'approval_code': approval_code,
            'instance_code': instance_code,
            'user_id': user_id,
            'task_id': task_id,
            'comment': comment,
        }
        self._post(url, body, with_tenant_token=True)

    def reject_approval(self,
                        approval_code,
                        instance_code,
                        user_id,
                        task_id,
                        comment=None):
        """审批任务拒绝

        :type self: OpenLark
        :param approval_code: 审批定义 code
        :type approval_code: str
        :param instance_code: 审批实例 code
        :type instance_code: str
        :param user_id: 操作用户的 user_id(v3 接口的 employee_id)
        :type user_id: str
        :param task_id: 任务id
        :type task_id: str
        :param comment: 意见
        :type comment: str

        对于单个审批任务进行拒绝操作。拒绝后审批流程结束。

        https://open.feishu.cn/document/ukTMukTMukTM/uQDNyUjL0QjM14CN0ITN
        """
        url = self._gen_request_url('/approval/openapi/v2/instance/reject', app='approval')
        body = {
            'approval_code': approval_code,
            'instance_code': instance_code,
            'user_id': user_id,
            'task_id': task_id,
            'comment': comment,
        }
        self._post(url, body, with_tenant_token=True)

    def transfer_approval(self,
                          approval_code,
                          instance_code,
                          user_id,
                          task_id,
                          transfer_user_id,
                          comment=None):
        """审批任务转交

        :type self: OpenLark
        :param approval_code: 审批定义 code
        :type approval_code: str
        :param instance_code: 审批实例 code
        :type instance_code: str
        :param user_id: 操作用户的 user_id(v3 接口的 employee_id)
        :type user_id: str
        :param task_id: 任务id
        :type task_id: str
        :param comment: 意见
        :type comment: str
        :param transfer_user_id: 被转交用户的 user_id(v3 接口的 employee_id)
        :type transfer_user_id: str

        对于单个审批任务进行转交操作。转交后审批流程流转给被转交人。

        https://open.feishu.cn/document/ukTMukTMukTM/uUDNyUjL1QjM14SN0ITN?lang=zh-CN
        """
        url = self._gen_request_url('/approval/openapi/v2/instance/transfer', app='approval')
        body = {
            'approval_code': approval_code,
            'instance_code': instance_code,
            'user_id': user_id,
            'task_id': task_id,
            'comment': comment,
            'transfer_user_id': transfer_user_id,
        }
        self._post(url, body, with_tenant_token=True)

    def cancel_approval(self, approval_code, instance_code, user_id):
        """审批实例撤销

        :type self: OpenLark
        :param approval_code: 审批定义 code
        :type approval_code: str
        :param instance_code: 审批实例 code
        :param user_id: 操作用户的 user_id(v3 接口的 employee_id)

        对于单个审批实例进行撤销操作。撤销后审批流程结束。

        https://open.feishu.cn/document/ukTMukTMukTM/uYDNyUjL2QjM14iN0ITN?lang=zh-CN
        """
        url = self._gen_request_url('/approval/openapi/v2/instance/cancel', app='approval')
        body = {
            'approval_code': approval_code,
            'instance_code': instance_code,
            'user_id': user_id,
        }
        self._post(url, body, with_tenant_token=True)

    def upload_approval_file(self, name, filetype, content):
        """审批所需要的文件上传

        :type self: OpenLark
        :param name: 文件名，需包含文件扩展名，如“文件.doc
        :type name: str
        :param filetype: 文件类型，只能是 image 和 attachment 之一
        :type filetype: ApprovalUploadFileType
        :param content: 文件，支持路径、bytes、BytesIO
        :return: 返回的第一个是可以用于审批的 code，第二个是图片或者文件的 URL
        :rtype: Tuple[str, str]
        """
        content = to_file_like(content)

        url = self._gen_request_url('/approval/openapi/v1/file/upload', app='approval')
        body = {
            'name': name,
            'type': converter_enum(filetype),
        }
        files = {'content': content}
        res = self._post(url=url, body=body, files=files, with_tenant_token=True)
        data = res['data']
        code = data.get('code', '')  # type: str
        url = data.get('url', '')  # type: str
        return code, url
