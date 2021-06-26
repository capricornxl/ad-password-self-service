# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import attr

from utils.feishu.dt_enum import I18NType
from utils.feishu.dt_help import int_convert_bool, to_json_decorator


@to_json_decorator
@attr.s
class App(object):
    """应用
    """
    app_id = attr.ib(type=str, default='')  # 应用ID
    app_name = attr.ib(type=str, default='')  # 应用名称
    description = attr.ib(type=str, default='')  # 应用描述
    is_isv = attr.ib(type=bool, default=False, metadata={'json': 'app_scene_type'},
                     converter=int_convert_bool)  # 是否是ISV
    avatar_url = attr.ib(type=str, default='')  # 应用Icon
    primary_language = attr.ib(type=I18NType, default=I18NType.zh_cn)  # 应用首选语言
    status = attr.ib(type=int, default=0)  # 是否是启用
