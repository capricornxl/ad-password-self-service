# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import List

import attr

from utils.feishu.dt_enum import CalendarEventVisibility, CalendarRole
from utils.feishu.dt_help import to_json_decorator


@to_json_decorator
@attr.s
class Calendar(object):
    """日历对象
    """
    id = attr.ib(type=str, default=None)
    summary = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    default_access_role = attr.ib(type=CalendarRole, default=None)
    is_private = attr.ib(type=bool, default=None)


# ----- 日历日程


@to_json_decorator
@attr.s
class CalendarAttendee(object):
    """日历的参与人对象
    """
    open_id = attr.ib(type=str, default='')
    employee_id = attr.ib(type=str, default='')
    optional = attr.ib(type=bool, default=None)
    display_name = attr.ib(type=str, default='')


@attr.s
class CalendarEvent(object):
    """日历的日程对象
    """
    id = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    start = attr.ib(type=int, default=None)
    end = attr.ib(type=int, default=None)
    visibility = attr.ib(type=CalendarEventVisibility, default=CalendarEventVisibility.default)
    summary = attr.ib(type=str, default='')
    attendees = attr.ib(type=List[CalendarAttendee], default=attr.Factory(list))
