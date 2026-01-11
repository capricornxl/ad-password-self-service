# -*- coding: utf-8 -*-
"""
LDAP适配器工厂
根据配置创建相应的LDAP适配器实例
"""

from .adapter import LDAPAdapter
from .ad_adapter import ADAdapter
from .openldap_adapter import OpenLDAPAdapter
from .errors import LDAPException, LDAPErrorCode
from utils.config import get_config
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class LDAPFactory:
    """LDAP适配器工厂"""
    
    # 适配器注册表
    _adapters = {
        'ad': ADAdapter,
        'openldap': OpenLDAPAdapter
    }
    
    @classmethod
    def create_adapter(cls, ldap_type: str = None) -> LDAPAdapter:
        """
        创建LDAP适配器
        
        Args:
            ldap_type: LDAP类型 ('ad' 或 'openldap'),如果为None则从配置读取
            
        Returns:
            LDAP适配器实例
            
        Raises:
            LDAPException: 如果LDAP类型不支持
        """
        config = get_config()
        
        # 从配置读取LDAP类型
        if ldap_type is None:
            ldap_type = config.get('ldap.type', 'ad').lower()
        else:
            ldap_type = ldap_type.lower()
        
        logger.debug(f"创建LDAP适配器: type={ldap_type}")
        
        # 检查是否支持
        if ldap_type not in cls._adapters:
            supported_types = ', '.join(cls._adapters.keys())
            error_msg = f"不支持的LDAP类型: {ldap_type} (支持: {supported_types})"
            logger.error(error_msg)
            raise LDAPException(
                LDAPErrorCode.CONFIGURATION_ERROR,
                error_msg,
                'factory'
            )
        
        # 创建适配器实例
        adapter_class = cls._adapters[ldap_type]
        adapter = adapter_class()
        
        logger.info(f"LDAP适配器创建成功: {ldap_type} -> {adapter_class.__name__}")
        return adapter
    
    @classmethod
    def register_adapter(cls, ldap_type: str, adapter_class: type):
        """
        注册新的适配器类型
        
        Args:
            ldap_type: LDAP类型标识
            adapter_class: 适配器类 (必须继承自LDAPAdapter)
        """
        if not issubclass(adapter_class, LDAPAdapter):
            raise TypeError(f"适配器类必须继承自LDAPAdapter: {adapter_class}")
        
        cls._adapters[ldap_type.lower()] = adapter_class
        logger.info(f"注册LDAP适配器: {ldap_type} -> {adapter_class.__name__}")
    
    @classmethod
    def get_supported_types(cls) -> list:
        """获取支持的LDAP类型列表"""
        return list(cls._adapters.keys())
