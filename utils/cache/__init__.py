# -*- coding: utf-8 -*-
"""
缓存模块初始化
"""
from utils.cache.memory_cache import get_cache, MemoryCache
from utils.cache.token_cache import get_token_cache, TokenCache

__all__ = ['get_cache', 'MemoryCache', 'get_token_cache', 'TokenCache']
