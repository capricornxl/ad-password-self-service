# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING

from six.moves.urllib.parse import quote

from utils.feishu.helper import join_url

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIAppLink(object):
    def __init__(self, host, qs):
        self.host = host
        self.qs = qs

    def open_client(self):
        """唤起飞书客户端的 app_link 链接
        """

        base = 'https://{}/client/op/open'.format(self.host)
        return join_url(base, self.qs, sep='?')

    def open_mini_program(self, app_id, mode='', path='', path_android='', path_ios='', path_pc=''):
        """打开一个小程序或者小程序中的一个页面

        :param app_id: 小程序 app_id
        :type app_id: str
        :param mode: PC 必填	PC小程序的三种模式：sidebar-semi、window、appCenter
        :type mode: str
        :param path: 需要跳转的页面路径，路径后可以带参数。也可以使用path_android、path_ios、path_pc参数对不同的客户端指定不同的path
        :type path: str
        :param path_android: 同 path 参数，Android 端会优先使用该参数，如果该参数不存在，则会使用 ptah 参数
        :type path_android: str
        :param path_ios: 同 path 参数，iOS 端会优先使用该参数，如果该参数不存在，则会使用 ptah 参数
        :type path_ios: str
        :param path_pc: 同 path 参数，PC 端会优先使用该参数，如果该参数不存在，则会使用 ptah 参数
        :type path_pc: str
        :return: url
        :rtype: str

        使用示例

        1. 打开小程序

            lark_cli.app_link().open_mini_program(app_id='1234567890', mode='window')

            # https://applink.feishu.cn/client/mini_program/open?appId=1234567890&mode=window

        2. 打开小程序的一个页面 pages/home

            lark_cli.app_link().open_mini_program(app_id='1234567890', mode='window', path='pages/home')

            # https://applink.feishu.cn/client/mini_program/open?appId=1234567890&mode=window&path=pages%2Fhome

        3. 打开小程序的一个页面带参数 pages/home?xid=123

            lark_cli.app_link().open_mini_program(app_id='1234567890', mode='window', path='pages/home?xid=123')

            # https://applink.feishu.cn/client/mini_program/open?appId=1234567890&mode=window&
            path=pages%2Fhome%3Fxid%3D123

        4. 在 PC 端打开页面 pages/pc_home?pid=123，在其他端打开页面 pages/home?xid=123

            lark_cli.app_link().open_mini_program(app_id='1234567890', mode='window', path='pages/home?xid=123',
            path_pc='pages/pc_home?pid=123')

            # https://applink.feishu.cn/client/mini_program/open?appId=1234567890&mode=window&
            path=pages%2Fhome%3Fxid%3D123&path_pc=pages%2Fpc_home%3Fpid%3D123

        5. 在 PC 4.2.0 及以上版本支持打开小程序，PC 4.2.0 以下版本提示不支持

            lark_cli.app_link(min_ver_pc='4.2.0').open_mini_program(app_id='1234567890', mode='window')

            # https://applink.feishu.cn/client/mini_program/open?appId=1234567890&mode=window&min_lk_ver_pc=4.2.0
        """
        qs = [
            ('appId', app_id),
            ('mode', mode),
            ('path', quote(path, safe='') if path else ''),
            ('path_android', quote(path_android, safe='') if path_android else ''),
            ('path_ios', quote(path_ios, safe='') if path_ios else ''),
            ('path_pc', quote(path_pc, safe='') if path_pc else ''),
        ]
        for i in self.qs:
            qs.append((i[0], i[1]))

        base = 'https://{}/client/mini_program/open'.format(self.host)
        return join_url(base, qs, sep='?')

    def open_chat(self, open_id='', open_chat_id=''):
        """打开一个小程序或者小程序中的一个页面

        :param open_id: 用户 open_id
        :type open_id: str
        :param open_chat_id: 用会话ID，包括单聊会话和群聊会话
        :type open_chat_id: str
        :return: url
        :rtype: str

        使用示例

        使用 open_id 打开聊天页面

            lark_cli.app_link().open_chat(open_id='1234567890')

            # https://applink.feishu.cn/client/chat/open?openId=1234567890
        """
        qs = [
            ('openId', open_id),
            ('openChatId', open_chat_id)
        ]
        for i in self.qs:
            if i[1]:
                qs.append((i[0], i[1]))

        base = 'https://{}/client/mini_program/open'.format(self.host)
        return join_url(base, qs, sep='?')


class APIAppLinkMixin(object):
    @property
    def _app_link_host(self):
        """
        :type self: OpenLark
        """
        if self.is_lark:
            return 'applink.larksuite.com'
        return 'applink.feishu.cn'

    def app_link(self, min_lk_ver='', min_lk_ver_android='', min_lk_ver_ios='', min_lk_ver_pc=''):
        """

        :param min_lk_ver:
        :param min_lk_ver_android:
        :param min_lk_ver_ios:
        :param min_lk_ver_pc:
        :return:
        :rtype: APIAppLink

        指定 AppLink 协议能够兼容的最小飞书版本，使用三位版本号 x.y.z。

        如果当前飞书版本号小于min_lk_ver，打开该 AppLink 会显示为兼容页面。

        也可使用 min_lk_ver_android、min_lk_ver_ios、min_lk_ver_pc 参数对不同的客户端指定不同的版本。
        """
        qs = [
            ('min_lk_ver', min_lk_ver),
            ('min_lk_ver_android', min_lk_ver_android),
            ('min_lk_ver_ios', min_lk_ver_ios),
            ('min_lk_ver_pc', min_lk_ver_pc),
        ]
        return APIAppLink(self._app_link_host, qs)
