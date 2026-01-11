# -*- coding: utf-8 -*-
"""
错误码标准化模块
统一管理应用中所有错误码和对应的用户友好消息
"""
from enum import Enum
from typing import Dict, Optional


class ErrorCode(Enum):
    """
    应用错误码枚举
    
    命名规范：
    - CATEGORY_SPECIFIC_ERROR
    - 类别包括：FORM, AUTH, LDAP, OAUTH, SESSION, VALIDATION
    """
    
    # 表单验证错误 (1xxx)
    FORM_VALIDATION_ERROR = "FORM_VALIDATION_ERROR"
    FORM_PASSWORDS_MISMATCH = "FORM_PASSWORDS_MISMATCH"
    FORM_USERNAME_EMPTY = "FORM_USERNAME_EMPTY"
    
    # 认证相关错误 (2xxx)
    AUTH_INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    AUTH_ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    AUTH_ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    AUTH_ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"
    AUTH_PASSWORD_EXPIRED = "PASSWORD_EXPIRED"
    AUTH_ACCOUNT_EXPIRED = "ACCOUNT_EXPIRED"
    
    # LDAP操作错误 (3xxx)
    LDAP_CONNECTION_ERROR = "LDAP_CONNECTION_ERROR"
    LDAP_SEARCH_ERROR = "LDAP_SEARCH_ERROR"
    LDAP_MODIFY_ERROR = "LDAP_MODIFY_ERROR"
    LDAP_TIMEOUT_ERROR = "LDAP_TIMEOUT_ERROR"
    
    # OAuth相关错误 (4xxx)
    OAUTH_INVALID_CODE = "INVALID_CODE"
    OAUTH_GET_USER_FAILED = "OAUTH_GET_USER_FAILED"
    OAUTH_USER_INACTIVE = "OAUTH_USER_INACTIVE"
    OAUTH_NO_IDENTIFIER = "OAUTH_NO_IDENTIFIER"
    OAUTH_ERROR = "OAUTH_ERROR"
    
    # 会话相关错误 (5xxx)
    SESSION_EXPIRED = "SESSION_EXPIRED"
    SESSION_INVALID = "SESSION_INVALID"
    
    # 密码验证错误 (6xxx)
    VALIDATION_PASSWORD_TOO_SHORT = "PASSWORD_TOO_SHORT"
    VALIDATION_PASSWORD_TOO_LONG = "PASSWORD_TOO_LONG"
    VALIDATION_PASSWORD_WEAK = "PASSWORD_WEAK"
    VALIDATION_PASSWORD_FORBIDDEN = "PASSWORD_FORBIDDEN"
    VALIDATION_USERNAME_FORMAT = "USERNAME_FORMAT_ERROR"
    
    # 通用错误 (9xxx)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


