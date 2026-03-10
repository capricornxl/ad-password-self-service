# -*- coding: utf-8 -*-
"""
统一的LDAP错误码和异常定义
将AD和OpenLDAP的不同错误映射到统一的错误码体系
"""


class LDAPErrorCode:
    """统一的LDAP错误码"""
    
    # ========== 认证相关错误 (1xxx) ==========
    INVALID_CREDENTIALS = 1001      # 用户名或密码错误
    ACCOUNT_LOCKED = 1002           # 账号锁定
    ACCOUNT_DISABLED = 1003         # 账号禁用
    PASSWORD_EXPIRED = 1004         # 密码过期
    PASSWORD_MUST_CHANGE = 1005     # 必须修改密码
    ACCOUNT_EXPIRED = 1006          # 账号过期
    ACCOUNT_NOT_FOUND = 1007        # 账号不存在
    
    # ========== 密码策略错误 (2xxx) ==========
    PASSWORD_POLICY_VIOLATION = 2001    # 密码策略违规
    PASSWORD_TOO_SHORT = 2002           # 密码过短
    PASSWORD_TOO_LONG = 2003            # 密码过长
    PASSWORD_TOO_WEAK = 2004            # 密码过弱
    PASSWORD_IN_HISTORY = 2005          # 密码在历史记录中
    PASSWORD_SAME_AS_OLD = 2006         # 新旧密码相同
    
    # ========== 操作错误 (3xxx) ==========
    CONNECTION_FAILED = 3001            # 连接失败
    BIND_FAILED = 3002                  # 绑定失败
    SEARCH_FAILED = 3003                # 搜索失败
    MODIFY_FAILED = 3004                # 修改失败
    INSUFFICIENT_PERMISSION = 3005      # 权限不足
    OPERATION_NOT_SUPPORTED = 3006      # 操作不支持
    TIMEOUT = 3007                      # 超时
    SSL_ERROR = 3008                    # SSL错误
    
    # ========== 数据错误 (4xxx) ==========
    INVALID_DN = 4001                   # 无效的DN
    ATTRIBUTE_NOT_FOUND = 4002          # 属性不存在
    INVALID_ATTRIBUTE_VALUE = 4003      # 无效的属性值
    ENTRY_NOT_FOUND = 4004              # 条目不存在
    ENTRY_ALREADY_EXISTS = 4005         # 条目已存在
    INVALID_PARAMETER = 4006            # 无效的参数
    
    # ========== 系统错误 (5xxx) ==========
    UNKNOWN_ERROR = 5001                # 未知错误
    CONFIGURATION_ERROR = 5002          # 配置错误
    INTERNAL_ERROR = 5003               # 内部错误
    
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


class LDAPException(Exception):
    """统一的LDAP异常"""
    
    def __init__(self, code: int, message: str = None, ldap_type: str = None, 
                 original_error=None, details: dict = None):
        """
        初始化LDAP异常
        
        Args:
            code: 错误码 (LDAPErrorCode)
            message: 错误消息 (如果为None则使用默认消息)
            ldap_type: LDAP类型 ('ad' 或 'openldap')
            original_error: 原始异常对象
            details: 额外的错误详情
        """
        self.code = code
        self.ldap_type = ldap_type or 'unknown'
        self.original_error = original_error
        self.details = details or {}
        
        # 如果没有提供消息,使用默认消息
        if message is None:
            message = LDAPErrorCode.ERROR_MESSAGES.get(code, "未知错误")
        
        self.message = message
        
        # 构造完整的错误消息
        error_msg = f"[{self.ldap_type.upper()}] {self.message} (错误码: {self.code})"
        if self.details:
            error_msg += f" | 详情: {self.details}"
        
        super().__init__(error_msg)
    
    def __str__(self):
        return self.message
    
    def __repr__(self):
        return f"LDAPException(code={self.code}, message='{self.message}', ldap_type='{self.ldap_type}')"
    
    def get_user_message(self) -> str:
        """获取用户友好的错误消息"""
        return self.message
    
    def get_log_message(self) -> str:
        """获取详细的日志消息"""
        log_msg = f"[{self.ldap_type.upper()}] 错误码: {self.code}, 消息: {self.message}"
        if self.details:
            log_msg += f", 详情: {self.details}"
        if self.original_error:
            log_msg += f", 原始错误: {str(self.original_error)}"
        return log_msg
