# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import TYPE_CHECKING, Tuple

import requests

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark

logger = logging.getLogger('feishu')


class APIDutyMixin(object):
    def join_duty_room(self, duty_room_id, duty_room_token, user_id):
        """加入服务台

        :type self: OpenLark
        :param duty_room_id: 服务台的 id
        :param duty_room_token: 服务台的 token
        :param user_id: 用户 id
        :return: 用户所在的服务台对话的 chat_id，和带有 Lark 协议的跳转 URI
        :rtype: Tuple[str, str]

        跳转入用户专属的飞书中值班号客服群中

        需要服务台的管理员联系 @杨帆 获取接入服务台 duty_room_token 和服务台 duty_room_id

        https://bytedance.feishu.cn/space/doc/YlsR7QzmqM0gg6wbwpY4la
        """
        url = 'https://api.zjurl.cn/saipan/api/chat/to_chat'
        r = requests.post(url, json={
            'duty_room_id': duty_room_id,
            'token': duty_room_token,
            'user_id': user_id,
        })
        logger.debug('[join_duty_room] duty_room_id=%s, user_id=%s, status_code=%d, resp=%s', duty_room_id, user_id,
                     r.status_code, r.text)

        try:
            r.raise_for_status()
            data = r.json()
            chat_id = data['data']['chat_id']
            lark_client_uri = 'lark://client/chat/{}'.format(chat_id)
            return chat_id, lark_client_uri
        except Exception as e:
            logger.error('[join_duty_room] duty_room_id=%s, user_id=%s, status_code=%d, resp=%s, err=%s', duty_room_id,
                         user_id, r.status_code, r.text, e)
            raise
