# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import List

import attr

from utils.feishu.dt_help import to_json_decorator


@to_json_decorator
@attr.s
class I18NTitle(object):
    en_us = attr.ib(type=str, default=None)
    zh_cn = attr.ib(type=str, default=None)
    ja_jp = attr.ib(type=str, default=None)


@to_json_decorator
@attr.s
class SimpleUser(object):
    """用户对象
    """
    name = attr.ib(type=str, default=None)
    open_id = attr.ib(type=str, default=None)
    user_id = attr.ib(type=str, default=None)


@to_json_decorator
@attr.s
class User(object):
    """用户对象
    """
    avatar_url = attr.ib(type=str, default='')
    name = attr.ib(type=str, default='')
    open_id = attr.ib(type=str, default='')
    email = attr.ib(type=str, default='')  # 需要申请获取email权限才有
    mobile = attr.ib(type=str, default='')  # 用户手机号，已申请"获取用户手机号"权限的企业自建应用返回该字段
    user_id = attr.ib(type=str, default='')  # 用户的user_id
    status = attr.ib(type=int, default=0)


@to_json_decorator
@attr.s
class Bot(object):
    """机器人对象
    """
    activate_status = attr.ib(type=int, default=None)  # TODO 啥意思
    app_name = attr.ib(type=str, default=None)
    avatar_url = attr.ib(type=str, default=None)
    open_id = attr.ib(type=str, default='')  # 啥意思，没有在文档中
    ip_white_list = attr.ib(type=List[str], default=attr.Factory(list))  # type: List[str]


@to_json_decorator
@attr.s
class Chat(object):
    """会话信息，包括和机器人的私聊 + 群聊
    """
    avatar = attr.ib(type=str, default='')  # 群头像
    description = attr.ib(type=str, default='')  # 群描述
    chat_id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default='')  # 群聊的名字，如果是p2p就是空
    owner_user_id = attr.ib(type=str, default='')  # 群主的user_id，机器人是群主的时候没有这个字段
    owner_open_id = attr.ib(type=str, default='')  # 群主的open_id，机器人是群主的时候没有这个字段


@to_json_decorator
@attr.s
class DetailChat(object):
    """详细的会话信息，包括和机器人的私聊 + 群聊
    """
    chat_id = attr.ib(type=str, default=None)
    avatar = attr.ib(type=str, default='')  # 群头像
    description = attr.ib(type=str, default='')  # 群描述
    name = attr.ib(type=str, default='')  # 群聊的名字，如果是p2p就是空
    i18n_names = attr.ib(type=I18NTitle, default=None)  # 国际化名称
    members = attr.ib(type=List[SimpleUser], default=attr.Factory(list))  # type: List[SimpleUser]
    type = attr.ib(type=str, default=None)  # 群类型，group表示群聊，p2p表示单聊
    owner_user_id = attr.ib(type=str, default='')  # 群主的user_id，机器人是群主的时候没有这个字段
    owner_open_id = attr.ib(type=str, default='')  # 群主的open_id，机器人是群主的时候没有这个字段


@to_json_decorator
@attr.s
class MinaCodeToSessionResp(object):
    """小程序 code 换取 session 对象
    """
    open_id = attr.ib(type=str, default=None)  # 用户唯一标识,openid 用于在同一个应用中对用户进行标识，用户和应用可以确定一个唯一的 openid
    union_id = attr.ib(type=str, default=None)  # 用户在同一个开发者所属的多个应用中唯一标识,一个用户在同一个开发者所属的多个应用中，unionid 唯一
    session_key = attr.ib(type=str, default=None)  # 会话密钥
    tenant_key = attr.ib(type=str, default=None)  # 用户所在租户唯一标识
    employee_id = attr.ib(type=str, default='')  # 用户在同一个租户下的唯一标识（可选）
    token_type = attr.ib(type=str, default='')  # 此处为Bearer
    access_token = attr.ib(type=str, default='')  # user_access_token，用于获取用户资源
    expires_in = attr.ib(type=int, default=0)  # user_access_token过期时间
    refresh_token = attr.ib(type=str, default='')  # 刷新用户 access_token 时使用的 token


@to_json_decorator
@attr.s
class OAuthCodeToSessionResp(object):
    """获取登录用户身份，OAuth code 换取 session 对象
    """
    access_token = attr.ib(type=str, default=None)  # user_access_token，用于获取用户资源
    avatar_url = attr.ib(type=str, default=None)  # 用户头像
    avatar_thumb = attr.ib(type=str, default=None)  # 用户头像 72x72
    avatar_middle = attr.ib(type=str, default=None)  # 用户头像 240x240
    avatar_big = attr.ib(type=str, default=None)  # 用户头像 640x640
    expires_in = attr.ib(type=int, default=None)  # access_token 的有效期，单位: 秒
    name = attr.ib(type=str, default=None)  # 用户姓名
    en_name = attr.ib(type=str, default=None)  # 用户英文姓名
    open_id = attr.ib(type=str, default=None)  # 用户在应用内的唯一标识
    tenant_key = attr.ib(type=str, default=None)  # 当前企业标识
    refresh_token = attr.ib(type=str, default=None)  # 刷新用户 access_token 时使用的 token
    refresh_expires_in = attr.ib(type=int, default=None)  # refresh_token过期时间，秒数
    token_type = attr.ib(type=str, default=None)  # 此处为 Bearer
