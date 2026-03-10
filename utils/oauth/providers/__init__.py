# -*- coding: utf-8 -*-
"""
OAuth providers 包

此模块允许通过导入 providers 包触发 provider 模块的加载。
"""

__all__ = []

try:
    from .ding_provider import DingTalkProvider
    __all__.append('DingTalkProvider')
except ImportError:
    pass

try:
    from .wework_provider import WeWorkProvider
    __all__.append('WeWorkProvider')
except ImportError:
    pass
