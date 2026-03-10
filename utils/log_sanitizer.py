import re
from typing import Dict, Any

class LogSanitizer:
    """日志脱敏工具类"""
    
    # 敏感字段名称（不区分大小写）
    SENSITIVE_KEYS = {
        'password', 'pwd', 'passwd', 'secret', 'token', 'key',
        'authorization', 'auth', 'apikey', 'api_key', 'credential'
    }
    
    @classmethod
    def sanitize_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        脱敏字典中的敏感信息
        
        Args:
            data: 原始字典
            
        Returns:
            脱敏后的字典
        """
        if not isinstance(data, dict):
            return data
        
        sanitized = {}
        for key, value in data.items():
            key_lower = key.lower()
            
            # 检查是否为敏感字段
            if any(sensitive in key_lower for sensitive in cls.SENSITIVE_KEYS):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = cls.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [cls.sanitize_dict(item) if isinstance(item, dict) else item 
                                  for item in value]
            else:
                sanitized[key] = value
        
        return sanitized
    
    @classmethod
    def sanitize_mobile(cls, mobile: str) -> str:
        """
        脱敏手机号
        
        Args:
            mobile: 原始手机号
            
        Returns:
            脱敏后的手机号（保留前3后4位）
        """
        if not mobile or not isinstance(mobile, str):
            return "***"
        
        if len(mobile) < 7:
            return "***"
        
        return f"{mobile[:3]}****{mobile[-4:]}"
    
    @classmethod
    def sanitize_email(cls, email: str) -> str:
        """
        脱敏邮箱
        
        Args:
            email: 原始邮箱
            
        Returns:
            脱敏后的邮箱
        """
        if not email or '@' not in email:
            return "***@***.***"
        
        local, domain = email.split('@', 1)
        if len(local) <= 2:
            return f"**@{domain}"
        
        return f"{local[0]}***{local[-1]}@{domain}"
    
    @classmethod
    def sanitize_username(cls, username: str, show_length: int = 3) -> str:
        """
        部分脱敏用户名（用于日志）
        
        Args:
            username: 原始用户名
            show_length: 显示的前缀长度
            
        Returns:
            脱敏后的用户名
        """
        if not username:
            return "***"
        
        if len(username) <= show_length:
            return "*" * len(username)
        
        return f"{username[:show_length]}***"
    
    @classmethod
    def sanitize_user_info(cls, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        脱敏OAuth用户信息（保留必要字段，脱敏敏感字段）
        
        Args:
            user_info: OAuth用户信息字典
            
        Returns:
            脱敏后的用户信息
        """
        if not isinstance(user_info, dict):
            return {}
        
        sanitized = cls.sanitize_dict(user_info.copy())
        
        # 额外处理特定字段
        if 'mobile' in sanitized:
            sanitized['mobile'] = cls.sanitize_mobile(str(sanitized['mobile']))
        
        if 'email' in sanitized or 'orgEmail' in sanitized:
            email_key = 'email' if 'email' in sanitized else 'orgEmail'
            sanitized[email_key] = cls.sanitize_email(str(sanitized[email_key]))
        
        return sanitized
    
    @classmethod
    def sanitize_log_message(cls, message: str) -> str:
        """
        脱敏日志消息字符串中的敏感信息
        
        Args:
            message: 原始日志消息
            
        Returns:
            脱敏后的日志消息
            
        Example:
            >>> msg = "User login with password=abc123 and token=xyz"
            >>> LogSanitizer.sanitize_log_message(msg)
            'User login with password=***REDACTED*** and token=***REDACTED***'
        """
        # 匹配模式: key=value 或 key:value
        pattern = r'(password|pwd|passwd|secret|token|key|authorization|apikey|api_key|credential)\s*[=:]\s*[^\s,;)}\]]+' 
        
        def replace_sensitive(match):
            key_part = match.group(1)
            return f"{key_part}=***REDACTED***"
        
        return re.sub(pattern, replace_sensitive, message, flags=re.IGNORECASE)
    
    @classmethod
    def get_safe_error_message(cls, error: Exception, include_type: bool = True) -> str:
        """
        获取安全的异常消息（移除可能包含的敏感信息）
        
        Args:
            error: 异常对象
            include_type: 是否包含异常类型
            
        Returns:
            安全的错误消息
        """
        error_msg = str(error)
        sanitized_msg = cls.sanitize_log_message(error_msg)
        
        if include_type:
            return f"{type(error).__name__}: {sanitized_msg}"
        
        return sanitized_msg
