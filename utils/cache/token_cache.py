# -*- coding: utf-8 -*-
"""
Token缓存 - 专用于缓存OAuth token
"""
from typing import Optional, Dict, Any
from utils.cache.memory_cache import get_cache


class TokenCache:
    """
    OAuth Token专用缓存
    
    支持多个来源（钉钉、企业微信等）的token缓存
    
    Example:
        token_cache = TokenCache()
        token_cache.store_access_token('ding', 'token123', 7200)
        token = token_cache.get_access_token('ding')
    """
    
    def __init__(self):
        """初始化Token缓存"""
        self._cache = get_cache()
    
    def _make_key(self, source: str, key_type: str = 'access_token') -> str:
        """生成缓存键"""
        return f"token:{source}:{key_type}"
    
    def store_access_token(self, source: str, token: str, expire_in: int) -> None:
        """
        存储Access Token
        
        Args:
            source: token来源（'ding'或'wework'）
            token: token值
            expire_in: 过期时间（秒）
        """
        key = self._make_key(source, 'access_token')
        # 提前10分钟过期，避免边界问题
        ttl = max(expire_in - 600, 60)
        self._cache.set(key, token, ttl=ttl)
    
    def get_access_token(self, source: str) -> Optional[str]:
        """
        获取Access Token
        
        Args:
            source: token来源
            
        Returns:
            token值或None（不存在或已过期）
        """
        key = self._make_key(source, 'access_token')
        return self._cache.get(key)
    
    def is_token_expired(self, source: str) -> bool:
        """
        检查token是否过期
        
        Args:
            source: token来源
            
        Returns:
            token是否过期（不存在视为已过期）
        """
        return self.get_access_token(source) is None
    
    def clear_token(self, source: str) -> bool:
        """
        清除Token
        
        Args:
            source: token来源
            
        Returns:
            是否成功清除
        """
        key = self._make_key(source, 'access_token')
        return self._cache.delete(key)
    
    def clear_all_tokens(self) -> None:
        """清除所有tokens"""
        self._cache.clear()
    
    def store_user_ticket(self, source: str, user_id: str, ticket: str, expire_in: int) -> None:
        """
        存储用户Ticket（企业微信OAuth2流程）
        
        Args:
            source: 来源
            user_id: 用户ID
            ticket: user_ticket值
            expire_in: 过期时间（秒）
        """
        key = f"ticket:{source}:{user_id}"
        ttl = max(expire_in - 600, 60)
        self._cache.set(key, ticket, ttl=ttl)
    
    def get_user_ticket(self, source: str, user_id: str) -> Optional[str]:
        """获取用户Ticket"""
        key = f"ticket:{source}:{user_id}"
        return self._cache.get(key)
    
    def clear_user_ticket(self, source: str, user_id: str) -> bool:
        """清除用户Ticket"""
        key = f"ticket:{source}:{user_id}"
        return self._cache.delete(key)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return self._cache.get_stats()


# 全局token缓存单例
_token_cache = TokenCache()


def get_token_cache() -> TokenCache:
    """获取全局Token缓存实例"""
    return _token_cache
