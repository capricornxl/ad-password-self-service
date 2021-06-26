# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from typing import TYPE_CHECKING, Any, Dict, List

import attr

from utils.feishu.dt_enum import ImageColor
from utils.feishu.dt_help import to_json_decorator
from utils.feishu.exception import LarkInvalidArguments

if TYPE_CHECKING:
    from six import string_types


# 文字，图片，at，link，这四个在post和card中都有，做统一处理
# 富文本：https://lark-open.bytedance.net/document/ukTMukTMukTM/uMDMxEjLzATMx4yMwETM
# 卡片：https://lark-open.bytedance.net/document/ukTMukTMukTM/uUzMxEjL1MTMx4SNzETM


@to_json_decorator
@attr.s
class I18nText(object):
    text = attr.ib(type=str, default=None)
    zh_cn = attr.ib(type=str, default=None)  # 如果设置了，那么国际化中文环境会显示
    en_us = attr.ib(type=str, default=None)  # 如果设置了，那么国际化日文环境会显示
    ja_jp = attr.ib(type=str, default=None)  # 如果设置了，那么国际化英文环境会显示

    def as_dict(self):
        return {
            'text': self.text,
            'i18n': {
                'zh_cn': self.zh_cn or self.text,
                'en_us': self.en_us or self.text,
                'ja_jp': self.ja_jp or self.text,
            }
        }


@to_json_decorator
@attr.s
class MessageText(object):
    text = attr.ib(type=str, default=None)
    zh_cn = attr.ib(type=str, default=None)  # card 格式有效：如果设置了，那么国际化中文环境会显示
    en_us = attr.ib(type=str, default=None)  # card 格式有效：如果设置了，那么国际化日文环境会显示
    ja_jp = attr.ib(type=str, default=None)  # card 格式有效：如果设置了，那么国际化英文环境会显示
    lines = attr.ib(type=int, default=None)  # 只能在富文本消息中起作用，最大显示行数
    un_escape = attr.ib(type=bool, default=None)  # 只能在富文本消息中起作用，表示为 unescape 解码

    def as_post_dict(self):
        if self.zh_cn or self.en_us or self.ja_jp:
            logging.warning('zh_cn or en_us or ja_jp is for card text')

        text = ''
        for i in [self.text, self.zh_cn, self.en_us, self.ja_jp]:
            if i is not None:
                text = i
                break
        d = {
            'tag': 'text',
            'text': text,
        }
        for i in ['un_escape', 'lines']:
            r = getattr(self, i)
            if r is not None:
                d[i] = r

        return d

    def as_card_dict(self):
        if self.lines is not None:
            logging.warning('lines is for post text')
        if self.un_escape is not None:
            logging.warning('un_escape is for post text')

        return {
            'tag': 'text',
            'text': self.text,
            'i18n': {
                'zh_cn': self.zh_cn or self.text,
                'en_us': self.en_us or self.text,
                'ja_jp': self.ja_jp or self.text,
            }
        }


@to_json_decorator
@attr.s
class MessageAt(object):
    """富文本的at消息
    """
    user_id = attr.ib(type=str, default=None)  # open_id 或者 employee_id
    text = attr.ib(type=str, default=None)  # 用户名

    def as_dict(self):
        return {
            'tag': 'at',
            'user_id': self.user_id,
            'text': self.text,
        }

    as_post_dict = as_dict
    as_card_dict = as_dict


@to_json_decorator
@attr.s
class MessageImage(object):
    """富文本的图片消息
    """
    # 图片的唯一标识，可以通过图片上传接口获得: https://lark-open.bytedance.net/document/ukTMukTMukTM/uEDO04SM4QjLxgDN
    image_key = attr.ib(type=str, default=None)
    height = attr.ib(type=int, default=None)  # 图片的宽
    width = attr.ib(type=int, default=None)  # 图片的高

    def as_dict(self):
        return {
            'tag': 'img',
            'image_key': self.image_key,
            'height': self.height,
            'width': self.width
        }

    as_post_dict = as_dict
    as_card_dict = as_dict


@to_json_decorator
@attr.s
class MessageLink(object):
    text = attr.ib(type=str, default=None)
    href = attr.ib(type=str, default=None)  # 默认的链接地址，如果这个没有写，从下面三个取一个
    un_escape = attr.ib(type=bool, default=None)

    # 以下配置只在 card 有效
    zh_cn = attr.ib(type=str, default=None)  # card有效：如果设置了，那么国际化中文环境会显示
    en_us = attr.ib(type=str, default=None)  # card有效：如果设置了，那么国际化日文环境会显示
    ja_jp = attr.ib(type=str, default=None)  # card有效：如果设置了，那么国际化英文环境会显示
    pc_href = attr.ib(type=str, default=None)  # card有效：PC 端的链接地址
    ios_href = attr.ib(type=str, default=None)  # card有效：iOS 端的链接地址
    android_href = attr.ib(type=str, default=None)  # card有效：Android 端的链接地址

    def as_post_dict(self):
        i18n_text = self.zh_cn or self.en_us or self.ja_jp
        if i18n_text:
            logging.warning('zh_cn or en_us or ja_jp is for card text')
        multi_platform_href = self.pc_href or self.ios_href or self.android_href
        if multi_platform_href:
            logging.warning('pc_href or ios_href or android_href is for card text')

        text = self.text or i18n_text
        if text is None:
            raise LarkInvalidArguments(msg='[message] empty text')

        href = self.href or multi_platform_href
        if href is None:
            raise LarkInvalidArguments(msg='[message] empty href')

        d = {
            'tag': 'a',
            'text': text,
            'href': href,
        }  # type: Dict[string_types, Any]
        if self.un_escape is not None:
            d['un_escape'] = self.un_escape

        return d

    def as_card_dict(self):
        return {
            'tag': 'a',
            'text': self.text,
            'i18n': {
                'zh_cn': self.zh_cn or self.text,
                'en_us': self.en_us or self.text,
                'ja_jp': self.ja_jp or self.text,
            },
            'href': {
                'href': self.href,
                'pc_href': self.pc_href,
                'ios_href': self.ios_href,
                'android_href': self.android_href,
            }
        }


