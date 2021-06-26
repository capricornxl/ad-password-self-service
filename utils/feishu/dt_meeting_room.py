# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
from typing import List

import attr

from utils.feishu.dt_code import SimpleUser
from utils.feishu.dt_help import to_json_decorator


@to_json_decorator
@attr.s
class Building(object):
    """建筑物对象
    """
    building_id = attr.ib(type=str, default='')  # 建筑物ID
    description = attr.ib(type=str, default='')  # 建筑物的相关描述
    name = attr.ib(type=str, default='')  # 建筑物名称
    floors = attr.ib(type=List[str], default=attr.Factory(list))  # type: List[str] # 属于当前建筑物的所有楼层列表


@to_json_decorator
@attr.s
class Room(object):
    """会议室对象
    """
    room_id = attr.ib(type=str, default='')  # 会议室ID
    building_id = attr.ib(type=str, default='')  # 会议室所属建筑物ID
    building_name = attr.ib(type=str, default='')  # 会议室所属建筑物名称
    capacity = attr.ib(type=int, default=None)  # 会议室能容纳的人数
    description = attr.ib(type=str, default='')  # 会议室的相关描述
    display_id = attr.ib(type=str, default='')  # 会议室的展示ID
    floor_name = attr.ib(type=str, default='')  # 会议室所在楼层名称
    is_disabled = attr.ib(type=bool, default=False)  # 会议室是否不可用，若会议室不可用，则该值为 True，否则为 False
    name = attr.ib(type=str, default='')  # 会议室名称


@to_json_decorator
@attr.s
class RoomFreeBusy(object):
    """会议室忙闲时间段
    """
    start_time = attr.ib(type=datetime.datetime, default=None)
    end_time = attr.ib(type=datetime.datetime, default=None)
    uid = attr.ib(type=str, default=None)
    original_time = attr.ib(type=int, default=0)
    organizer_info = attr.ib(type=SimpleUser, default=None)
