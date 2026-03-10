# -*- coding: utf-8 -*-
"""
OAuth基础提供商抽象类
"""
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any


class BaseOAuthProvider(ABC):
    """
    OAuth提供商基础抽象类
    
    所有OAuth提供商（钉钉、企业微信等）都应继承此类
    """
    
    def __init__(self):
        """初始化提供商"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """提供商名称（如：钉钉、企业微信）"""
        pass
    
    @property
    @abstractmethod
    def provider_type(self) -> str:
        """提供商类型（如：ding、wework）"""
        pass
    
    @property
    @abstractmethod
    def corp_id(self) -> str:
        """企业ID"""
        pass
    
    @property
    @abstractmethod
    def app_id(self) -> str:
        """应用ID"""
        pass
    
    @property
    def agent_id(self) -> Optional[str]:
        """应用代理ID（可选）"""
        return None
    
    @abstractmethod
    def get_user_detail(self, code: str, home_url: str) -> Tuple[bool, Any, Optional[Dict[str, Any]]]:
        """
        通过授权码获取用户详情
        
        Args:
            code: OAuth授权码
            home_url: 主页URL
            
        Returns:
            (成功状态, 用户ID, 用户信息字典)
            
            失败时返回: (False, 错误上下文, 错误信息)
            成功时返回: (True, 用户ID, 用户信息)
        """
        pass
    
    @abstractmethod
    def get_user_id_by_code(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        通过授权码获取用户ID
        
        Args:
            code: OAuth授权码
            
        Returns:
            (成功状态, 用户ID)
        """
        pass
    
    @abstractmethod
    def get_user_detail_by_user_id(self, user_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        通过用户ID获取用户详情
        
        Args:
            user_id: 用户ID
            
        Returns:
            (成功状态, 用户信息)
        """
        pass
    
    def get_auth_config(self, home_url: str, redirect_url: str) -> Dict[str, Any]:
        """
        获取前端OAuth授权配置（可被子类覆盖）
        
        Args:
            home_url: 主页URL
            redirect_url: 回调URL
            
        Returns:
            前端授权配置字典
        """
        return {
            'provider_type': self.provider_type,
            'provider_name': self.provider_name,
            'corp_id': self.corp_id,
            'app_id': self.app_id,
            'agent_id': self.agent_id,
            'redirect_url': redirect_url,
        }
