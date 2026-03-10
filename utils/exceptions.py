# -*- coding: utf-8 -*-
"""
统一异常处理

提供统一的异常基类和处理机制，确保所有模块使用一致的方式处理错误。

使用示例:
    # 自定义异常
    class MyException(BaseException):
        def __init__(self, code, message, context=None):
            super().__init__(code, message, context)
    
    # 抛出异常
    raise MyException(ErrorCode.SOME_ERROR, "操作失败", {"detail": "..."})
    
    # 捕获和处理
    try:
        ...
    except BaseException as e:
        user_message = e.get_user_message()
        log_message = e.get_log_message()
"""
from typing import Optional, Dict, Any
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class BaseException(Exception):
    """
    统一异常基类
    
    所有自定义异常都应继承此类，确保统一的错误处理接口。
    
    Attributes:
        code: 错误码（整数或枚举值）
        message: 错误消息
        context: 上下文信息字典
        original_exception: 原始异常（可选）
    """
    
    def __init__(
        self,
        code: Any,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        """
        初始化异常
        
        Args:
            code: 错误码
            message: 错误消息
            context: 上下文信息（可选）
            original_exception: 原始异常（可选）
        """
        self.code = code
        self.message = message
        self.context = context or {}
        self.original_exception = original_exception
        
        super().__init__(self._build_message())
    
    def _build_message(self) -> str:
        """构建完整错误消息"""
        parts = [f"[{self.code}] {self.message}"]
        if self.context:
            parts.append(f" Context: {self.context}")
        return "".join(parts)
    
    def get_user_message(self) -> str:
        """
        获取用户友好消息
        
        子类可以覆盖此方法提供更友好的消息。
        
        Returns:
            用户友好的错误消息
        """
        return self.message
    
    def get_log_message(self) -> str:
        """
        获取日志消息（包含详细信息）
        
        Returns:
            详细的日志消息
        """
        msg = f"[{self.code}] {self.message}"
        if self.context:
            msg += f" | Context: {self.context}"
        if self.original_exception:
            msg += f" | Original: {type(self.original_exception).__name__}: {self.original_exception}"
        return msg
    
    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式（用于 API 响应）
        
        Returns:
            包含错误信息的字典
        """
        result = {
            'success': False,
            'error_code': str(self.code),
            'message': self.get_user_message()
        }
        if self.context:
            result['context'] = self.context
        return result


class ConfigurationError(BaseException):
    """配置错误"""
    
    def __init__(self, message: str, config_key: str = None):
        context = {'config_key': config_key} if config_key else None
        super().__init__(5002, message, context)


class ValidationError(BaseException):
    """验证错误"""
    
    def __init__(self, message: str, field: str = None, value: Any = None):
        context = {}
        if field:
            context['field'] = field
        if value is not None:
            context['value'] = str(value)[:100]  # 限制长度
        super().__init__(4006, message, context)


class RateLimitError(BaseException):
    """限流错误"""
    
    def __init__(self, message: str, retry_after: int = None):
        context = {'retry_after': retry_after} if retry_after else None
        super().__init__(4104, message, context)
    
    def get_user_message(self) -> str:
        if 'retry_after' in self.context:
            return f"操作过于频繁，请 {self.context['retry_after']} 秒后重试"
        return "操作过于频繁，请稍后重试"


class AuthenticationError(BaseException):
    """认证错误"""
    
    def __init__(self, message: str = "认证失败", code: Any = 4203):
        super().__init__(code, message)


class AuthorizationError(BaseException):
    """授权错误"""
    
    def __init__(self, message: str = "权限不足"):
        super().__init__(4204, message)


class NotFoundError(BaseException):
    """资源不存在错误"""
    
    def __init__(self, resource_type: str, resource_id: str = None):
        message = f"{resource_type}不存在"
        context = {'resource_type': resource_type}
        if resource_id:
            context['resource_id'] = resource_id
        super().__init__(4004, message, context)


def handle_exception(e: Exception, default_message: str = "操作失败") -> Dict[str, Any]:
    """
    统一异常处理函数
    
    将任意异常转换为标准响应格式。
    
    Args:
        e: 异常实例
        default_message: 默认错误消息
        
    Returns:
        标准错误响应字典
    """
    if isinstance(e, BaseException):
        logger.error(e.get_log_message())
        return e.to_dict()
    
    # 处理非自定义异常
    logger.exception(f"未处理的异常: {type(e).__name__}: {e}")
    return {
        'success': False,
        'error_code': '5000',
        'message': default_message
    }


def log_exception(e: Exception, context: str = "") -> None:
    """
    记录异常日志
    
    Args:
        e: 异常实例
        context: 上下文描述
    """
    if isinstance(e, BaseException):
        log_msg = f"{context}: {e.get_log_message()}" if context else e.get_log_message()
        logger.error(log_msg)
    else:
        log_msg = f"{context}: {type(e).__name__}: {e}" if context else f"{type(e).__name__}: {e}"
        logger.exception(log_msg)