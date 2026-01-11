# -*- coding: utf-8 -*-
"""
统一错误码定义

错误码范围分配：
- LDAP: 1000-1999
- SMS: 2000-2999  
- OAuth: 3000-3999
- 系统: 4000-4999

使用说明：
各模块可以导入对应的错误码类，也可以从本模块导入 BaseErrorCode 进行扩展。
"""


class BaseErrorCode:
    """错误码基类"""
    
    @classmethod
    def get_message(cls, code: int) -> str:
        """获取错误码对应的消息"""
        return cls.ERROR_MESSAGES.get(code, "未知错误")


# =============================================================================
# LDAP 错误码 (1000-1999)
# =============================================================================
class LDAPErrorCode(BaseErrorCode):
    """LDAP 错误码"""
    
    # ---------- 认证相关错误 (1xxx) ----------
    INVALID_CREDENTIALS = 1001      # 用户名或密码错误
    ACCOUNT_LOCKED = 1002           # 账号锁定
    ACCOUNT_DISABLED = 1003         # 账号禁用
    PASSWORD_EXPIRED = 1004         # 密码过期
    PASSWORD_MUST_CHANGE = 1005     # 必须修改密码
    ACCOUNT_EXPIRED = 1006          # 账号过期
    ACCOUNT_NOT_FOUND = 1007        # 账号不存在
    
    # ---------- 密码策略错误 (11xx) ----------
    PASSWORD_POLICY_VIOLATION = 1101    # 密码策略违规
    PASSWORD_TOO_SHORT = 1102           # 密码过短
    PASSWORD_TOO_LONG = 1103            # 密码过长
    PASSWORD_TOO_WEAK = 1104            # 密码过弱
    PASSWORD_IN_HISTORY = 1105          # 密码在历史记录中
    PASSWORD_SAME_AS_OLD = 1106         # 新旧密码相同
    
    # ---------- 操作错误 (12xx) ----------
    CONNECTION_FAILED = 1201            # 连接失败
    BIND_FAILED = 1202                  # 绑定失败
    SEARCH_FAILED = 1203                # 搜索失败
    MODIFY_FAILED = 1204                # 修改失败
    INSUFFICIENT_PERMISSION = 1205      # 权限不足
    OPERATION_NOT_SUPPORTED = 1206      # 操作不支持
    TIMEOUT = 1207                      # 超时
    SSL_ERROR = 1208                    # SSL错误
    
    # ---------- 数据错误 (13xx) ----------
    INVALID_DN = 1301                   # 无效的DN
    ATTRIBUTE_NOT_FOUND = 1302          # 属性不存在
    INVALID_ATTRIBUTE_VALUE = 1303      # 无效的属性值
    ENTRY_NOT_FOUND = 1304              # 条目不存在
    ENTRY_ALREADY_EXISTS = 1305         # 条目已存在
    INVALID_PARAMETER = 1306            # 无效的参数
    
    # ---------- 系统错误 (14xx) ----------
    UNKNOWN_ERROR = 1401                # 未知错误
    CONFIGURATION_ERROR = 1402          # 配置错误
    INTERNAL_ERROR = 1403               # 内部错误
    
    # 错误码到消息的映射
    ERROR_MESSAGES = {
        # 认证相关
        INVALID_CREDENTIALS: "用户名或密码不正确",
        ACCOUNT_LOCKED: "账号已锁定",
        ACCOUNT_DISABLED: "账号已禁用",
        PASSWORD_EXPIRED: "密码已过期",
        PASSWORD_MUST_CHANGE: "用户登录前必须修改密码",
        ACCOUNT_EXPIRED: "账号已过期",
        ACCOUNT_NOT_FOUND: "账号不存在",
        
        # 密码策略
        PASSWORD_POLICY_VIOLATION: "密码不符合策略要求",
        PASSWORD_TOO_SHORT: "密码过短",
        PASSWORD_TOO_LONG: "密码过长",
        PASSWORD_TOO_WEAK: "密码过弱",
        PASSWORD_IN_HISTORY: "密码不能与历史密码相同",
        PASSWORD_SAME_AS_OLD: "新密码不能与旧密码相同",
        
        # 操作错误
        CONNECTION_FAILED: "LDAP连接失败",
        BIND_FAILED: "LDAP绑定失败",
        SEARCH_FAILED: "LDAP搜索失败",
        MODIFY_FAILED: "LDAP修改失败",
        INSUFFICIENT_PERMISSION: "权限不足",
        OPERATION_NOT_SUPPORTED: "操作不支持",
        TIMEOUT: "操作超时",
        SSL_ERROR: "SSL连接错误",
        
        # 数据错误
        INVALID_DN: "无效的DN",
        ATTRIBUTE_NOT_FOUND: "属性不存在",
        INVALID_ATTRIBUTE_VALUE: "无效的属性值",
        ENTRY_NOT_FOUND: "条目不存在",
        ENTRY_ALREADY_EXISTS: "条目已存在",
        INVALID_PARAMETER: "无效的参数",
        
        # 系统错误
        UNKNOWN_ERROR: "未知错误",
        CONFIGURATION_ERROR: "配置错误",
        INTERNAL_ERROR: "内部错误"
    }


