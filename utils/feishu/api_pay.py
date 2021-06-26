# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, Any, Dict, List, Tuple

from utils.feishu.dt_code import Chat, DetailChat
from utils.feishu.dt_help import make_datatype
from utils.feishu.dt_pay import PayOrder
from utils.feishu.exception import LarkInvalidArguments
from utils.feishu.helper import join_url

if TYPE_CHECKING:
    from utils.feishu.api import OpenLark
    from six import string_types


class APIPayMixin(object):
    def is_user_in_paid_scope(self, open_id=None, user_id=None):
        """查询用户是否在应用开通范围

        :type self: OpenLark
        :param open_id: 用户 open_id，open_id 和 user_id 两个参数必须包含其一，若同时传入取 open_id
        :type open_id: str
        :param user_id: 用户 user_id，user_id 和 open_id 两个参数必须包含其一，若同时传入取 open_id
        :type user_id: str
        :return status: 用户是否在开通范围中，"valid" -该用户在开通范围中，"not_in_scope"-该用户不在开通范围中，
                        "no_active_license"-租户未购买任何价格方案或价格方案已过期
        :return price_plan_id: 租户当前使用的「价格方案ID」，对应开发者后台中「价格方案配置」中的「价格方案」
        :return is_trial: 是否为试用版本，true-是试用版本；false-非试用版本
        :return service_stop_time: 租户当前有生效价格方案时表示价格方案的到期时间，为时间unix时间戳
        :return: 状态, 付费方案, 是否是适用版本, 到期时间
        :rtype: (str, str, bool, int)

        该接口用于查询用户是否在企业管理员设置的使用该应用的范围中。

        如果设置的付费套餐是按人收费或者限制了最大人数，开放平台会引导企业管理员设置“付费功能开通范围”，

        本接口用于查询用户是否在企业管理员设置的使用该应用的范围中，可以通过此接口，在付费功能点入口判断是否允许某个用户进入使用。

        https://open.feishu.cn/document/ukTMukTMukTM/uATNwUjLwUDM14CM1ATN
        """
        url = self._gen_request_url('/open-apis/pay/v1/paid_scope/check_user?')
        if open_id:
            url = '{}open_id={}'.format(url, open_id)
        if user_id:
            url = '{}user_id={}'.format(url, user_id)

        res = self._get(url, with_tenant_token=True)
        data = res['data']

        status = data.get('status')
        price_plan_id = data.get('price_plan_id')
        is_trial = data.get('is_trial')
        service_stop_time = data.get('service_stop_time')

        if service_stop_time:
            try:
                service_stop_time = int(service_stop_time)
            except Exception:
                pass

        return status, price_plan_id, is_trial, service_stop_time

    def get_pay_orders(self, status='all', page_size=20, page_token='', tenant_key=None):
        """查询租户购买的付费方案

        :type self: OpenLark
        :param status: 获取用户购买套餐信息设置的过滤条件，normal为正常状态，refund为已退款，为空或者all表示所有，未支付的订单无法查到
        :type status: str
        :param page_size: 每页显示的订单数量
        :type page_size: str
        :param page_token: 翻页标识，可以从上次请求的响应中获取，不填或者为空时表示从开头获取
        :type page_token: str
        :param tenant_key: 购买应用的租户唯一标识，为空表示获取应用下所有订单，有值表示获取应用下该租户购买的订单
        :type tenant_key: str

        查询应用租户下的付费订单

        该接口用于分页查询应用租户下的已付费订单，每次购买对应一个唯一的订单，订单会记录购买的套餐的相关信息，

        业务方需要自行处理套餐的有效期和付费方案的升级。

        https://open.feishu.cn/document/ukTMukTMukTM/uETNwUjLxUDM14SM1ATN
        """
        url = self._gen_request_url('/open-apis/pay/v1/order/list')
        qs = [
            ('status', status),
            ('page_size', page_size),
            ('page_token', page_token),
            ('tenant_key', tenant_key)
        ]
        url = join_url(url, qs, sep='?')

        res = self._get(url, with_app_token=True)
        data = res['data']

        total = data.get('total')
        has_more = data.get('has_more')
        page_token = data.get('page_token')
        orders = [make_datatype(PayOrder, i) for i in data.get('order_list', [])]

        return has_more, page_token, total, orders

    def get_pay_order_detail(self, order_id):
        """查询订单详情

        :type self: OpenLark
        :param order_id: 获取用户购买套餐信息设置的过滤条件，normal为正常状态，refund为已退款，为空或者all表示所有，未支付的订单无法查到
        :type order_id: str

        该接口用于查询某个订单的具体信息

        https://open.feishu.cn/document/ukTMukTMukTM/uITNwUjLyUDM14iM1ATN
        """
        url = self._gen_request_url('/open-apis/pay/v1/order/get?order_id={}'.format(order_id))

        res = self._get(url, with_app_token=True)

        data = res['data']

        total = data.get('total')
        has_more = data.get('has_more')
        page_token = data.get('page_token')
        orders = [make_datatype(PayOrder, i) for i in data.get('order_list', [])]

        return has_more, page_token, total, orders
