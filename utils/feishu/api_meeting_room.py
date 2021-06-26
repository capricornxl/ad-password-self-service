# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
from typing import TYPE_CHECKING, List

from dateutil import parser
from six.moves.urllib.parse import urlencode

from utils.feishu.dt_code import SimpleUser
from utils.feishu.dt_help import make_datatype
from utils.feishu.dt_meeting_room import Building, Room, RoomFreeBusy
from utils.feishu.helper import converter_enum, datetime_format_rfc3339

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark


class TimeZoneChina(datetime.tzinfo):
    _offset = datetime.timedelta(hours=8)
    _dst = datetime.timedelta(0)
    _name = "+08"

    def utcoffset(self, dt):
        return self.__class__._offset

    def dst(self, dt):
        return self.__class__._dst

    def tzname(self, dt):
        return self.__class__._name


class APIMeetingRoomMixin(object):
    def get_building_list(self, page_size=10, page_token='', order_by='', fields=None):
        """获取建筑物列表

        :type self: OpenLark
        :param page_size: 可选参数，请求期望返回的建筑物数量，不足则返回全部，该值默认为 10，最大为 100
        :type page_size: int
        :param page_token: 可选参数，用于标记当前请求的页数，将返回以当前页开始，往后 page_size 个元素
        :type page_token: str
        :param order_by: 可选参数，提供用于对名称进行升序/降序排序的方式查询，可选项有："name-asc,name-desc"，传入其他字符串不做处理，默认无序
        :type order_by: str
        :param fields: 可选参数，可选字段有："id,name,description,floors"，默认返回所有字段
        :type fields: list[str]
        :return: has_more, page_token, 建筑物列表
        :rtype: (bool, str, list[Building])

        该接口用于获取本企业下的建筑物（办公大楼）。

        https://open.feishu.cn/document/ukTMukTMukTM/ugzNyUjL4cjM14CO3ITN
        """
        if page_size > 100:
            page_size = 100
        elif page_size <= 0:
            page_size = 10

        params = {
            'page_size': page_size,
        }
        if page_token:
            params['page_token'] = page_token
        if order_by:
            params['order_by'] = order_by
        if fields:
            params['fields'] = ','.join(fields)

        url = self._gen_request_url('/open-apis/meeting_room/building/list?{}'.format(urlencode(params)))
        res = self._get(url, with_tenant_token=True)
        data = res['data']

        has_more = data.get('has_more', False)
        page_token = data.get('page_token', '')
        building_list = [make_datatype(Building, i) for i in data.get('buildings', [])]
        return has_more, page_token, building_list

    def batch_get_building(self, building_ids, fields=None):
        """查询建筑物详情

        :type self: OpenLark
        :param building_ids: 必须参数，用于查询指定建筑物的ID列表
        :type building_ids: list[str]
        :param fields: 可选参数，用于指定返回的字段名，可选字段有："id,name,description,floors"，默认返回所有字段
        :return: 建筑物列表
        :rtype: list[Building]

        https://open.feishu.cn/document/ukTMukTMukTM/ukzNyUjL5cjM14SO3ITN
        """
        params = {
            'building_ids': building_ids,
        }
        if fields:
            params['fields'] = ','.join(fields)

        url = self._gen_request_url(
            '/open-apis/meeting_room/building/batch_get?{}'.format(urlencode(params, doseq=True)))

        res = self._get(url, with_tenant_token=True)
        data = res.get('data', {})
        buildings = data.get('buildings', [])
        building_list = [make_datatype(Building, i) for i in buildings]

        return building_list

    def get_room_list(self, building_id, page_size=100, page_token='', order_by='', fields=None):
        """获取会议室列表

        :type self: OpenLark
        :param building_id: 被查询的建筑物ID
        :type building_id: str
        :param page_size: 请求期望返回的会议室数量，不足则返回全部，该值默认为 100，最大为 1000
        :type page_size: int
        :param page_token: 用于标记当前请求的页数，将返回以当前页开始，往后 page_size 个元素
        :type page_token: str
        :param order_by: 提供用于对名称/楼层进行升序/降序排序的方式查询，可选项有："name-asc,name-desc,floor_name-asc,
                         floor_name-desc"，传入其他字符串不做处理，默认无序
        :type order_by: str
        :param fields: 可选字段有："id,name,description,capacity,building_id,building_name,floor_name,is_disabled,
                       display_id"，默认返回所有字段
        :type fields: list[str]
        :return: has_more, page_token, 会议室列表
        :rtype: (bool, str, list[Room])

        https://open.feishu.cn/document/ukTMukTMukTM/uADOyUjLwgjM14CM4ITN
        """
        if page_size > 1000:
            page_size = 1000
        elif page_size <= 0:
            page_size = 100

        params = {
            'building_id': building_id,
            'page_size': page_size
        }
        if page_token:
            params['page_token'] = page_token
        if order_by:
            params['order_by'] = order_by
        if fields:
            params['fields'] = ','.join(fields)

        url = self._gen_request_url('/open-apis/meeting_room/room/list?{}'.format(urlencode(params)))
        res = self._get(url, with_tenant_token=True)
        data = res.get('data', {})
        rooms = data.get('rooms', [])

        has_more = data.get('has_more', False)
        page_token = data.get('page_token', '')
        room_list = [make_datatype(Room, i) for i in rooms]
        return has_more, page_token, room_list

    def batch_get_room_list(self, room_ids, fields=None):
        """查询会议室详情

        :type self: OpenLark
        :param room_ids: 用于查询指定会议室的ID列表
        :type room_ids: List[str]
        :param fields: 可选字段有："id,name,description,capacity,building_id,building_name,floor_name,is_disabled,
                       display_id"，默认返回所有字段
        :return: 会议室列表
        :rtype: list[Room]

        https://open.feishu.cn/document/ukTMukTMukTM/uEDOyUjLxgjM14SM4ITN
        """
        params = {
            'room_ids': room_ids,
        }
        if fields:
            params['fields'] = ','.join(fields)

        url = self._gen_request_url('/open-apis/meeting_room/room/batch_get?{}'.format(urlencode(params, doseq=True)))

        res = self._get(url, with_tenant_token=True)
        data = res.get('data', {})
        rooms = data.get('rooms', [])
        room_list = [make_datatype(Room, i) for i in rooms]

        return room_list

    def batch_get_room_freebusy(self, room_ids, time_min, time_max):
        """会议室忙闲查询

        :type self: OpenLark
        :param room_ids: 用于查询指定会议室的ID列表
        :type room_ids: list[str]
        :param time_min: 查询会议室忙闲的起始时间
        :type time_min: datetime.datetime
        :param time_max: 查询会议室忙闲的结束时间
        :type time_max: datetime.datetime
        :return: 查询会议室忙闲的起始时间(与请求参数完全相同), 查询会议室忙闲的结束时间(与请求参数完全相同), Dict['会议室ID', List[忙碌时间]]
        :rtype: (datetime.datetime, datetime.datetime, dict[str, list[RoomFreeBusy]])

        https://open.feishu.cn/document/ukTMukTMukTM/uIDOyUjLygjM14iM4ITN
        """
        tz = TimeZoneChina()
        params = {
            'room_ids': room_ids,
            'time_min': datetime_format_rfc3339(time_min, tz),
            'time_max': datetime_format_rfc3339(time_max, tz)
        }

        url = self._gen_request_url(
            '/open-apis/meeting_room/freebusy/batch_get?{}'.format(urlencode(params, doseq=True)))

        res = self._get(url, with_tenant_token=True)
        data = res.get('data', {})
        time_min = data.get('time_min')
        time_max = data.get('time_max')
        if time_min:
            time_min = parser.parse(time_min)
        if time_max:
            time_max = parser.parse(time_max)

        return time_min, time_max, {
            k: [RoomFreeBusy(
                start_time=parser.parse(i.get('start_time')),
                end_time=parser.parse(i.get('end_time')),
                uid=i.get('uid'),
                original_time=i.get('original_time'),
                organizer_info=make_datatype(SimpleUser, i.get('organizer_info'))
            ) for i in v]
            for k, v in data.get('free_busy', {}).items()}

    def reply_meeting(self, room_id, uid, original_time, status):
        """回复会议室日程实例

        :type self: OpenLark
        :param room_id: 会议室的 ID
        :type room_id: str
        :param uid: 会议室的日程 ID
        :type uid: str
        :param original_time: 日程实例原始时间，非重复日程必为0。重复日程若为0则表示回复其所有实例，否则表示回复单个实例。
        :type original_time: int
        :param status: 回复状态，NOT_CHECK_IN 表示未签到，ENDED_BEFORE_DUE 表示提前结束
        :type status: MeetingReplyStatus
        :return: 查询会议室忙闲的起始时间(与请求参数完全相同), 查询会议室忙闲的结束时间(与请求参数完全相同), Dict['会议室ID', List[忙碌时间]]
        :rtype: (datetime.datetime, datetime.datetime, dict[str, list[RoomFreeBusy]])

        https://open.feishu.cn/document/ukTMukTMukTM/uIDOyUjLygjM14iM4ITN
        """
        body = {
            'room_id': room_id,
            'uid': uid,
            'original_time': original_time,
            'status': converter_enum(status),
        }
        url = self._gen_request_url('/open-apis/meeting_room/instance/reply')

        self._post(url, body=body, with_tenant_token=True)
