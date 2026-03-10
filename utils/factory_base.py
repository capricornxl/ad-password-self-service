# -*- coding: utf-8 -*-
"""
通用工厂基类

提供可扩展的注册器模式，支持动态注册和创建实例。

使用示例:
    class MyAdapter:
        def do_something(self):
            pass
    
    class MyFactory(BaseFactory):
        _base_class = MyAdapter
        _type_name = "adapter"
    
    # 注册
    MyFactory.register("my_type", MyAdapterImpl)
    
    # 创建
    adapter = MyFactory.create("my_type")
"""
from typing import Dict, Type, TypeVar, Generic, Optional, List
from utils.logger_factory import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


class BaseFactory(Generic[T]):
    """
    通用工厂基类
    
    特性:
    1. 支持动态注册
    2. 类型检查
    3. 自动发现和加载
    4. 单例缓存
    """
    
    # 子类必须指定基类
    _base_class: Type[T] = None
    # 类型名称（用于日志）
    _type_name: str = "component"
    # 注册表（类级别）
    _registry: Dict[str, Type[T]] = {}
    # 实例缓存（类级别）
    _instances: Dict[str, T] = {}
    
    @classmethod
    def register(cls, type_name: str, component_class: Type[T]) -> None:
        """
        注册组件类型
        
        Args:
            type_name: 类型标识（不区分大小写）
            component_class: 组件类
            
        Raises:
            TypeError: 如果组件类不是 _base_class 的子类
        """
        if cls._base_class and not issubclass(component_class, cls._base_class):
            raise TypeError(
                f"{cls._type_name} 类必须继承自 {cls._base_class.__name__}: "
                f"{component_class.__name__}"
            )
        
        type_key = type_name.lower()
        cls._registry[type_key] = component_class
        logger.debug(f"注册 {cls._type_name}: {type_name} -> {component_class.__name__}")
    
    @classmethod
    def unregister(cls, type_name: str) -> bool:
        """
        注销组件类型
        
        Args:
            type_name: 类型标识
            
        Returns:
            是否成功注销
        """
        type_key = type_name.lower()
        if type_key in cls._registry:
            del cls._registry[type_key]
            # 同时清除缓存实例
            if type_key in cls._instances:
                del cls._instances[type_key]
            logger.debug(f"注销 {cls._type_name}: {type_name}")
            return True
        return False
    
    @classmethod
    def create(cls, type_name: str, *args, **kwargs) -> T:
        """
        创建组件实例
        
        Args:
            type_name: 类型标识
            *args, **kwargs: 传递给组件构造函数的参数
            
        Returns:
            组件实例
            
        Raises:
            ValueError: 如果类型未注册
        """
        type_key = type_name.lower()
        
        if type_key not in cls._registry:
            supported = ', '.join(cls.get_registered_types())
            raise ValueError(
                f"不支持的 {cls._type_name} 类型: {type_name} (支持: {supported})"
            )
        
        component_class = cls._registry[type_key]
        instance = component_class(*args, **kwargs)
        
        logger.debug(f"创建 {cls._type_name} 实例: {type_name}")
        return instance
    
    @classmethod
    def get_instance(cls, type_name: str, *args, **kwargs) -> T:
        """
        获取单例实例（带缓存）
        
        如果实例已存在则返回缓存实例，否则创建新实例并缓存。
        
        Args:
            type_name: 类型标识
            *args, **kwargs: 传递给组件构造函数的参数（仅在首次创建时使用）
            
        Returns:
            组件实例
        """
        type_key = type_name.lower()
        
        if type_key not in cls._instances:
            cls._instances[type_key] = cls.create(type_name, *args, **kwargs)
        
        return cls._instances[type_key]
    
    @classmethod
    def clear_cache(cls, type_name: str = None) -> None:
        """
        清除实例缓存
        
        Args:
            type_name: 指定类型，None 表示清除所有
        """
        if type_name:
            type_key = type_name.lower()
            if type_key in cls._instances:
                del cls._instances[type_key]
        else:
            cls._instances.clear()
    
    @classmethod
    def is_registered(cls, type_name: str) -> bool:
        """
        检查类型是否已注册
        
        Args:
            type_name: 类型标识
            
        Returns:
            是否已注册
        """
        return type_name.lower() in cls._registry
    
    @classmethod
    def get_registered_types(cls) -> List[str]:
        """
        获取所有已注册的类型
        
        Returns:
            类型标识列表
        """
        return list(cls._registry.keys())
    
    @classmethod
    def get_registered_classes(cls) -> Dict[str, Type[T]]:
        """
        获取注册表（只读）
        
        Returns:
            类型到类的映射
        """
        return dict(cls._registry)


def auto_register(factory_class: Type[BaseFactory], module_name: str = None):
    """
    自动注册装饰器
    
    用于自动将类注册到工厂。
    
    使用示例:
        @auto_register(MyFactory, "my_type")
        class MyAdapterImpl:
            pass
    
    Args:
        factory_class: 工厂类
        module_name: 注册的类型名（可选，默认使用类名的小写）
    """
    def decorator(cls):
        type_name = module_name or cls.__name__.lower()
        factory_class.register(type_name, cls)
        return cls
    return decorator