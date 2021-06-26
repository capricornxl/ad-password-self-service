# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from utils.feishu.dt_drive import DriveCopyFile, DriveCreateFile, DriveDeleteFile, DriveFileType
from utils.feishu.dt_help import make_datatype
from utils.feishu.exception import LarkInvalidArguments
from utils.feishu.helper import converter_enum

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIDriveFileMixin(object):
    def create_drive_file(self, user_access_token, folder_token, title, file_type):
        """创建云空间文件

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param folder_token: 文件夹的 token
        :type folder_token: str
        :param title: 文档标题
        :type title: str
        :param file_type: 文档类型，可选值为 doc 和 sheet
        :type file_type: DriveFileType
        :return: 文件夹元信息
        :rtype: DriveCreateFile

        该接口用于根据 folder_token 创建 Docs或 Sheets 。

        https://open.feishu.cn/document/ukTMukTMukTM/uQTNzUjL0UzM14CN1MTN
        """
        url = self._gen_request_url('/open-apis/drive/explorer/v2/file/{}'.format(folder_token))
        body = {
            'title': title,
            'type': converter_enum(file_type, ranges=[DriveFileType.doc, DriveFileType.sheet]),
        }
        res = self._post(url, body=body, auth_token=user_access_token)
        return make_datatype(DriveCreateFile, res['data'])

    def delete_drive_file(self, user_access_token, file_token, file_type):
        """删除云空间文件

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文档类型，可选值为 doc 和 sheet
        :type file_type: DriveFileType
        :return: 文件夹元信息
        :rtype: DriveDeleteFile

        本文档包含两个接口，分别用于删除 Doc 和 Sheet，对应的文档类型请调用对应的接口

        文档只能被文档所有者删除，文档被删除后将会放到回收站里

        https://open.feishu.cn/document/ukTMukTMukTM/uATM2UjLwEjN14CMxYTN
        """
        if converter_enum(file_type) == 'doc':
            url = self._gen_request_url('/open-apis/drive/explorer/v2/file/docs/{}'.format(file_token))
        elif converter_enum(file_type) == 'sheet':
            url = self._gen_request_url('/open-apis/drive/explorer/v2/file/spreadsheets/{}'.format(file_token))
        else:
            raise LarkInvalidArguments(msg='delete file type should be doc or sheet')

        res = self._delete(url, auth_token=user_access_token)
        return make_datatype(DriveDeleteFile, res['data'])

    def copy_drive_file(self, user_access_token, file_token, file_type, dst_folder_token, dst_title,
                        permission_needed=False, comment_needed=False):
        """复制云空间文件

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param file_type: 文档类型，可选值为 doc 和 sheet
        :type file_type: DriveFileType
        :param dst_folder_token：目标文件夹 token
        :type dst_folder_token: str
        :param dst_title: 目标文档标题
        :type dst_title: str
        :param permission_needed: 同时复制权限
        :type permission_needed: bool
        :param comment_needed: 同时复制评论
        :type comment_needed: bool
        :return: 复制文件的返回值
        :rtype: DriveCopyFile

        该接口用于根据 file_token 复制 docs 或 sheets 。

        https://open.feishu.cn/document/ukTMukTMukTM/uYTNzUjL2UzM14iN1MTN
        """
        url = self._gen_request_url('/open-apis/drive/explorer/v2/file/copy/files/{}'.format(file_token))
        body = {
            'type': converter_enum(file_type),
            'dstFolderToken': dst_folder_token,
            'dstName': dst_title,
            'permissionNeeded': permission_needed,
            'CommentNeeded': comment_needed
        }

        res = self._post(url, body=body, auth_token=user_access_token)
        return make_datatype(DriveCopyFile, res['data'])
