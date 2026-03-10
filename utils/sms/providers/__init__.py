# -*- coding: utf-8 -*-
"""
SMS providers package

提供多种SMS服务提供商实现
"""
from .mock_provider import MockSMSProvider

__all__ = [
    'MockSMSProvider',
]

try:
    from .aliyun_provider import AliyunSMSProvider
    __all__.append('AliyunSMSProvider')
except ImportError:
    pass

try:
    from .tencent_provider import TencentSMSProvider
    __all__.append('TencentSMSProvider')
except ImportError:
    pass

try:
    from .huawei_provider import HuaweiSMSProvider
    __all__.append('HuaweiSMSProvider')
except ImportError:
    pass
