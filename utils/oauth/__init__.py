# -*- coding: utf-8 -*-
"""
OAuth模块初始化

支持插件化的 OAuth Provider 自动注册。
"""
from .factory import OAuthFactory, get_oauth_factory

__all__ = [
    'OAuthFactory',
    'get_oauth_factory',
]