# =============================================================================
# SMS 错误码 (2000-2999)
# =============================================================================
class SMSErrorCode(BaseErrorCode):
    """SMS 错误码"""
    
    # ---------- 配置错误 (2xxx) ----------
    CONFIGURATION_ERROR = 2001
    PROVIDER_NOT_FOUND = 2002
    INVALID_PROVIDER_CONFIG = 2003
    
    # ---------- 手机号相关 (21xx) ----------
    INVALID_MOBILE = 2101
    MOBILE_NOT_FOUND = 2102
    MOBILE_BINDING_FAILED = 2103
    
    # ---------- 验证码相关 (22xx) ----------
    CODE_GENERATION_FAILED = 2201
    CODE_EXPIRED = 2202
    CODE_INVALID = 2203
    CODE_NOT_FOUND = 2204
    CODE_ALREADY_USED = 2205
    
    # ---------- 发送相关 (23xx) ----------
    SEND_FAILED = 2301
    SEND_RATE_LIMITED = 2302
    SEND_DAILY_LIMIT = 2303
    NETWORK_ERROR = 2304
    PROVIDER_ERROR = 2305
    
    # ---------- 验证相关 (24xx) ----------
    VERIFY_FAILED = 2401
    VERIFY_RATE_LIMITED = 2402
    TOO_MANY_ATTEMPTS = 2403
    
    # ---------- 通用错误 (29xx) ----------
    UNKNOWN_ERROR = 2901
    
    # 错误码到消息的映射
    ERROR_MESSAGES = {
        # 配置错误
        CONFIGURATION_ERROR: "短信服务配置错误，请联系管理员",
        PROVIDER_NOT_FOUND: "短信提供商未配置",
        INVALID_PROVIDER_CONFIG: "短信提供商配置无效",
        
        # 手机号相关
        INVALID_MOBILE: "手机号格式不正确",
        MOBILE_NOT_FOUND: "未找到绑定的手机号，请联系管理员",
        MOBILE_BINDING_FAILED: "手机号绑定失败",
        
        # 验证码相关
        CODE_GENERATION_FAILED: "验证码生成失败",
        CODE_EXPIRED: "验证码已过期，请重新获取",
        CODE_INVALID: "验证码错误",
        CODE_NOT_FOUND: "验证码不存在或已过期",
        CODE_ALREADY_USED: "验证码已使用",
        
        # 发送相关
        SEND_FAILED: "短信发送失败",
        SEND_RATE_LIMITED: "发送频率过快，请稍后再试",
        SEND_DAILY_LIMIT: "今日发送次数已达上限",
        NETWORK_ERROR: "网络错误，请稍后重试",
        PROVIDER_ERROR: "短信服务商错误",
        
        # 验证相关
        VERIFY_FAILED: "验证失败",
        VERIFY_RATE_LIMITED: "验证频率过快",
        TOO_MANY_ATTEMPTS: "验证尝试次数过多",
        
        # 通用错误
        UNKNOWN_ERROR: "短信服务未知错误"
    }


