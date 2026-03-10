# -*- coding: utf-8 -*-
"""
内存存储 - 用于OAuth token缓存

说明：
    - 支持TTL自动过期
    - 适用于钉钉/企业微信SDK的token缓存
    - 使用全局单例模式，确保多个提供商共享token缓存
"""
from __future__ import absolute_import, unicode_literals

import time
import threading

from utils.storage import BaseStorage


class MemoryStorage(BaseStorage):
    """
    线程安全的内存存储
    
    用于OAuth token缓存，支持TTL自动过期
    """

    def __init__(self):
        """初始化存储"""
        self._data = {}  # 存储格式: {key: (value, expire_timestamp)}
        self._lock = threading.RLock()  # 线程锁，保证线程安全

    def get(self, key, default=None):
        """
        获取缓存值
        
        Args:
            key: 缓存键
            default: 默认值
            
        Returns:
            缓存值或默认值（如果不存在或已过期）
        """
        with self._lock:
            ret = self._data.get(key, None)
            if ret is None or len(ret) != 2:
                return default
            else:
                value = ret[0]
                expires_at = ret[1]
                # 检查是否过期
                if expires_at is None or expires_at > time.time():
                    return value
                else:
                    # 已过期，删除并返回默认值
                    del self._data[key]
                    return default

    def set(self, key, value, ttl=3600):
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 生存时间（秒），默认1小时
        """
        if value is None:
            return
        with self._lock:
            self._data[key] = (value, int(time.time()) + ttl)

    def delete(self, key):
        """
        删除缓存项
        
        Args:
            key: 缓存键
        """
        with self._lock:
            self._data.pop(key, None)
    
    def clear(self):
        """清空所有缓存"""
        with self._lock:
            self._data.clear()
    
    def size(self):
        """获取缓存项数量"""
        with self._lock:
            return len(self._data)


# ============================================================================
# 全局单例 - 用于OAuth token缓存
# ============================================================================
_global_token_storage = MemoryStorage()


def get_token_storage():
    """
    获取全局token存储单例
    
    返回值用于钉钉/企业微信SDK的token缓存
    所有OAuth提供商共享同一个缓存实例
    
    Returns:
        MemoryStorage: 全局token存储实例
    """
    return _global_token_storage

