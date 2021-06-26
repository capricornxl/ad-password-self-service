# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from utils.feishu.dt_drive import DriveFileMeta
from utils.feishu.dt_help import make_datatype
from utils.feishu.helper import converter_enum

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark
    from utils.feishu.dt_drive import DriveFileToken, DriveFileType


class APIDriveSuiteMixin(object):
    def get_drive_file_meta(self, user_access_token, files):
        """获取各类文件的元数据

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param files: 文件的 token 列表
        :type files: list[DriveFileToken]
        :return: 文件元信息
        :rtype: list[DriveFileMeta]

        该接口用于根据 token 获取各类文件的元数据

        https://open.feishu.cn/document/ukTMukTMukTM/uMjN3UjLzYzN14yM2cTN
        """
        url = self._gen_request_url('/open-apis/suite/docs-api/meta')
        body = {
            'request_docs': [
                {
                    'docs_token': i.token,
                    'docs_type': i.type,
                } for i in files
            ]
        }
        res = self._post(url, body=body, auth_token=user_access_token)
        return [make_datatype(DriveFileMeta, i) for i in res['data']['docs_metas']]

    def search_drive_file(self, user_access_token, key, owner_open_ids=None, chat_open_ids=None, docs_types=None,
                          count=50, offset=0):
        """文档搜索

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param key: 搜索的关键词
        :type key: str
        :param owner_open_ids: 文档所有人
        :type owner_open_ids: list[str]
        :param chat_open_ids: 文档所在群
        :type chat_open_ids: list[str]
        :param docs_types: 文档类型，支持："doc", "sheet", "slide", "bitable", "mindnote", "file", "wiki"
        :type docs_types: list[DriveFileType]
        :param count: 个数
        :type count: int
        :param offset: 偏移
        :type offset: int
        :return: 文件元信息
        :rtype: (bool, int, list[DriveFileMeta])

        该接口用于根据搜索条件进行文档搜索

        https://open.feishu.cn/document/ukTMukTMukTM/ugDM4UjL4ADO14COwgTN
        """
        url = self._gen_request_url('/open-apis/suite/docs-api/search/object')
        body = {
            'search_key': key,
            'count': count,
            'offset': offset,
        }
        if owner_open_ids:
            body['owner_ids'] = owner_open_ids
        if chat_open_ids:
            body['chat_ids'] = chat_open_ids
        if docs_types:
            body['docs_types'] = [converter_enum(i) for i in docs_types]
        res = self._post(url, body=body, auth_token=user_access_token)
        has_more = res['data']['has_more']
        total = res['data']['total']
        entities = [make_datatype(DriveFileMeta, i) for i in res['data']['docs_entities']]
        return has_more, total, entities
