# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Tuple

from utils.feishu.dt_drive import DriveCreateFile, DriveFileToken, DriveFolderMeta
from utils.feishu.dt_help import make_datatype

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIDriveFolderMixin(object):
    def create_drive_folder(self, user_access_token, folder_token, title):
        """新建文件夹

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param folder_token: 父文件夹的 token
        :type folder_token: str
        :param title: 要创建的文件夹名称
        :type title: str
        :return: 文件夹元信息
        :rtype: DriveFolderMeta

        该接口用于根据 folder_token 在该 folder 下创建文件夹

        https://open.feishu.cn/document/ukTMukTMukTM/ukTNzUjL5UzM14SO1MTN
        """
        url = self._gen_request_url('/open-apis/drive/explorer/v2/folder/{}'.format(folder_token))
        body = {
            'title': title,
        }
        res = self._post(url, body=body, auth_token=user_access_token)
        return make_datatype(DriveCreateFile, res['data'])

    def get_drive_folder_meta(self, user_access_token, folder_token):
        """获取文件夹元信息

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param folder_token: 文件夹的 token
        :type folder_token: str
        :return: 文件夹元信息
        :rtype: DriveFolderMeta

        该接口用于根据 folder_token 获取该文件夹的元信息

        https://open.feishu.cn/document/ukTMukTMukTM/uAjNzUjLwYzM14CM2MTN
        """
        url = self._gen_request_url('/open-apis/drive/explorer/v2/folder/{}/meta'.format(folder_token))
        res = self._get(url, auth_token=user_access_token)
        return make_datatype(DriveFolderMeta, res['data'])

    def get_drive_root_folder_meta(self, user_access_token):
        """获取root folder（我的空间） meta

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :return: 文件夹元信息
        :rtype: DriveFolderMeta

        该接口用于获取 "我的文档" 的元信息

        https://open.feishu.cn/document/ukTMukTMukTM/uAjNzUjLwYzM14CM2MTN
        """
        url = self._gen_request_url('/open-apis/drive/explorer/v2/root_folder/meta')
        res = self._get(url, auth_token=user_access_token)
        return DriveFolderMeta(id=res['data']['id'],
                               token=res['data']['token'],
                               own_uid=res['data']['user_id'])

    def get_drive_folder_children(self, user_access_token, folder_token):
        """获取文件夹下的文档清单

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param folder_token: 文件夹的 token
        :type folder_token: str
        :return: 该文件夹的文档清单，如 doc、sheet、bitable、folder
        :rtype: list[DriveFileToken]

        该接口用于获取 "我的文档" 的元信息

        https://open.feishu.cn/document/ukTMukTMukTM/uEjNzUjLxYzM14SM2MTN
        """
        url = self._gen_request_url('/open-apis/drive/explorer/v2/folder/{}/children'.format(folder_token))
        res = self._get(url, auth_token=user_access_token)
        return [make_datatype(DriveFileToken, i) for _, i in res['data']['children'].items()]
