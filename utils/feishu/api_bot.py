# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Any, Dict

from utils.feishu.dt_code import Bot
from utils.feishu.dt_help import make_datatype

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class APIBotMixin(object):
    def get_bot_info(self):
        """获取机器人信息

        :type self: OpenLark
        :return: 机器人的对象 Bot
        :rtype: Bot

        https://open.feishu.cn/document/ukTMukTMukTM/uAjMxEjLwITMx4CMyETM
        """
        url = self._gen_request_url('/open-apis/bot/v3/info/')
        body = {}  # type: Dict[str, Any]
        res = self._post(url, body, with_tenant_token=True)
        return make_datatype(Bot, res['bot'])
