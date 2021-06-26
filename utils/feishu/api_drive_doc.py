# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from utils.feishu.dt_drive import DriveDocFileMeta
from utils.feishu.dt_help import make_datatype

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIDriveDocMixin(object):
    def get_drive_doc_content(self, user_access_token, doc_token):
        """获取 doc 文件内容

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param doc_token: 文件的 token
        :type doc_token: str
        :return: 文件原始内容
        :rtype: str

        该接口用于获取文档的纯文本内容，不包含富文本格式信息，主要用于搜索，如导入 es 等。

        https://open.feishu.cn/document/ukTMukTMukTM/ukzNzUjL5czM14SO3MTN
        """
        url = self._gen_request_url('/open-apis/doc/v2/{}/raw_content'.format(doc_token))
        res = self._get(url, auth_token=user_access_token)
        return res['data']['content']

    def get_drive_doc_meta(self, user_access_token, doc_token):
        """获取 doc 文件元信息

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param doc_token: 文件的 token
        :type doc_token: str
        :return: 文件元内容
        :rtype: DriveDocFileMeta

        该接口用于根据 docToken 获取元数据。

        https://open.feishu.cn/document/ukTMukTMukTM/uczN3UjL3czN14yN3cTN
        """
        url = self._gen_request_url('/open-apis/doc/v2/meta/{}'.format(doc_token))
        res = self._get(url, auth_token=user_access_token)
        return make_datatype(DriveDocFileMeta, res['data'])