# =============================================================================
# OAuth 错误码 (3000-3999)
# =============================================================================
class OAuthErrorCode(BaseErrorCode):
    """OAuth 错误码"""
    
    # ---------- 配置错误 (3xxx) ----------
    CONFIGURATION_ERROR = 3001
    PROVIDER_NOT_FOUND = 3002
    INVALID_PROVIDER_CONFIG = 3003
    
    # ---------- 授权错误 (31xx) ----------
    AUTHORIZATION_FAILED = 3101
    INVALID_CODE = 3102
    CODE_EXPIRED = 3103
    ACCESS_DENIED = 3104
    
    # ---------- 用户信息错误 (32xx) ----------
    USER_INFO_FAILED = 3201
    USER_ID_NOT_FOUND = 3202
    USER_NOT_IN_ENTERPRISE = 3203
    
    # ---------- Token 错误 (33xx) ----------
    TOKEN_FAILED = 3301
    TOKEN_EXPIRED = 3302
    TOKEN_INVALID = 3303
    
    # ---------- 通用错误 (39xx) ----------
    API_ERROR = 3901
    NETWORK_ERROR = 3902
    UNKNOWN_ERROR = 3903
    
    # 错误码到消息的映射
    ERROR_MESSAGES = {
        # 配置错误
        CONFIGURATION_ERROR: "OAuth配置错误",
        PROVIDER_NOT_FOUND: "OAuth提供商未配置",
        INVALID_PROVIDER_CONFIG: "OAuth提供商配置无效",
        
        # 授权错误
        AUTHORIZATION_FAILED: "授权失败",
        INVALID_CODE: "授权码无效",
        CODE_EXPIRED: "授权码已过期",
        ACCESS_DENIED: "访问被拒绝",
        
        # 用户信息错误
        USER_INFO_FAILED: "获取用户信息失败",
        USER_ID_NOT_FOUND: "用户ID不存在",
        USER_NOT_IN_ENTERPRISE: "用户未加入企业",
        
        # Token 错误
        TOKEN_FAILED: "Token获取失败",
        TOKEN_EXPIRED: "Token已过期",
        TOKEN_INVALID: "Token无效",
        
        # 通用错误
        API_ERROR: "API调用错误",
        NETWORK_ERROR: "网络错误",
        UNKNOWN_ERROR: "OAuth未知错误"
    }


# =============================================================================
# 系统错误码 (4000-4999)
# =============================================================================
class SystemErrorCode(BaseErrorCode):
    """系统错误码"""
    
    # ---------- 通用错误 (4xxx) ----------
    UNKNOWN_ERROR = 4001
    INTERNAL_ERROR = 4002
    CONFIGURATION_ERROR = 4003
    FEATURE_DISABLED = 4004
    
    # ---------- 请求错误 (41xx) ----------
    INVALID_REQUEST = 4101
    INVALID_PARAMETER = 4102
    MISSING_PARAMETER = 4103
    RATE_LIMITED = 4104
    
    # ---------- 会话错误 (42xx) ----------
    SESSION_EXPIRED = 4201
    SESSION_INVALID = 4202
    UNAUTHORIZED = 4203
    FORBIDDEN = 4204
    
    # 错误码到消息的映射
    ERROR_MESSAGES = {
        # 通用错误
        UNKNOWN_ERROR: "系统未知错误",
        INTERNAL_ERROR: "系统内部错误",
        CONFIGURATION_ERROR: "系统配置错误",
        FEATURE_DISABLED: "功能已禁用",
        
        # 请求错误
        INVALID_REQUEST: "无效的请求",
        INVALID_PARAMETER: "无效的参数",
        MISSING_PARAMETER: "缺少必要参数",
        RATE_LIMITED: "请求频率过快",
        
        # 会话错误
        SESSION_EXPIRED: "会话已过期",
        SESSION_INVALID: "会话无效",
        UNAUTHORIZED: "未授权访问",
        FORBIDDEN: "禁止访问"
    }