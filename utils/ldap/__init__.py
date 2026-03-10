# -*- coding: utf-8 -*-
"""
LDAP抽象层模块
提供AD和OpenLDAP的统一访问接口
"""

from .errors import LDAPErrorCode, LDAPException
from .adapter import LDAPAdapter
from .factory import LDAPFactory

__all__ = [
    'LDAPErrorCode',
    'LDAPException',
    'LDAPAdapter',
    'LDAPFactory'
]
