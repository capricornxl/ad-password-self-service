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
            return re.fullmatch(mail_compile, account).group(1)
        elif re.fullmatch(domain_compile, account):
            return re.fullmatch(domain_compile, account).group(2)
        else:
            return account
    else:
        raise NameError("输入的账号不能为空..")


if __name__ == '__main__':
    user = 'aaa\jf.com'
    username = format2username(user)
    print(username)
