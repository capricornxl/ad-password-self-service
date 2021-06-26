# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from io import BytesIO
from typing import TYPE_CHECKING, Tuple, Union

from utils.feishu.helper import to_file_like

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIImageMixin(object):
    def upload_image(self, image):
        """上传图片

        :type self: OpenLark
        :param image: 图片文件，支持路径、bytes、BytesIO
        :type image: Union[str, bytes, BytesIO]
        :return: image_key, url
        :rtype: Tuple[str, str]

        上传图片，获取图片的 image_key。

        https://open.feishu.cn/document/ukTMukTMukTM/uEDO04SM4QjLxgDN
        """
        content = to_file_like(image)

        url = self._gen_request_url('/open-apis/image/v4/upload/')
        files = {'image': content}
        res = self._post(url, files=files, with_tenant_token=True)
        data = res['data']
        image_key = data['image_key']  # type: str
        url = data['url']  # type: str
        return image_key, url

    def get_image(self, image_key):
        """获取图片

        :type self: OpenLark
        :param image_key: 图片的key
        :type image_key: str
        :return: 图片 bytes
        :rtype: bytes

        根据图片的image_key拉取图片内容，仅可以拉到自己上传或者收到推送的图片

        https://open.feishu.cn/document/ukTMukTMukTM/uYzN5QjL2cTO04iN3kDN
        """
        url = self._gen_request_url('/open-apis/image/v4/get?image_key=' + image_key)
        return self._get(url=url, raw_content=True, with_tenant_token=True)
