# -*- coding: utf-8 -*-
"""
SMS 提供商工厂

负责创建和管理不同的SMS服务提供商实例
"""
import importlib
import pkgutil
from typing import Dict, Type, Optional
from utils.config import get_config
from utils.logger_factory import get_logger
from .base_provider import BaseSMSProvider
from .errors import SMSException, SMSErrorCode

logger = get_logger(__name__)


class SMSFactory:
    """
    SMS 提供商工厂
    
    支持：
    1. 动态加载SMS提供商
    2. 提供商注册机制
    3. 根据配置创建提供商实例
    """
    
    # 提供商注册表（类级别）
    _providers: Dict[str, Type[BaseSMSProvider]] = {}
    
    # 当前提供商实例缓存
    _current_provider: Optional[BaseSMSProvider] = None
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseSMSProvider]):
        """
        注册SMS提供商
        
        Args:
            name: 提供商名称（如 'mock', 'aliyun', 'tencent'）
            provider_class: 提供商类
        """
        cls._providers[name] = provider_class
        logger.debug(f"SMS提供商已注册: {name}")
    
    @classmethod
    def create_provider(cls, provider_name: Optional[str] = None) -> BaseSMSProvider:
        """
        创建SMS提供商实例
        
        Args:
            provider_name: 提供商名称（可选，默认从配置读取）
            
        Returns:
            SMS提供商实例
            
        Raises:
            SMSException: 创建失败时抛出
        """
        config = get_config()
        
        # 从配置获取提供商名称
        if provider_name is None:
            provider_name = config.get('sms.provider', 'mock')
        
        logger.debug(f"创建SMS提供商: {provider_name}")
        
        # 检查提供商是否已注册
        if provider_name not in cls._providers:
            logger.error(f"未注册的SMS提供商: {provider_name}")
            raise SMSException(
                SMSErrorCode.PROVIDER_NOT_FOUND,
                f"SMS提供商 '{provider_name}' 未注册",
                "create_provider"
            )
        
        # 获取提供商类
        provider_class = cls._providers[provider_name]
        
        # 创建实例
        try:
            provider = provider_class()
            logger.info(f"SMS提供商创建成功: {provider_name}")
            return provider
        except Exception as e:
            logger.error(f"SMS提供商创建失败: {provider_name}, 错误: {e}")
            raise SMSException(
                SMSErrorCode.CONFIGURATION_ERROR,
                f"创建SMS提供商失败: {str(e)}",
                "create_provider",
                e
            )
    
    @classmethod
    def get_current_provider(cls) -> BaseSMSProvider:
        """
        获取当前配置的SMS提供商实例（单例模式）
        
        Returns:
            SMS提供商实例
            
        Raises:
            SMSException: 获取失败时抛出
        """
        if cls._current_provider is None:
            cls._current_provider = cls.create_provider()
        
        return cls._current_provider
    
    @classmethod
    def reset_current_provider(cls):
        """
        重置当前提供商实例（用于配置变更后重新加载）
        """
        cls._current_provider = None
        logger.debug("当前SMS提供商已重置")
    
    @classmethod
    def list_providers(cls) -> list:
        """
        列出所有已注册的提供商
        
        Returns:
            提供商名称列表
        """
        return list(cls._providers.keys())
    
    @classmethod
    def validate_provider_config(cls, provider_name: str) -> bool:
        """
        验证指定提供商的配置
        
        Args:
            provider_name: 提供商名称
            
        Returns:
            配置是否有效
        """
        try:
            provider = cls.create_provider(provider_name)
            provider.validate_config()
            return True
        except SMSException as e:
            logger.error(f"提供商配置验证失败: {provider_name}, 错误: {e}")
            return False
    
    @classmethod
    def get_provider_info(cls, provider_name: str) -> dict:
        """
        获取提供商信息
        
        Args:
            provider_name: 提供商名称
            
        Returns:
            提供商信息字典
        """
        if provider_name not in cls._providers:
            return {
                'name': provider_name,
                'registered': False
            }
        
        provider_class = cls._providers[provider_name]
        
        return {
            'name': provider_name,
            'registered': True,
            'class': provider_class.__name__,
            'module': provider_class.__module__
        }

# from .providers.aliyun_provider import AliyunSMSProvider
# SMSFactory.register_provider('aliyun', AliyunSMSProvider)
def _register_builtin_providers():
    """
    自动扫描并注册 providers 目录下的所有 SMS 提供商
    
    此函数在模块导入时自动调用，实现：
    1. 扫描 utils/sms/providers/ 目录下所有 *_provider.py 文件
    2. 动态导入模块并查找 BaseSMSProvider 的子类
    3. 自动提取 provider 名称并注册
    
    新增 provider 只需创建 *_provider.py 文件，无需修改此文件
    """
    providers_package = 'utils.sms.providers'
    
    try:
        # 导入 providers 包
        package = importlib.import_module(providers_package)
        package_path = package.__path__
        
        # 遍历所有模块
        for importer, module_name, is_pkg in pkgutil.iter_modules(package_path):
            # 只处理 *_provider.py 文件
            if not module_name.endswith('_provider'):
                continue
            
            # 跳过 __init__ 等特殊模块
            if module_name.startswith('_'):
                continue
            
            try:
                # 动态导入模块
                module = importlib.import_module(f'{providers_package}.{module_name}')
                
                # 查找 BaseSMSProvider 的子类
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    
                    # 检查是否是类、是否是 BaseSMSProvider 的子类、且不是基类本身
                    if (isinstance(attr, type) and
                        issubclass(attr, BaseSMSProvider) and
                        attr is not BaseSMSProvider):
                        
                        # 从模块名提取 provider 名称：aliyun_provider -> aliyun
                        # 这是主要方式，确保名称与文件命名一致
                        provider_type = module_name.replace('_provider', '')
                        
                        # 注册提供商
                        SMSFactory.register_provider(provider_type, attr)
                        logger.debug(f"自动注册 SMS provider: {provider_type} -> {attr.__name__}")
                        
            except ImportError as e:
                # 导入失败（可能是依赖未安装），记录警告但不影响其他 provider
                logger.debug(f"导入 SMS provider {module_name} 失败（可能未安装依赖）: {e}")
            except Exception as e:
                # 其他异常，记录警告
                logger.warning(f"注册 SMS provider {module_name} 时发生错误: {e}")
                
    except Exception as e:
        logger.error(f"扫描 SMS providers 目录失败: {e}")
    
    # 输出注册结果
    registered = SMSFactory.list_providers()
    if registered:
        logger.info(f"已注册 SMS 提供商: {registered}")
    else:
        logger.warning("未找到任何 SMS 提供商")


# 便捷函数：获取当前SMS提供商实例
def get_sms_provider() -> BaseSMSProvider:
    """
    获取当前配置的SMS提供商实例（便捷函数）
    
    Returns:
        SMS提供商实例
    """
    return SMSFactory.get_current_provider()


# 模块导入时自动注册提供商
_register_builtin_providers()
