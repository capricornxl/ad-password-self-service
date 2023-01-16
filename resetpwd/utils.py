#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @FileName：     utils.py
# @Software:      
# @Author:         Leven Xiang
# @Mail:           xiangle0109@outlook.com
# @Date：          2021/5/20 8:47

from django.shortcuts import render
import logging
from ldap3.core.exceptions import LDAPException
from django.conf import settings
import os

APP_ENV = os.getenv('APP_ENV')
if APP_ENV == 'dev':
    from conf.local_settings_dev import *
else:
    from conf.local_settings import *

logger = logging.getLogger('django')


def code_2_user_detail(ops, home_url, code):
    """
    临时授权码换取userinfo
    """
    _, s, e = ops.get_user_detail(code=code, home_url=home_url)
    return _, s, e


def code_2_user_info_with_oauth2(ops, request, msg_template, home_url, code):
    """
    临时授权码换取userinfo
    """
    _status, user_id = ops.get_user_id_by_code(code)
    # 判断 user_id 在本企业钉钉/微信中是否存在
    if not _status:
        context = {'global_title': TITLE,
                   'msg': '获取userid失败，错误信息：{}'.format(user_id),
                   'button_click': "window.location.href='%s'" % home_url,
                   'button_display': "返回主页"
                   }
        return False, context, user_id
    detail_status, user_info = ops.get_user_detail_by_user_id(user_id)
    if not detail_status:
        context = {'global_title': TITLE,
                   'msg': '获取用户信息失败，错误信息：{}'.format(user_info),
                   'button_click': "window.location.href='%s'" % home_url,
                   'button_display': "返回主页"
                   }
        return False, context, user_info
    return True, user_id, user_info


def ops_account(ad_ops, request, msg_template, home_url, username, new_password):
    """
    ad 账号操作，判断账号状态，重置密码或解锁账号
    """
    try:
        print("ops_account: {}".format(username))
        _status, _account = ad_ops.ad_ensure_user_by_account(username=username)
        if not _status:
            context = {'global_title': TITLE,
                       'msg': "账号[%s]在AD中不存在，请确认当前钉钉扫码账号绑定的邮箱是否和您正在使用的邮箱一致？或者该账号己被禁用！\n猜测：您的账号或邮箱是否是带有数字或其它字母区分？" % username,
                       'button_click': "window.location.href='%s'" % home_url,
                       'button_display': "返回主页"
                       }
            return render(request, msg_template, context)

        _status, account_code = ad_ops.ad_get_user_status_by_account(username)
        if _status and account_code in settings.AD_ACCOUNT_DISABLE_CODE:
            context = {'global_title': TITLE,
                       'msg': "此账号状态为己禁用，请联系HR确认账号是否正确。",
                       'button_click': "window.location.href='%s'" % home_url,
                       'button_display': "返回主页"
                       }
            return render(request, msg_template, context)
        elif not _status:
            context = {'global_title': TITLE,
                       'msg': "错误：{}".format(account_code),
                       'button_click': "window.location.href='%s'" % home_url,
                       'button_display': "返回主页"
                       }
            return render(request, msg_template, context)

        if new_password:
            reset_status, result = ad_ops.ad_reset_user_pwd_by_account(username=username, new_password=new_password)
            if reset_status:
                # 重置密码并执行一次解锁，防止重置后账号还是锁定状态。
                unlock_status, result = ad_ops.ad_unlock_user_by_account(username)
                if unlock_status:
                    context = {'global_title': TITLE,
                               'msg': "密码己修改成功，请妥善保管。你可以点击修改密码或直接关闭此页面！",
                               'button_click': "window.location.href='%s'" % home_url,
                               'button_display': "返回主页"
                               }
                    return render(request, msg_template, context)
            else:
                context = {'global_title': TITLE,
                           'msg': "密码未修改/重置成功，错误信息：{}".format(result),
                           'button_click': "window.location.href='%s'" % '/auth',
                           'button_display': "重新认证授权"
                           }
                return render(request, msg_template, context)
        else:
            unlock_status, result = ad_ops.ad_unlock_user_by_account(username)
            if unlock_status:
                context = {'global_title': TITLE,
                           'msg': "账号己解锁成功。你可以点击返回主页或直接关闭此页面！",
                           'button_click': "window.location.href='%s'" % home_url,
                           'button_display': "返回主页"
                           }
                return render(request, msg_template, context)
            else:
                context = {'global_title': TITLE,
                           'msg': "账号未能解锁，错误信息：{}".format(result),
                           'button_click': "window.location.href='%s'" % '/auth',
                           'button_display': "重新认证授权"
                           }
                return render(request, msg_template, context)
    except LDAPException as l_e:
        context = {'global_title': TITLE,
                   'msg': "账号未能解锁，错误信息：{}".format(l_e),
                   'button_click': "window.location.href='%s'" % '/auth',
                   'button_display': "重新认证授权"
                   }
        return render(request, msg_template, context)
