# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import time
from datetime import datetime
from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING

from six import PY2, string_types
from six.moves.urllib.request import urlretrieve

from utils.feishu.exception import LarkInvalidArguments

if TYPE_CHECKING:
    from datetime import tzinfo


def to_timestamp(t):
    """

    :param t:
    :type t: datetime
    :return:
    :rtype: int
    """
    try:
        return int(t.timestamp())
    except AttributeError:
        return int((time.mktime(t.timetuple()) + t.microsecond / 1000000.0))


def to_native(s):
    """转成 str

    :type s: Union[str, bytes]
    :rtype str
    """
    if isinstance(s, bytes):
        return s.decode('utf-8')
    return s


def _read_from_url(url):
    filename, _ = urlretrieve(url)
    return open(filename, 'rb')


def _read_from_file(file):
    return open(file, 'rb')


def to_file_like(image):
    """
    :param image:
    :type image: Union[string_types, bytes, BytesIO]
    :return:
    """
    if isinstance(image, bytes):
        return BytesIO(image)

    if isinstance(image, string_types):
        if image.startswith(str('http://')) or image.startswith(str('https://')):
            return _read_from_url(image)

        return _read_from_file(image)

    return image


def converter_enum(value, ranges=None):
    v = value.value if isinstance(value, Enum) else value

    if ranges is not None:
        ranges_v = [i.value if isinstance(i, Enum) else i for i in ranges]
        if v not in ranges_v:
            raise LarkInvalidArguments(msg='enum: %s should be in ranges: %s' % (v, ' / '.join(map(str, ranges_v))))

    return v


def datetime_format_rfc3339(d, default_tz=None):
    """datetime 转 RFC3339 格式的时间字符串

    :param d: datetime
    :type d: datetime
    :param default_tz:
    :type default_tz: tzinfo
    :return: RFC3339 格式的时间字符串
    :rtype: str
    """
    # 如果没有时区，给一个 default_tz
    if not d.tzinfo and default_tz:
        d = d.replace(tzinfo=default_tz)

    return d.astimezone(d.tzinfo).isoformat()


def join_url(base_url, qs, sep='?'):
    url = base_url
    qs = '&'.join(map(lambda x: '{}={}'.format(x[0], x[1]), filter(lambda x: x[1], qs)))
    if qs:
        url = url + sep + qs

    return url


def join_dict(base, d):
    for i in d:
        key, val = i[0], i[1]
        if isinstance(val, bool):
            if val is not None:
                base[key] = val
        else:
            if val:
                base[key] = val
    return base


def pop_or_none(d, key):
    try:
        return d.pop(key)
    except KeyError:
        return
