# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from io import BytesIO
from typing import TYPE_CHECKING, Tuple, Union

from utils.feishu.helper import to_file_like

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIFileMixin(object):
    def get_file_by_key(self, file_key):
        """获取文件

        :type self: OpenLark
        :param file_key: 文件的 key
        :type file_key: str
        :return: 文件的二进制数据流
        :rtype: list[byte]

        根据文件的 file_key 拉取文件内容，当前仅可用来获取用户与机器人单聊发送的文件

        https://open.feishu.cn/document/ukTMukTMukTM/uMDN4UjLzQDO14yM0gTN
        """
        url = self._gen_request_url('/open-apis/open-file/v1/get?file_key={}'.format(file_key))
        res = self._get(url, raw_content=True, with_tenant_token=True)
        return res
