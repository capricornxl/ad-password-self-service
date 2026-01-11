#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @FileName：     format_username.py
# @Software:      
# @Author:         Leven Xiang
# @Mail:           xiangle0109@outlook.com
# @Date：          2021/4/19 9:17

import re
from typing import Tuple, Dict, Any, List
from utils.logger_factory import get_logger
from utils.config import get_config

logger = get_logger(__name__)


def get_user_identifier(user_info: Dict[str, Any], provider_type: str) -> Tuple[bool, str]:
    """
    从OAuth用户信息中提取用户标识（用于匹配AD账号）
    
    支持可配置的字段映射，按优先级依次尝试提取
    
    Args:
        user_info: OAuth提供商返回的用户信息字典
        provider_type: OAuth提供商类型，如 'ding' 或 'wework'
        
    Returns:
        (成功状态, 用户标识字符串或错误消息)
        
    Example:
        >>> user_info = {'email': 'user@company.com', 'mobile': '13800138000'}
        >>> status, identifier = get_user_identifier(user_info, 'wework')
        >>> # Returns: (True, 'user@company.com')
    """
    config = get_config()
    
    # 从配置获取字段映射
    mapping_key = f'oauth.user_identifier_mapping.{provider_type}'
    field_mapping = config.get_dict(mapping_key, {})
    
    if not field_mapping:
        # 降级到默认配置（兼容旧版）
        logger.warning(f"未找到 {provider_type} 的字段映射配置，使用默认映射")
        primary_field = 'email'
        fallback_fields = ['biz_mail', 'mobile']
    else:
        primary_field = field_mapping.get('primary', 'email')
        fallback_fields = field_mapping.get('fallback', [])
    
    # 按优先级尝试提取字段
    all_fields = [primary_field] + fallback_fields
    
    for field_name in all_fields:
        field_value = user_info.get(field_name)
        if field_value not in ['', None]:
            logger.debug(f"成功从字段 '{field_name}' 提取用户标识: {field_value}")
            return True, field_value
    
    # 所有字段都为空
    tried_fields = ', '.join(all_fields)
    error_msg = f"未能从用户信息中提取标识，已尝试字段: {tried_fields}。请联系管理员完善个人信息！"
    logger.warning(f"用户标识提取失败，用户信息: {user_info}, 尝试的字段: {tried_fields}")
    return False, error_msg


def get_email_from_userinfo(user_info: Dict[str, Any]) -> Tuple[bool, str]:
    """
    从用户信息中提取邮箱（兼容旧版函数，建议使用 get_user_identifier）
    
    Args:
        user_info: 用户信息字典
        
    Returns:
        (成功状态, 邮箱或错误消息)
    """
    if user_info.get('email') not in ['', None]:
        return True, user_info.get('email')
    elif user_info.get('biz_mail') not in ['', None]:
        return True, user_info.get('biz_mail')
    else:
        return False, "当前用户的邮箱或企业邮箱均没配置，请先完善个人信息！"


def format2username(account):
    """
    格式化账号，统一输出为用户名格式
    :param account 用户账号可以是邮箱、DOMAIN\\username、username格式。
    :return: username
    """

    if account is None:
        return False, NameError(
            "传入的用户账号为空！".format(account))
    try:
        mail_compile = re.compile(r'(.*)@(.*)')
        domain_compile = re.compile(r'(.*)\\(.*)')

        if re.fullmatch(mail_compile, account):
            return True, re.fullmatch(mail_compile, account).group(1)
        elif re.fullmatch(domain_compile, account):
            return True, re.fullmatch(domain_compile, account).group(2)
        else:
            return True, account.lower()
    except Exception as e:
        return False, NameError("格式化失败，注意：account用户账号是邮箱或DOMAIN\\username或username格式，错误信息[{}]".format(account, e))


def get_user_is_active(user_info):
    try:
        return True, user_info.get('active') or user_info.get('status')
    except Exception as e:
        return False, 'get_user_is_active: %s' % str(e)

    except (KeyError, IndexError) as k_error:
        return False, 'get_user_is_active: %s' % str(k_error)

