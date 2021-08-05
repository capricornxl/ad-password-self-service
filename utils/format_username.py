#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @FileName：     format_username.py
# @Software:      
# @Author:         Leven Xiang
# @Mail:           xiangle0109@outlook.com
# @Date：          2021/4/19 9:17

import re


def format2username(account):
    """
    格式化账号，统一输出为用户名格式
    :param account 用户账号可以是邮箱、DOMAIN\\username、username格式。
    :return: username
    """
    if account:
        mail_compile = re.compile(r'(.*)@(.*)')
        domain_compile = re.compile(r'(.*)\\(.*)')

        if re.fullmatch(mail_compile, account):
            return True, re.fullmatch(mail_compile, account).group(1)
        elif re.fullmatch(domain_compile, account):
            return True, re.fullmatch(domain_compile, account).group(2)
        else:
            return True, account.lower()
    else:
        return False, NameError("{}格式化失败，注意：account用户账号是邮箱或DOMAIN\\username或username格式！".format(account))


def get_user_is_active(user_info):
    try:
        return True, user_info.get('active') or user_info.get('status')
    except Exception as e:
        return False, 'get_user_is_active: %s' % str(e)

    except (KeyError, IndexError) as k_error:
        return False, 'get_user_is_active: %s' % str(k_error)


if __name__ == '__main__':
    user = 'jf.com\XiangLe'
    username = format2username(user)
    print(username)
