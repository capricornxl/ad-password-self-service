# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from utils.feishu.dt_calendar import Calendar, CalendarAttendee, CalendarEvent
from utils.feishu.dt_enum import CalendarEventVisibility, CalendarRole
from utils.feishu.dt_help import make_datatype

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark
    from six import string_types

"""
page_token && sync_token
使用 page_token/sync_token 可以方便开发者以“分页”的形式获取日历列表。
max_results 表示一个分页最多包含多少个日历。
假如当次请求返回的结果未包含最后一个日历，response 中会携带 page_token，代表当前分页；
下次请求时带上此 page_token 可以访问下个分页，依此类推。
若 response 中携带了 sync_token，代表当次请求已经是最后分页。若以后还有新增日历，可以通过携带 sync_token 继续访问。
"""


class APICalendarMixin(object):
    def get_calendar_by_id(self, calendar_id):
        """获取日历

        :type self: OpenLark
        :param calendar_id: 日历 ID，来源于 URL 路径，创建日历后也会返回
        :type calendar_id: str
        :return: 日历的对象 Calendar
        :rtype: Calendar

        该接口用于根据日历 ID 获取日历信息。

        https://open.feishu.cn/document/ukTMukTMukTM/uMDN04yM0QjLzQDN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendar_list/{}'.format(calendar_id))
        res = self._get(url, with_tenant_token=True, success_code=200000)
        data = res.get('data', {})
        return make_datatype(Calendar, data)

    def get_calendar_list(self,
                          max_results=500,
                          page_token='',
                          sync_token=''):
        """获取日历列表

        :type self: OpenLark
        :param max_results: 一次请求要求返回最大数，该参数不能大于 1000，默认 500
        :type max_results: int
        :param page_token: 用于标志当次请求从哪页开始，90 天有效期
        :type page_token: str
        :param sync_token: 表示从上次返回的截止页起，返回结果，90 天有效期
        :type sync_token: str
        :return: 两个分页参数，和日历对象 Calendar 的列表
        :rtype: Tuple[str, str, List[Calendar]]

        该接口用于获取应用在企业内的日历列表。

        https://open.feishu.cn/document/ukTMukTMukTM/uMTM14yMxUjLzETN
        """
        if max_results > 1000:
            max_results = 1000

        url = self._gen_request_url('/open-apis/calendar/v3/calendar_list?max_results={}'.format(max_results))
        if page_token:
            url = '{}&page_token={}'.format(url, page_token)
        if sync_token:
            url = '{}&sync_token={}'.format(url, sync_token)

        res = self._get(url, with_tenant_token=True, success_code=200000)
        data = res.get('data', [])
        page_token = res.get('page_token', '')
        sync_token = res.get('sync_token', '')
        calendar_list = [make_datatype(Calendar, i) for i in data]
        return page_token, sync_token, calendar_list

    def create_calendar(self,
                        summary,
                        description='',
                        is_private=False,
                        default_access_role=CalendarRole.free_busy_reader):
        """创建日历

        :type self: OpenLark
        :param summary: 日历标题，最大长度为 256
        :type summary: str
        :param description: 日历描述，最大长度为 256
        :type description: str
        :param is_private: 是否为私有日历，私有日历不可被搜索，默认为false
        :param default_access_role: 表示用户的默认访问权限。取值如下：
                   reader: 订阅者，可查看日程详情
                   free_busy_reader: 游客，只能看到"忙碌/空闲"
        :type default_access_role: CalendarRole
        :return: 日历的对象 Calendar
        :rtype: Calendar

        该接口用于为应用在企业内创建一个日历。

        https://open.feishu.cn/document/ukTMukTMukTM/uQTM14CNxUjL0ETN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendars')
        body = {
            'summary': summary,
            'description': description,
            'is_private': is_private,
            'default_access_role': default_access_role.value
        }
        res = self._post(url, body=body, with_tenant_token=True, success_code=200000)
        data = res.get('data', {})
        return make_datatype(Calendar, data)

    def delete_calendar_by_id(self, calendar_id):
        """删除日历

        :type self: OpenLark
        :param calendar_id: 日历 ID
        :type calendar_id: str

        该接口用于删除应用在企业内的指定日历。

        https://open.feishu.cn/document/ukTMukTMukTM/uUTM14SNxUjL1ETN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendars/{}'.format(calendar_id))
        self._delete(url, with_tenant_token=True, success_code=200000)

    def update_calendar_by_id(self,
                              calendar_id,
                              summary=None,
                              description=None,
                              is_private=None,
                              default_access_role=None):
        """更新日历

        :type self: OpenLark
        :param calendar_id: 日历 ID
        :type calendar_id: str
        :param summary: 日历标题，最大长度为 256
        :type summary: str
        :param description: 日历描述，最大长度为 256
        :type description: str
        :param is_private: 是否为私有日历，私有日历不可被搜索，默认为false
        :type is_private: bool
        :param default_access_role: 表示用户的默认访问权限。取值如下：
                   reader: 订阅者，可查看日程详情
                   free_busy_reader: 游客，只能看到"忙碌/空闲"
        :type default_access_role: CalendarRole
        :return: Calendar 对象
        :rtype: Calendar

        该接口用于修改指定日历的信息。

        https://open.feishu.cn/document/ukTMukTMukTM/uYTM14iNxUjL2ETN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendars/{}'.format(calendar_id))
        body = {}
        for k, v in {
            'summary': summary,
            'description': description,
            'is_private': is_private,
            'default_access_role': default_access_role.value if default_access_role else None,
        }.items():
            if v is not None:
                body[k] = v
        res = self._patch(url, body, with_tenant_token=True, success_code=200000)
        data = res['data']
        return make_datatype(Calendar, data)

    def _gen_calendar_event(self, data):
        """生成 CalendarEvent

        :rtype CalendarEvent
        """
        return CalendarEvent(
            id=data.get('id', ''),
            summary=data.get('summary', ''),
            description=data.get('description', ''),
            start=data.get('start', {}).get('time_stamp', 0),
            end=data.get('end', {}).get('time_stamp', 0),
            visibility=CalendarEventVisibility(data.get('visibility', 'default')),
            attendees=[make_datatype(CalendarAttendee, i) for i in (data.get('attendees') or [])]
        )

    def get_calendar_event(self, calendar_id, event_id):
        """获取日程

        :type self: OpenLark
        :param calendar_id: 日历 ID
        :param event_id: 日程 ID
        :return: 日历事件的对象
        :rtype: CalendarEvent

        该接口用于获取指定日历下的指定日程。

        https://open.feishu.cn/document/ukTMukTMukTM/ucTM14yNxUjL3ETN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendars/{}/events/{}'.format(calendar_id, event_id))
        res = self._get(url, with_tenant_token=True, success_code=200000)
        data = res['data']
        return self._gen_calendar_event(data)

    def create_calendar_event(self,
                              calendar_id,
                              summary,
                              start_timestamp,
                              end_timestamp,
                              description='',
                              attendees=None,
                              visibility=CalendarEventVisibility.default):
        """创建日程

        :type self: OpenLark
        :param calendar_id: 日历 ID
        :type calendar_id: str
        :param summary: 日程标题，最大长度为 256
        :type summary: str
        :param start_timestamp: 日程的起始时间，10 位秒级时间戳
        :type start_timestamp: int
        :param end_timestamp: 日程的结束时间，10 位秒级时间戳
        :type end_timestamp: int
        :param description: 日程描述，最大长度为 256，默认空
        :type description: str
        :param attendees: 日程参与者信息，默认空数组，每个 Attendess 必须有 open_id 或者 employee_id
        :type attendees: List[CalendarAttendee]
        :param visibility: 公开范围
        :type visibility: CalendarEventVisibility
        :return: 日历事件的对象
        :rtype: CalendarEvent

        该接口用于在日历中创建一个日程。

        https://open.feishu.cn/document/ukTMukTMukTM/ugTM14COxUjL4ETN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendars/{}/events'.format(calendar_id))
        if not attendees:
            attendees = []
        else:
            attendees = [dict(filter(lambda x: x[1], [('open_id', i.open_id),
                                                      ('employee_id', i.employee_id),
                                                      ('display_name', i.display_name)])) for i in attendees]

        body = {
            'summary': summary,
            'description': description,
            'start': {
                'time_stamp': start_timestamp,
            },
            'end': {
                'time_stamp': end_timestamp,
            },
            'attendees': attendees,  # type: ignore
            'visibility': visibility.value if isinstance(visibility, CalendarEventVisibility) else visibility,
        }
        res = self._post(url, body, with_tenant_token=True, success_code=200000)
        data = res['data']
        return self._gen_calendar_event(data)

    def get_calendar_event_list(self,
                                calendar_id,
                                max_results=500,
                                page_token='',
                                sync_token=''):
        """获取日程列表

        :type self: OpenLark
        :param calendar_id: 日历 ID
        :type calendar_id: str
        :param max_results: 一次请求要求返回最大数，该参数不能大于 1000，默认 500
        :param page_token: 用于标志当次请求从哪页开始
        :type page_token: str
        :param sync_token: 表示从上次返回的截止页起，返回结果
        :type sync_token: str
        :return: page_token, sync_token 和 日历事件的列表
        :rtype: Tuple[str, str, List[CalendarEvent]]

        该接口用于获取指定日历下的日程列表。

        https://open.feishu.cn/document/ukTMukTMukTM/ukTM14SOxUjL5ETN
        """
        if max_results > 1000:
            max_results = 1000

        url = self._gen_request_url(
            '/open-apis/calendar/v3/calendars/{}/events?max_results={}'.format(calendar_id, max_results))
        if page_token:
            url = '{}&page_token={}'.format(url, page_token)
        if sync_token:
            url = '{}&sync_token={}'.format(url, sync_token)

        res = self._get(url, with_tenant_token=True, success_code=200000)
        data = res.get('data', [])
        page_token = res.get('page_token', '')
        sync_token = res.get('sync_token', '')
        calendar_event_list = [self._gen_calendar_event(i) for i in data]
        return page_token, sync_token, calendar_event_list

    def delete_calendar_event(self, calendar_id, event_id=''):
        """删除日程

        :type self: OpenLark
        :param calendar_id: 日历 ID
        :param event_id: 日程 ID

        该接口用于删除指定日历下的日程。

        https://open.feishu.cn/document/ukTMukTMukTM/uAjM14CMyUjLwITN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendars/{}/events/{}'.format(calendar_id, event_id))
        self._delete(url, with_tenant_token=True, success_code=200000)

    def update_calendar_event(self,
                              calendar_id,
                              event_id,
                              summary=None,
                              start_timestamp=None,
                              end_timestamp=None,
                              description=None,
                              attendees=None,
                              visibility=None):
        """更新日程

        :type self: OpenLark
        :param calendar_id: 日历 ID
        :type calendar_id: str
        :param event_id: 日程 ID
        :type event_id: str
        :param summary: 日程标题，最大长度为 256
        :type summary: str
        :param start_timestamp: 日程的起始时间，10 位秒级时间戳
        :type start_timestamp: int
        :param end_timestamp: 日程的结束时间，10 位秒级时间戳
        :type end_timestamp: int
        :param description: 日程描述，最大长度为 256，默认空
        :type description: str
        :param attendees: 日程参与者信息，默认空数组，每个 Attendess 必须有 open_id 或者 employee_id
        :type attendees: List[CalendarAttendee]
        :param visibility: 公开范围
        :type visibility: CalendarEventVisibility
        :return: 日历事件
        :rtype: CalendarEvent

        该接口用于在日历中创建一个日程。

        https://open.feishu.cn/document/ukTMukTMukTM/uEjM14SMyUjLxITN
        """
        url = self._gen_request_url('/open-apis/calendar/v3/calendars/{}/events/{}'.format(calendar_id, event_id))
        if not attendees:
            attendees = []
        else:
            attendees = [dict(filter(lambda x: x[1], [('open_id', i.open_id),
                                                      ('employee_id', i.employee_id),
                                                      ('display_name', i.display_name)])) for i in attendees]

        body = {}  # type: Dict[string_types, Any]
        if summary is not None:
            body['summary'] = summary
        if description is not None:
            body['description'] = description
        if start_timestamp is not None:
            body['start'] = {'time_stamp': start_timestamp}
        if end_timestamp is not None:
            body['end'] = {'time_stamp': end_timestamp}
        if attendees is not None:
            body['attendees'] = attendees
        if visibility is not None:
            body['visibility'] = visibility.value if isinstance(visibility, CalendarEventVisibility) else visibility
        res = self._patch(url, body, with_tenant_token=True, success_code=200000)
        data = res['data']
        return self._gen_calendar_event(data)

# TODO:

# 邀请/移除日程参与者

# 获取访问控制列表

# 创建访问控制

# 删除访问控制

# 查询日历的忙闲状态
