import re
from typing import Tuple

class LDAPEscape:
    """LDAP注入防护工具类"""
    
    # LDAP搜索过滤器需要转义的字符（RFC 4515）
    SEARCH_ESCAPE_MAP = {
        '\\': '\\5c',  # 反斜杠（必须第一个转义）
        '*': '\\2a',   # 星号（通配符）
        '(': '\\28',   # 左括号
        ')': '\\29',   # 右括号
        '\0': '\\00',  # NULL字符
    }
    
    # DN需要转义的字符（RFC 4514）
    DN_ESCAPE_CHARS = ',\\#+<>;"='
    
    @classmethod
    def escape_filter_value(cls, value: str) -> str:
        """
        转义LDAP搜索过滤器中的特殊字符
        
        Args:
            value: 原始值
            
        Returns:
            转义后的值
            
        Example:
            >>> LDAPEscape.escape_filter_value("admin*")
            'admin\\2a'
        """
        if not value:
            return value
        
        # 按顺序转义（反斜杠必须最先）
        for char, escaped in cls.SEARCH_ESCAPE_MAP.items():
            value = value.replace(char, escaped)
        
        return value
    
    @classmethod
    def escape_dn_value(cls, value: str) -> str:
        """
        转义DN组件中的特殊字符
        
        Args:
            value: 原始值
            
        Returns:
            转义后的值
            
        Example:
            >>> LDAPEscape.escape_dn_value("admin,user")
            'admin\\,user'
        """
        if not value:
            return value
        
        # 转义特殊字符
        result = []
        for i, char in enumerate(value):
            if char in cls.DN_ESCAPE_CHARS:
                result.append('\\')
                result.append(char)
            elif char == '\0':
                result.append('\\00')
            else:
                result.append(char)
        
        return ''.join(result)
    
    @classmethod
    def validate_username(cls, username: str) -> Tuple[bool, str]:
        """
        验证username格式（额外的安全层）
        
        Args:
            username: 用户名
            
        Returns:
            (是否合法, 错误消息)
        """
        if not username:
            return False, "用户名不能为空"
        
        # 长度限制
        if len(username) > 256:
            return False, "用户名过长"
        
        # 格式检查（根据业务需求调整）
        # 只允许字母、数字、@、.、-、_
        if not re.match(r'^[a-zA-Z0-9@._-]+$', username):
            return False, "用户名包含非法字符"
        
        # 禁止特定模式（如连续的特殊字符）
        if '..' in username or '--' in username or '__' in username:
            return False, "用户名格式不正确"
        
        return True, ""