@to_json_decorator
@attr.s
class CardURL(object):
    """多设备 URL
    """
    href = attr.ib(type=str, default=None)  # 默认的链接地址，如果这个没有写，从下面三个取一个
    pc_href = attr.ib(type=str, default=None)  # PC 端的链接地址
    ios_href = attr.ib(type=str, default=None)  # iOS 端的链接地址
    android_href = attr.ib(type=str, default=None)  # Android 端的链接地址

    def as_card_dict(self):
        d = {'href': self.href}
        for i in ['pc_href', 'ios_href', 'android_href']:
            href = getattr(self, i)
            if not href:
                continue
            d[i] = href
            if not d['href']:
                d['href'] = href
        return d

    def as_button_dict(self):
        d = {}
        if self.pc_href:
            d['pc_url'] = self.pc_href or self.href
        if self.ios_href:
            d['ios_url'] = self.ios_href or self.href
        if self.android_href:
            d['android_url'] = self.android_href or self.href
        return d


@to_json_decorator
@attr.s
class CardHeader(object):
    title = attr.ib(type=str, default=None)  # 显示的默认的文本内容,如果设置了 i18n 内容，会优先显示 i18n 里面对应的语种内容
    zh_cn = attr.ib(type=str, default=None)  # 如果设置了，那么国际化中文环境会显示
    en_us = attr.ib(type=str, default=None)  # 如果设置了，那么国际化日文环境会显示
    ja_jp = attr.ib(type=str, default=None)  # 如果设置了，那么国际化英文环境会显示
    # 标题前图标的颜色。可选范围：[orange, red, yellow, gray, blue, green] 默认为 red
    image_color = attr.ib(type=ImageColor, default=ImageColor.red)
    lines = attr.ib(type=int, default=None)  # 指定文本最大显示行数，0 表示不限行数

    def as_dict(self):
        d = {'title': self.title, 'image_color': self.image_color.value}
        if self.lines:
            d['lines'] = self.lines
        if self.zh_cn or self.en_us or self.ja_jp:
            d['i18n'] = {
                'zh_cn': self.zh_cn or self.title,
                'en_us': self.en_us or self.title,
                'ja_jp': self.ja_jp or self.title,
            }
        return d


@to_json_decorator
@attr.s
class CardButton(object):
    text = attr.ib(type=str, default=None)

    # 发送 post 请求
    method = attr.ib(type=str, default=None)

    # 请求或者跳转的地址
    url = attr.ib(type=str, default=None)

    # 标题的 i18n
    text_i18n = attr.ib(type=I18nText, default=None)

    # 点击按钮以后显示的默认的文本内容，仅在 method 是 post 或 get 时候才有效
    triggered_text = attr.ib(type=str, default=None)

    # 点击按钮以后国际化内容的字段，仅在 method 是 post 或 get 时候才有效
    triggered_i18n = attr.ib(type=I18nText, default=None)

    # 为 true 时，请求参数会带上 open_id 或者 employee_id，仅在 method 是 post 时候才有效
    need_user_info = attr.ib(type=bool, default=None)

    # 为 true 时，请求参数会带上 open_message_id，仅在 method 是 post 时候才有效
    need_message_info = attr.ib(type=bool, default=None)

    # 开发者自定义的请求参数，仅在 method 是 post 时候才有效
    parameter = attr.ib(type=Any, default=None)

    # 可包含 pc_url, ios_url, android_url, 仅在 method 是 jump 时候才有效. 如果配置了该字段, 则在相应端上优先使用指定的链接
    open_url = attr.ib(type=CardURL, default=None)

    # 配置是否点击成功后，需要将其它按钮隐藏，仅在 method 是 post 或 get 时候才有效
    hide_others = attr.ib(type=bool, default=None)

    def as_dict(self):
        d = {
            'text': self.text,
            'method': self.method,
            'url': self.url,
        }  # type: Dict[string_types, Any]
        if self.text_i18n:
            d['i18n'] = self.text_i18n.as_dict()
        if self.triggered_i18n:
            d['triggered_i18n'] = self.triggered_i18n.as_dict()
        if self.open_url:
            d['open_url'] = self.open_url.as_button_dict()

        for i in ['triggered_text', 'need_user_info', 'need_message_info', 'parameter', 'hide_others']:
            r = getattr(self, i, None)
            if r is not None:
                d[i] = r

        return d

    as_post_dict = as_dict
    as_card_dict = as_dict


@to_json_decorator
@attr.s
class CardAction(object):
    buttons = attr.ib(type=List[CardButton], default=None)  # type: List[CardButton]
    changeable = attr.ib(type=bool, default=None)

    def as_dict(self):
        d = {'buttons': [i.as_dict() for i in self.buttons]}  # type: Dict[string_types, Any]
        if self.changeable is not None:
            d['changeable'] = self.changeable
        return d
