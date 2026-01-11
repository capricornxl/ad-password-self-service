# -*- coding: utf-8 -*-
"""
OAuth工厂 - 创建和管理OAuth提供商实例
"""
import importlib
import pkgutil
from typing import Optional, Dict, Type
from utils.config import get_config
from utils.oauth.base_provider import BaseOAuthProvider
import logging

logger = logging.getLogger(__name__)


class OAuthFactory:
    """
    OAuth提供商工厂
    
    根据配置动态创建相应的OAuth提供商实例
    
    Example:
        factory = OAuthFactory()
        provider = factory.create_provider('wework')
        status, user_id, user_info = provider.get_user_detail(code, home_url)
    """
    
    # 提供商映射表（提供商类型 -> 提供商类）
    _providers: Dict[str, Type[BaseOAuthProvider]] = {}
    
    @classmethod
    def register_provider(cls, provider_type: str, provider_class: Type[BaseOAuthProvider]) -> None:
        """
        注册OAuth提供商
        
        Args:
            provider_type: 提供商类型（ding、wework等）
            provider_class: 提供商类
        """
        cls._providers[provider_type.lower()] = provider_class
        logger.info(f"已注册OAuth提供商: {provider_type}")
    
    @classmethod
    def create_provider(cls, provider_type: str) -> BaseOAuthProvider:
        """
        创建OAuth提供商实例
        
        Args:
            provider_type: 提供商类型
            
        Returns:
            提供商实例
            
        Raises:
            ValueError: 提供商类型不支持或未注册
        """
        provider_type = provider_type.lower()
        
        if provider_type not in cls._providers:
            raise ValueError(f"不支持的OAuth提供商类型: {provider_type}")
        
        provider_class = cls._providers[provider_type]
        provider = provider_class()
        logger.info(f"创建了{provider.provider_name}提供商实例")
        return provider
    
    @classmethod
    def get_current_provider(cls) -> BaseOAuthProvider:
        """
        获取当前配置的OAuth提供商实例
        
        Returns:
            提供商实例
            
        Raises:
            ValueError: 配置中的提供商类型不支持
        """
        config = get_config()
        provider_type = config.get('auth.provider', 'wework')
        return cls.create_provider(provider_type)
    
    @classmethod
    def is_provider_registered(cls, provider_type: str) -> bool:
        """
        检查提供商是否已注册
        
        Args:
            provider_type: 提供商类型
            
        Returns:
            是否已注册
        """
        return provider_type.lower() in cls._providers
    
    @classmethod
    def get_registered_providers(cls) -> list:
        """获取所有已注册的提供商类型"""
        return list(cls._providers.keys())


def _register_builtin_providers() -> None:
    """
    自动扫描并注册 providers 目录下的所有 OAuth 提供商
    
    实现：
    1. 扫描 utils/oauth/providers/ 目录下所有 *_provider.py 文件
    2. 动态导入模块并查找 BaseOAuthProvider 的子类
    3. 自动提取 provider 名称并注册
    """
    providers_package = 'utils.oauth.providers'

    try:
        package = importlib.import_module(providers_package)
        package_path = package.__path__

        for _, module_name, _ in pkgutil.iter_modules(package_path):
            if not module_name.endswith('_provider'):
                continue
            if module_name.startswith('_'):
                continue

            try:
                module = importlib.import_module(f'{providers_package}.{module_name}')

                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                        issubclass(attr, BaseOAuthProvider) and
                        attr is not BaseOAuthProvider):
                        provider_type = module_name.replace('_provider', '')
                        OAuthFactory.register_provider(provider_type, attr)
                        logger.debug(f"自动注册 OAuth provider: {provider_type} -> {attr.__name__}")

            except ImportError as e:
                logger.debug(f"导入 OAuth provider {module_name} 失败（可能未安装依赖）: {e}")
            except Exception as e:
                logger.warning(f"注册 OAuth provider {module_name} 时发生错误: {e}")

    except Exception as e:
        logger.error(f"扫描 OAuth providers 目录失败: {e}")

    registered = OAuthFactory.get_registered_providers()
    if registered:
        logger.info(f"已注册 OAuth 提供商: {registered}")
    else:
        logger.warning("未找到任何 OAuth 提供商")


# 全局工厂单例
_oauth_factory = OAuthFactory()


def get_oauth_factory() -> OAuthFactory:
    """获取OAuth工厂实例"""
    return _oauth_factory


_register_builtin_providers()