# 错误码对应的用户友好消息
ERROR_MESSAGES: Dict[str, str] = {
    # 表单验证
    ErrorCode.FORM_VALIDATION_ERROR.value: "表单验证失败，请检查输入内容",
    ErrorCode.FORM_PASSWORDS_MISMATCH.value: "两次输入的密码不一致",
    ErrorCode.FORM_USERNAME_EMPTY.value: "用户名不能为空",
    
    # 认证相关
    ErrorCode.AUTH_INVALID_CREDENTIALS.value: "账号或密码不正确，请重新输入",
    ErrorCode.AUTH_ACCOUNT_LOCKED.value: "账号已被锁定，请使用OAuth扫码解锁或联系管理员",
    ErrorCode.AUTH_ACCOUNT_DISABLED.value: "此账号已被禁用，请联系HR确认账号状态",
    ErrorCode.AUTH_ACCOUNT_NOT_FOUND.value: "账号不存在，请确认账号是否正确",
    ErrorCode.AUTH_PASSWORD_EXPIRED.value: "密码已过期，请使用OAuth方式重置密码",
    ErrorCode.AUTH_ACCOUNT_EXPIRED.value: "账号已过期，请联系管理员",
    
    # LDAP操作
    ErrorCode.LDAP_CONNECTION_ERROR.value: "无法连接到AD服务器，请稍后重试或联系管理员",
    ErrorCode.LDAP_SEARCH_ERROR.value: "LDAP查询失败，请稍后重试",
    ErrorCode.LDAP_MODIFY_ERROR.value: "LDAP修改操作失败，请稍后重试",
    ErrorCode.LDAP_TIMEOUT_ERROR.value: "AD服务器响应超时，请稍后重试",
    
    # OAuth
    ErrorCode.OAUTH_INVALID_CODE.value: "授权码无效或已过期，请重新认证",
    ErrorCode.OAUTH_GET_USER_FAILED.value: "获取用户信息失败，请重新认证",
    ErrorCode.OAUTH_USER_INACTIVE.value: "用户未激活或已离职，请联系HR",
    ErrorCode.OAUTH_NO_IDENTIFIER.value: "无法从用户信息中提取账号标识，请联系管理员完善个人信息",
    ErrorCode.OAUTH_ERROR.value: "OAuth认证过程出现错误，请重新尝试",
    
    # 会话
    ErrorCode.SESSION_EXPIRED.value: "会话已过期，请重新认证",
    ErrorCode.SESSION_INVALID.value: "会话无效，请重新认证",
    
    # 密码验证
    ErrorCode.VALIDATION_PASSWORD_TOO_SHORT.value: "密码长度不足，请使用更长的密码",
    ErrorCode.VALIDATION_PASSWORD_TOO_LONG.value: "密码长度超出限制",
    ErrorCode.VALIDATION_PASSWORD_WEAK.value: "密码强度不足，请使用更复杂的密码",
    ErrorCode.VALIDATION_PASSWORD_FORBIDDEN.value: "密码包含禁用内容，请重新设置",
    ErrorCode.VALIDATION_USERNAME_FORMAT.value: "用户名格式不正确",
    
    # 通用
    ErrorCode.INTERNAL_ERROR.value: "系统内部错误，请联系管理员",
    ErrorCode.METHOD_NOT_ALLOWED.value: "不支持的请求方法",
    ErrorCode.UNKNOWN_ERROR.value: "未知错误，请联系管理员",
}


def get_error_message(error_code: str, default: Optional[str] = None) -> str:
    """
    根据错误码获取用户友好的错误消息
    
    Args:
        error_code: 错误码（字符串或ErrorCode枚举值）
        default: 如果错误码不存在时的默认消息
        
    Returns:
        错误消息字符串
        
    Example:
        >>> msg = get_error_message(ErrorCode.AUTH_INVALID_CREDENTIALS)
        >>> msg = get_error_message("INVALID_CREDENTIALS")
    """
    if isinstance(error_code, ErrorCode):
        error_code = error_code.value
    
    return ERROR_MESSAGES.get(
        error_code,
        default or f"操作失败（错误码：{error_code}）"
    )


def get_ldap_error_code(ldap_result_code: str) -> ErrorCode:
    """
    将LDAP错误代码映射到应用错误码
    
    Args:
        ldap_result_code: LDAP返回的错误代码（如 '52e', '775' 等）
        
    Returns:
        对应的ErrorCode枚举值
        
    Reference:
        https://ldapwiki.com/wiki/Common%20Active%20Directory%20Bind%20Errors
    """
    ldap_error_mapping = {
        '52e': ErrorCode.AUTH_INVALID_CREDENTIALS,  # 用户名或密码错误
        '525': ErrorCode.AUTH_ACCOUNT_NOT_FOUND,    # 账号不存在
        '533': ErrorCode.AUTH_ACCOUNT_DISABLED,     # 账号已禁用
        '532': ErrorCode.AUTH_PASSWORD_EXPIRED,     # 密码已过期
        '701': ErrorCode.AUTH_ACCOUNT_EXPIRED,      # 账号已过期
        '773': ErrorCode.AUTH_PASSWORD_EXPIRED,     # 必须修改密码
        '775': ErrorCode.AUTH_ACCOUNT_LOCKED,       # 账号被锁定
    }
    
    return ldap_error_mapping.get(
        ldap_result_code,
        ErrorCode.LDAP_CONNECTION_ERROR
    )


def format_error_response(error_code: ErrorCode, details: Optional[str] = None) -> Dict:
    """
    格式化错误响应
    
    Args:
        error_code: 错误码枚举
        details: 额外的错误详情（可选，用于日志）
        
    Returns:
        标准化的错误响应字典
        
    Example:
        >>> response = format_error_response(ErrorCode.AUTH_ACCOUNT_LOCKED, "User: john")
        >>> # Returns: {'error_code': 'ACCOUNT_LOCKED', 'message': '...', 'details': 'User: john'}
    """
    response = {
        'error_code': error_code.value,
        'message': get_error_message(error_code),
    }
    
    if details:
        response['details'] = details
    
    return response
