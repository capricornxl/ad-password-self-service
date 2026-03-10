# -*- coding: utf-8 -*-
"""
短信服务异常定义
"""
from enum import Enum
from typing import Optional


class SMSErrorCode(Enum):
    """短信错误码枚举"""
    
    # 配置错误 (1xxx)
    CONFIGURATION_ERROR = "SMS_CONFIG_ERROR"
    CONFIG_INVALID = "SMS_CONFIG_INVALID"           # 配置无效
    CONFIG_MISSING_REQUIRED = "SMS_CONFIG_MISSING"   # 缺少必需配置
    PROVIDER_NOT_FOUND = "SMS_PROVIDER_NOT_FOUND"
    INVALID_PROVIDER_CONFIG = "SMS_INVALID_CONFIG"
    
    # 手机号相关 (2xxx)
    INVALID_MOBILE = "SMS_INVALID_MOBILE"
    MOBILE_INVALID_FORMAT = "SMS_MOBILE_FORMAT"      # 手机号格式错误
    MOBILE_NOT_FOUND = "SMS_MOBILE_NOT_FOUND"
    MOBILE_BINDING_FAILED = "SMS_BINDING_FAILED"
    
    # 验证码相关 (3xxx)
    CODE_GENERATION_FAILED = "SMS_CODE_GEN_FAILED"
    CODE_EXPIRED = "SMS_CODE_EXPIRED"
    CODE_INVALID = "SMS_CODE_INVALID"
    CODE_NOT_FOUND = "SMS_CODE_NOT_FOUND"
    CODE_ALREADY_USED = "SMS_CODE_USED"
    
    # 发送相关 (4xxx)
    SEND_FAILED = "SMS_SEND_FAILED"
    SEND_RATE_LIMITED = "SMS_RATE_LIMITED"
    SEND_DAILY_LIMIT = "SMS_DAILY_LIMIT"
    NETWORK_ERROR = "SMS_NETWORK_ERROR"
    PROVIDER_ERROR = "SMS_PROVIDER_ERROR"
    SDK_NOT_INSTALLED = "SMS_SDK_NOT_INSTALLED"     # SDK未安装
    
    # 验证相关 (5xxx)
    VERIFY_FAILED = "SMS_VERIFY_FAILED"
    VERIFY_RATE_LIMITED = "SMS_VERIFY_RATE_LIMITED"
    TOO_MANY_ATTEMPTS = "SMS_TOO_MANY_ATTEMPTS"
    
    # 通用错误 (9xxx)
    UNKNOWN_ERROR = "SMS_UNKNOWN_ERROR"


class SMSException(Exception):
    """
    短信服务异常基类
    
    统一的短信服务异常处理
    """
    
    def __init__(
        self,
        error_code: SMSErrorCode,
        message: str,
        context: str = '',
        original_exception: Optional[Exception] = None
    ):
        """
        初始化短信异常
        
        Args:
            error_code: 错误码
            message: 错误消息
            context: 上下文信息（如：发送验证码、验证验证码）
            original_exception: 原始异常（如果有）
        """
        self.error_code = error_code
        self.message = message
        self.context = context
        self.original_exception = original_exception
        
        super().__init__(self.get_log_message())
    
    def get_log_message(self) -> str:
        """获取日志消息（详细）"""
        msg = f"[{self.error_code.value}] {self.message}"
        if self.context:
            msg += f" (Context: {self.context})"
        if self.original_exception:
            msg += f" (Original: {str(self.original_exception)})"
        return msg
    
    def get_user_message(self) -> str:
        """获取用户友好消息（简化）"""
        return ERROR_MESSAGES.get(self.error_code.value, self.message)


# 错误码对应的用户友好消息
ERROR_MESSAGES = {
    # 配置错误
    SMSErrorCode.CONFIGURATION_ERROR.value: "短信服务配置错误，请联系管理员",
    SMSErrorCode.PROVIDER_NOT_FOUND.value: "短信提供商未配置",
    SMSErrorCode.INVALID_PROVIDER_CONFIG.value: "短信提供商配置无效",
    
    # 手机号相关
    SMSErrorCode.INVALID_MOBILE.value: "手机号格式不正确",
    SMSErrorCode.MOBILE_NOT_FOUND.value: "未找到绑定的手机号，请联系管理员",
    SMSErrorCode.MOBILE_BINDING_FAILED.value: "手机号绑定失败",
    
    # 验证码相关
    SMSErrorCode.CODE_GENERATION_FAILED.value: "验证码生成失败",
    SMSErrorCode.CODE_EXPIRED.value: "验证码已过期，请重新获取",
    SMSErrorCode.CODE_INVALID.value: "验证码错误",
    SMSErrorCode.CODE_NOT_FOUND.value: "验证码不存在或已过期",
    SMSErrorCode.CODE_ALREADY_USED.value: "验证码已使用，请重新获取",
    
    # 发送相关
    SMSErrorCode.SEND_FAILED.value: "短信发送失败，请稍后重试",
    SMSErrorCode.SEND_RATE_LIMITED.value: "发送过于频繁，请稍后重试",
    SMSErrorCode.SEND_DAILY_LIMIT.value: "今日发送次数已达上限",
    SMSErrorCode.NETWORK_ERROR.value: "网络连接失败，请稍后重试",
    SMSErrorCode.PROVIDER_ERROR.value: "短信服务商错误，请联系管理员",
    
    # 验证相关
    SMSErrorCode.VERIFY_FAILED.value: "验证失败",
    SMSErrorCode.VERIFY_RATE_LIMITED.value: "验证过于频繁，请稍后重试",
    SMSErrorCode.TOO_MANY_ATTEMPTS.value: "验证次数过多，请重新获取验证码",
    
    # 通用
    SMSErrorCode.UNKNOWN_ERROR.value: "未知错误，请联系管理员",
}
