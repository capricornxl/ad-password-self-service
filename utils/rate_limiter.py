# -*- coding: utf-8 -*-
"""
防暴力破解限流器 - 基于Django Cache（无需Redis）
支持多种后端：Database / Memory / FileSystem
"""
from typing import Tuple, Optional
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from utils.config import get_config
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    轻量级限流器 - 基于Django Cache（支持多种后端）
    
    支持的缓存后端：
    1. Database Cache（推荐，支持分布式）
    2. Memory Cache（最快，单机）
    3. File-based Cache（持久化，单机）
    
    Example:
        limiter = RateLimiter()
        
        # 检查是否超限
        allowed, remaining, wait_seconds = limiter.check_rate_limit(
            identifier='user:john',
            max_attempts=5,
            window_seconds=300
        )
        
        if not allowed:
            return f"请在 {wait_seconds} 秒后重试"
        
        # 业务逻辑...
        
        # 成功后重置计数器
        if success:
            limiter.reset(identifier)
    """
    
    def __init__(self):
        """初始化限流器"""
        self.config = get_config()
        # 从配置读取默认值
        self.default_max_attempts = self.config.get('security.rate_limiting.default_max_attempts', 5)
        self.default_window_seconds = self.config.get('security.rate_limiting.default_window_seconds', 300)
        self.enabled = self.config.get('security.rate_limiting.enabled', True)
        
        if not self.enabled:
            logger.warning("限流功能已禁用（security.rate_limiting.enabled=false）")
    
    def check_rate_limit(
        self,
        identifier: str,
        max_attempts: Optional[int] = None,
        window_seconds: Optional[int] = None
    ) -> Tuple[bool, int, int]:
        """
        检查是否超过限流阈值
        
        Args:
            identifier: 限流标识（如：'ip:192.168.1.1' 或 'user:john'）
            max_attempts: 时间窗口内最大尝试次数（None则使用默认值）
            window_seconds: 时间窗口（秒）（None则使用默认值）
            
        Returns:
            Tuple[是否允许, 剩余尝试次数, 等待秒数]
            
        Example:
            allowed, remaining, wait = limiter.check_rate_limit('ip:192.168.1.1', 10, 600)
            if not allowed:
                return f"请等待 {wait} 秒后重试，剩余尝试次数: {remaining}"
        """
        # 如果禁用限流，永远返回允许
        if not self.enabled:
            return True, 999, 0
        
        max_attempts = max_attempts or self.default_max_attempts
        window_seconds = window_seconds or self.default_window_seconds
        
        cache_key = f"rate_limit:{identifier}"
        
        # 获取当前计数数据
        limit_data = cache.get(cache_key)
        
        if limit_data is None:
            # 首次访问，初始化计数器
            limit_data = {
                'count': 1,
                'first_attempt_time': timezone.now().timestamp(),
                'window_seconds': window_seconds
            }
            cache.set(cache_key, limit_data, timeout=window_seconds)
            return True, max_attempts - 1, 0
        
        # 检查时间窗口是否过期
        current_time = timezone.now().timestamp()
        first_attempt_time = limit_data['first_attempt_time']
        elapsed = current_time - first_attempt_time
        
        if elapsed > window_seconds:
            # 时间窗口已过期，重置计数器
            limit_data = {
                'count': 1,
                'first_attempt_time': current_time,
                'window_seconds': window_seconds
            }
            cache.set(cache_key, limit_data, timeout=window_seconds)
            return True, max_attempts - 1, 0
        
        # 检查是否超过限制
        current_count = limit_data['count']
        
        if current_count >= max_attempts:
            # 超过限制，计算需要等待的时间
            wait_seconds = int(window_seconds - elapsed)
            logger.warning(f"限流触发: {identifier}, 已尝试 {current_count} 次，需等待 {wait_seconds} 秒")
            return False, 0, wait_seconds
        
        # 未超过限制，递增计数器
        limit_data['count'] += 1
        cache.set(cache_key, limit_data, timeout=window_seconds)
        
        remaining = max_attempts - limit_data['count']
        return True, remaining, 0
    
    def reset(self, identifier: str) -> bool:
        """
        重置限流计数器（成功操作后调用）
        
        Args:
            identifier: 限流标识
            
        Returns:
            是否成功重置
        """
        cache_key = f"rate_limit:{identifier}"
        cache.delete(cache_key)
        logger.debug(f"限流计数器已重置: {identifier}")
        return True
    
    def get_current_status(self, identifier: str) -> dict:
        """
        获取当前限流状态（用于调试）
        
        Args:
            identifier: 限流标识
            
        Returns:
            状态字典: {count, remaining, wait_seconds, first_attempt_time}
        """
        cache_key = f"rate_limit:{identifier}"
        limit_data = cache.get(cache_key)
        
        if limit_data is None:
            return {
                'count': 0,
                'remaining': self.default_max_attempts,
                'wait_seconds': 0,
                'first_attempt_time': None,
                'status': 'clean'
            }
        
        current_time = timezone.now().timestamp()
        first_attempt_time = limit_data['first_attempt_time']
        elapsed = current_time - first_attempt_time
        window_seconds = limit_data.get('window_seconds', self.default_window_seconds)
        
        wait_seconds = max(0, int(window_seconds - elapsed))
        count = limit_data['count']
        remaining = max(0, self.default_max_attempts - count)
        
        return {
            'count': count,
            'remaining': remaining,
            'wait_seconds': wait_seconds,
            'first_attempt_time': first_attempt_time,
            'status': 'limited' if count >= self.default_max_attempts else 'active'
        }
    
    def increment(
        self,
        identifier: str,
        max_attempts: Optional[int] = None,
        window_seconds: Optional[int] = None
    ) -> Tuple[bool, int]:
        """
        递增计数器（不检查限制，仅用于记录）
        
        Args:
            identifier: 限流标识
            max_attempts: 最大尝试次数
            window_seconds: 时间窗口
            
        Returns:
            Tuple[是否超限, 当前计数]
        """
        if not self.enabled:
            return False, 0
        
        max_attempts = max_attempts or self.default_max_attempts
        window_seconds = window_seconds or self.default_window_seconds
        
        cache_key = f"rate_limit:{identifier}"
        limit_data = cache.get(cache_key)
        
        if limit_data is None:
            limit_data = {
                'count': 1,
                'first_attempt_time': timezone.now().timestamp(),
                'window_seconds': window_seconds
            }
        else:
            limit_data['count'] += 1
        
        cache.set(cache_key, limit_data, timeout=window_seconds)
        
        is_limited = limit_data['count'] >= max_attempts
        return is_limited, limit_data['count']
    
    def get_lockout_info(self, identifier: str) -> Optional[dict]:
        """
        获取锁定信息（用于前端显示）
        
        Args:
            identifier: 限流标识
            
        Returns:
            锁定信息字典或None（未锁定）
        """
        status = self.get_current_status(identifier)
        
        if status['status'] == 'limited':
            return {
                'locked': True,
                'attempts': status['count'],
                'wait_seconds': status['wait_seconds'],
                'wait_minutes': status['wait_seconds'] // 60,
                'unlock_time': timezone.now() + timedelta(seconds=status['wait_seconds'])
            }
        
        return None


# 全局单例
_rate_limiter = None


def get_rate_limiter() -> RateLimiter:
    """获取全局限流器实例"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


# 便捷函数
def check_rate_limit(identifier: str, max_attempts: int = 5, 
                     window_seconds: int = 300) -> Tuple[bool, int, int]:
    """便捷函数：检查限流"""
    limiter = get_rate_limiter()
    return limiter.check_rate_limit(identifier, max_attempts, window_seconds)


def reset_rate_limit(identifier: str) -> bool:
    """便捷函数：重置限流"""
    limiter = get_rate_limiter()
    return limiter.reset(identifier)
