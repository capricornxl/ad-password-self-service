# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import attr

from utils.feishu.dt_enum import PayBuyType, PayPricePlanType, PayStatus
from utils.feishu.dt_help import to_json_decorator


@to_json_decorator
@attr.s
class PayOrder(object):
    order_id = attr.ib(type=str, default='')  # 订单ID，唯一标识
    price_plan_id = attr.ib(type=str, default='')  # 价格方案ID，唯一标识
    price_plan_type = attr.ib(type=PayPricePlanType, default=None)  # 价格方案类型
    seats = attr.ib(type=int, default=0)  # 实际购买人数，仅对price_plan_type为per_seat_per_year和per_seat_per_month 有效
    buy_count = attr.ib(type=int, default=0)  # 购买数量，总是为1
    create_time = attr.ib(type=str, default='')  # 订单创建时间戳
    pay_time = attr.ib(type=str, default='')  # 订单支付时间戳
    status = attr.ib(type=PayStatus, default=None)  # 订单当前状态
    buy_type = attr.ib(type=PayBuyType, default=None)  # 购买类型
    src_order_id = attr.ib(type=str, default='')  # 源订单ID，当前订单为升级购买时，即buy_type为upgrade时，此字段记录源订单等ID
    # 升级后的新订单ID，当前订单如果做过升级购买，此字段记录升级购买后生成的新订单ID，当前订单仍然有效
    dst_order_id = attr.ib(type=str, default='')
    order_pay_price = attr.ib(type=int, default=0)  # 订单实际支付金额, 单位分
    tenant_key = attr.ib(type=str, default='')  # 租户唯一标识
