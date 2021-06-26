# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, List

from utils.feishu.dt_drive import DriveFilePermission, unmarshal_drive_user_permission
from utils.feishu.helper import converter_enum

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark
    from utils.feishu.dt_drive import DriveFileUserPermission, DriveFileToken, DriveFileUser, \
        DriveFilePublicLinkSharePermission, DriveFileType


class APIDrivePermissionMixin(object):
    def add_drive_file_permission(self, user_access_token, file_token, file_type, members):
        """增加权限

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文件类型
        :type file_type: DriveFileType
        :param members: 要添加的权限的人
        :type members: list[DriveFileUserPermission]
        :rtype: list[DriveFileUserPermission]

        该接口用于根据 file_token 给用户增加文档的权限

        https://open.feishu.cn/document/ukTMukTMukTM/uMzNzUjLzczM14yM3MTN
        """
        url = self._gen_request_url('/open-apis/drive/permission/member/create')
        body = {
            'token': file_token,
            'type': converter_enum(file_type),
            'members': [i.as_dict() for i in members]
        }
        res = self._post(url, body=body, auth_token=user_access_token)
        if res['data'].get('is_all_success', False):
            return []

        return unmarshal_drive_user_permission(res['data']['fail_members'])  # type: List[DriveFileUserPermission]

    def transfer_drive_file_owner(self, user_access_token, file_token, file_type, owner, remove_old_owner=False,
                                  notify_old_owner=True):
        """转移拥有者

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文件类型
        :type file_type: DriveFileType
        :param owner: 要转移的人
        :type owner: DriveFileUser
        :param remove_old_owner: 转移后删除旧 owner 的权限，默认为 False
        :type remove_old_owner: bool
        :param notify_old_owner: 通知旧 owner，默认为 True
        :type notify_old_owner: bool

        该接口用于根据文档信息和用户信息转移文档的所有者。

        https://open.feishu.cn/document/ukTMukTMukTM/uQzNzUjL0czM14CN3MTN
        """
        url = self._gen_request_url('/open-apis/drive/permission/member/transfer')
        body = {
            'type': converter_enum(file_type),
            'token': file_token,
            'owner': owner.as_dict(),
            'remove_old_owner': remove_old_owner,
            'cancel_notify': not notify_old_owner
        }
        self._post(url, body=body, auth_token=user_access_token)

    def update_drive_file_public_permission(self, user_access_token,
                                            file_token,
                                            file_type,
                                            copy_print_export_status=None,
                                            comment=None,
                                            tenant_shareable=None,
                                            link_share_entity=None,
                                            external_access=None,
                                            invite_external=None):
        """更新文档公共设置

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文件类型
        :type file_type: DriveFileType
        :param copy_print_export_status: 可创建副本/打印/导出/复制设置（不传则保持原值）：
                                            true - 所有可访问此文档的用户
                                            false - 有编辑权限的用户
        :type copy_print_export_status: bool
        :param comment: 可评论设置（不传则保持原值）：
                            true - 所有可访问此文档的用户
                            false - 有编辑权限的用户
        :type comment: bool
        :param tenant_shareable: 租户内用户是否有共享权限（不传则保持原值）
        :type tenant_shareable: bool
        :param link_share_entity: 链接共享（不传则保持原值）：
                                    "tenant_readable" - 组织内获得链接的人可阅读
                                    "tenant_editable" - 组织内获得链接的人可编辑
                                    "anyone_readable" - 获得链接的任何人可阅读
                                    "anyone_editable" - 获得链接的任何人可编辑
        :type link_share_entity: DriveFilePublicLinkSharePermission
        :param external_access: 是否允许分享到租户外开关（不传则保持原值）
        :type external_access: bool
        :param invite_external: 非owner是否允许邀请外部人（不传则保持原值）
        :type invite_external: bool

        该接口用于根据 file_token 更新文档的公共设置

        https://open.feishu.cn/document/ukTMukTMukTM/ukTM3UjL5EzN14SOxcTN
        """
        url = self._gen_request_url('/open-apis/drive/permission/public/update')
        body = {
            'token': file_token,
            'type': converter_enum(file_type),
        }
        if copy_print_export_status is not None:
            body['copy_print_export_status'] = copy_print_export_status
        if comment is not None:
            body['comment'] = comment
        if tenant_shareable is not None:
            body['tenant_shareable'] = tenant_shareable
        if link_share_entity is not None:
            body['link_share_entity'] = link_share_entity.value
        if external_access is not None:
            body['external_access'] = external_access
        if invite_external is not None:
            body['invite_external'] = invite_external
        self._post(url, body=body, auth_token=user_access_token)

    def get_drive_file_permissions(self, user_access_token, file_token, file_type):
        """获取协作者列表

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文件类型
        :type file_type: DriveFileType
        :rtype list[DriveFileUserPermission]

        该接口用于根据 file_token 查询协作者，目前包括人("user")和群("chat")

        你能获取到协作者列表的前提是你对该文档有权限

        https://open.feishu.cn/document/ukTMukTMukTM/uATN3UjLwUzN14CM1cTN
        """
        url = self._gen_request_url('/open-apis/drive/permission/member/list')
        body = {
            'type': converter_enum(file_type),
            'token': file_token,
        }
        res = self._post(url, body=body, auth_token=user_access_token)
        return unmarshal_drive_user_permission(res['data']['members'],
                                               open_id_type='user',
                                               open_id_key='member_open_id',
                                               chat_id_type='chat',
                                               chat_id_key='member_open_id')  # type: List[DriveFileUserPermission]

    def delete_drive_file_permission(self, user_access_token, file_token, file_type, member):
        """移除协作者权限

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文件类型
        :type file_type: DriveFileType
        :param member: 成员
        :type member: DriveFileUser

        该接口用于根据 file_token 移除文档协作者的权限

        https://open.feishu.cn/document/ukTMukTMukTM/uYTN3UjL2UzN14iN1cTN
        """
        url = self._gen_request_url('/open-apis/drive/permission/member/delete')
        body = member.as_dict()
        body['token'] = file_token
        body['type'] = converter_enum(file_type)
        self._post(url, body=body, auth_token=user_access_token)

    def update_drive_file_permission(self, user_access_token,
                                     file_token, file_type,
                                     member,
                                     perm=DriveFilePermission.view,
                                     is_notify=None):
        """更新协作者权限

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文件类型
        :type file_type: DriveFileType
        :param member: 成员
        :type member: DriveFileUser
        :param perm: 权限
        :type perm: DriveFilePermission
        :param is_notify: 是否通知
        :type is_notify: bool

        该接口用于根据 file_token 更新文档协作者的权限

        https://open.feishu.cn/document/ukTMukTMukTM/ucTN3UjL3UzN14yN1cTN
        """
        url = self._gen_request_url('/open-apis/drive/permission/member/update')
        body = member.as_dict()
        body['token'] = file_token
        body['type'] = converter_enum(file_type)
        body['perm'] = converter_enum(perm)
        if is_notify is not None:
            body['notify_lark'] = is_notify
        self._post(url, body=body, auth_token=user_access_token)

    def check_drive_file_permission(self, user_access_token, file_token, file_type, perm):
        """判断协作者是否有某权限

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文件类型
        :type file_type: DriveFileType
        :param perm: 权限
        :type perm: DriveFilePermission

        该接口用于根据 file_token 判断当前登录用户是否具有某权限

        https://open.feishu.cn/document/ukTMukTMukTM/uYzN3UjL2czN14iN3cTN
        """
        url = self._gen_request_url('/open-apis/drive/permission/member/permitted')
        body = {
            'token': file_token,
            'type': converter_enum(file_type),
            'perm': converter_enum(perm),
        }
        res = self._post(url, body=body, auth_token=user_access_token)
        return res['data']['is_permitted']
