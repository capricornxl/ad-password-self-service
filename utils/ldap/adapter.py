# -*- coding: utf-8 -*-
"""
LDAP适配器抽象基类
定义所有LDAP操作的统一接口
"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Optional
from .errors import LDAPException


class LDAPAdapter(ABC):
    """LDAP操作抽象基类"""
    
    def __init__(self):
        """初始化适配器"""
        self.conn = None
        self.server = None
        self.ldap_type = 'unknown'
    
    # ========== 连接管理 ==========
    
    @abstractmethod
    def connect(self) -> Tuple[bool, str]:
        """
        建立LDAP连接
        
        Returns:
            (是否成功, 消息)
            
        Raises:
            LDAPException: 连接失败时抛出
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """断开LDAP连接"""
        pass
    
    # ========== 认证相关 ==========
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """
        验证用户凭据
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            (是否成功, 消息)
            
        Raises:
            LDAPException: 认证失败时抛出,错误码表示失败原因
        """
        pass
    
    # ========== 密码管理 ==========
    
    @abstractmethod
    def reset_password(self, username: str, new_password: str, 
                      old_password: str = None) -> Tuple[bool, str]:
        """
        重置用户密码
        
        Args:
            username: 用户名
            new_password: 新密码
            old_password: 旧密码 (用户自己修改时需要)
            
        Returns:
            (是否成功, 消息)
            
        Raises:
            LDAPException: 重置失败时抛出
        """
        pass
    
    @abstractmethod
    def change_password(self, username: str, old_password: str, 
                       new_password: str) -> Tuple[bool, str]:
        """
        用户修改自己的密码 (需要提供旧密码)
        
        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            (是否成功, 消息)
            
        Raises:
            LDAPException: 修改失败时抛出
        """
        pass
    
    # ========== 账号管理 ==========
    
    @abstractmethod
    def unlock_account(self, username: str) -> Tuple[bool, str]:
        """
        解锁账号
        
        Args:
            username: 用户名
            
        Returns:
            (是否成功, 消息)
            
        Raises:
            LDAPException: 解锁失败时抛出
        """
        pass
    
    @abstractmethod
    def is_account_locked(self, username: str) -> Tuple[bool, bool]:
        """
        检查账号是否锁定
        
        Args:
            username: 用户名
            
        Returns:
            (查询是否成功, 是否锁定)
            
        Raises:
            LDAPException: 查询失败时抛出
        """
        pass
    
    @abstractmethod
    def is_account_disabled(self, username: str) -> Tuple[bool, bool]:
        """
        检查账号是否禁用
        
        Args:
            username: 用户名
            
        Returns:
            (查询是否成功, 是否禁用)
            
        Raises:
            LDAPException: 查询失败时抛出
        """
        pass
    
    @abstractmethod
    def get_account_status(self, username: str) -> Tuple[bool, Dict]:
        """
        获取账号状态信息
        
        Args:
            username: 用户名
            
        Returns:
            (查询是否成功, 状态信息字典)
            状态信息包括:
            {
                'locked': bool,      # 是否锁定
                'disabled': bool,    # 是否禁用
                'expired': bool,     # 是否过期
                'password_expired': bool,  # 密码是否过期
                'details': dict      # 其他详细信息
            }
            
        Raises:
            LDAPException: 查询失败时抛出
        """
        pass
    
    # ========== 用户信息查询 ==========
    
    @abstractmethod
    def search_user(self, username: str, attributes: List[str] = None) -> Tuple[bool, Dict]:
        """
        搜索用户信息
        
        Args:
            username: 用户名
            attributes: 需要返回的属性列表 (None表示返回所有)
            
        Returns:
            (是否成功, 用户信息字典)
            
        Raises:
            LDAPException: 搜索失败时抛出
        """
        pass
    
    @abstractmethod
    def get_user_dn(self, username: str) -> Tuple[bool, str]:
        """
        获取用户的DN (Distinguished Name)
        
        Args:
            username: 用户名
            
        Returns:
            (是否成功, DN字符串)
            
        Raises:
            LDAPException: 查询失败时抛出
        """
        pass
    
    # ========== 组成员管理 ==========
    
    @abstractmethod
    def get_user_groups(self, username: str) -> Tuple[bool, List[str]]:
        """
        获取用户所属的组DN列表
        
        Args:
            username: 用户名
            
        Returns:
            (是否成功, 组DN列表)
            例如:
            AD: ['CN=Domain Admins,CN=Users,DC=company,DC=com']
            OpenLDAP: ['cn=admins,ou=people,dc=company,dc=com']
            
        Raises:
            LDAPException: 查询失败时抛出
        """
        pass
    
    @abstractmethod
    def extract_group_name(self, group_dn: str) -> str:
        """
        从组DN中提取组名
        
        Args:
            group_dn: 组的完整DN
            
        Returns:
            组名 (CN或cn属性的值)
            
        Examples:
            'CN=Domain Admins,CN=Users,DC=company,DC=com' -> 'Domain Admins'
            'cn=admins,ou=groups,dc=company,dc=com' -> 'admins'
        """
        pass
    
    # ========== 辅助方法 ==========
    
    def get_ldap_type(self) -> str:
        """获取LDAP类型"""
        return self.ldap_type
    
    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self.conn is not None and self.conn.bound
    
    def __enter__(self):
        """上下文管理器进入"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.disconnect()
