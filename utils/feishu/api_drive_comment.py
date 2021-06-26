# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from six import string_types

from utils.feishu.dt_drive import DriveComment
from utils.feishu.dt_help import make_datatype
from utils.feishu.exception import LarkInvalidArguments

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIDriveCommentMixin(object):
    def add_drive_comment(self, user_access_token, file_token, content):
        """添加全文评论

        :type self: OpenLark
        :param user_access_token: user_access_token
        :type user_access_token: str
        :param file_token: 文件的 token
        :type file_token: str
        :param content: 评论内容
        :type content: str
        :return: 评论对象
        :rtype: DriveComment

        该接口用于根据 file_token 给文档添加全文评论

        https://open.feishu.cn/document/ukTMukTMukTM/ucDN4UjL3QDO14yN0gTN
        """
        if not content or not isinstance(content, string_types):
            raise LarkInvalidArguments(msg='content empty')

        content = content. \
            replace('<', '&lt;'). \
            replace('>', '&gt;'). \
            replace('&', '&amp;'). \
            replace('\'', '&#x27;'). \
            replace('"', '&quot;')

        url = self._gen_request_url('/open-apis/comment/add_whole')
        body = {
            'type': 'doc',
            'token': file_token,
            'content': content
        }
        res = self._post(url, body=body, auth_token=user_access_token)
        return make_datatype(DriveComment, res['data'])
