# -*- coding: utf-8 -*-
"""
线程安全的内存缓存实现
支持TTL（生存时间）自动过期机制
"""
import time
import threading
from typing import Any, Optional, Dict
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """缓存项数据类"""
    value: Any
    expire_at: float  # 过期时间戳
    created_at: float  # 创建时间戳
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() > self.expire_at


class MemoryCache:
    """
    线程安全的内存缓存
    
    Example:
        cache = MemoryCache()
        cache.set('key1', 'value1', ttl=3600)
        value = cache.get('key1')
        cache.delete('key1')
    """
    
    def __init__(self, cleanup_interval: int = 3600):
        """
        初始化缓存
        
        Args:
            cleanup_interval: 后台清理间隔（秒），删除过期项
        """
        self._storage: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取缓存值
        
        Args:
            key: 缓存键
            default: 键不存在或已过期时的默认值
            
        Returns:
            缓存值或默认值
        """
        with self._lock:
            self._cleanup_if_needed()
            
            if key not in self._storage:
                return default
            
            entry = self._storage[key]
            if entry.is_expired():
                del self._storage[key]
                return default
            
            return entry.value

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值（None值会被忽略）
            ttl: 生存时间（秒），默认1小时
        """
        if value is None:
            return
        
        with self._lock:
            now = time.time()
            self._storage[key] = CacheEntry(
                value=value,
                expire_at=now + ttl,
                created_at=now
            )

    def delete(self, key: str) -> bool:
        """
        删除缓存项
        
        Args:
            key: 缓存键
            
        Returns:
            是否成功删除（键存在返回True）
        """
        with self._lock:
            if key in self._storage:
                del self._storage[key]
                return True
            return False

    def has(self, key: str) -> bool:
        """
        检查键是否存在且未过期
        
        Args:
            key: 缓存键
            
        Returns:
            键是否存在
        """
        with self._lock:
            if key not in self._storage:
                return False
            
            entry = self._storage[key]
            if entry.is_expired():
                del self._storage[key]
                return False
            
            return True

    def clear(self) -> None:
        """清空所有缓存"""
        with self._lock:
            self._storage.clear()

    def size(self) -> int:
        """获取缓存项数量"""
        with self._lock:
            return len(self._storage)

    def _cleanup_if_needed(self) -> None:
        """
        检查并执行过期项清理
        
        内部方法，不需要外部调用（已通过_lock保护）
        """
        now = time.time()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        
        # 删除过期项
        expired_keys = [
            key for key, entry in self._storage.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self._storage[key]
        
        self._last_cleanup = now

    def cleanup(self) -> int:
        """
        手动清理过期项
        
        Returns:
            清理的项数
        """
        with self._lock:
            expired_keys = [
                key for key, entry in self._storage.items()
                if entry.is_expired()
            ]
            for key in expired_keys:
                del self._storage[key]
            return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self._lock:
            total = len(self._storage)
            expired = sum(1 for entry in self._storage.values() if entry.is_expired())
            return {
                'total_items': total,
                'expired_items': expired,
                'active_items': total - expired,
                'last_cleanup': self._last_cleanup
            }


# 全局内存缓存单例
_memory_cache = MemoryCache()


def get_cache() -> MemoryCache:
    """获取全局内存缓存实例"""
    return _memory_cache
