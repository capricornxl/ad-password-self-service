# -*- coding: utf-8 -*-
"""
日志系统工厂 - 集中管理日志配置和创建
"""
import logging
import logging.config
import yaml
import os
from typing import Optional, Dict, Any


class LoggerFactory:
    """日志工厂类"""
    
    _initialized = False
    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def setup_logging(cls, config_file: str, env_vars: Optional[Dict[str, str]] = None) -> None:
        """
        初始化日志系统
        
        Args:
            config_file: 日志配置YAML文件路径
            env_vars: 环境变量字典，用于替换配置中的 ${VAR}
            
        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: YAML解析错误
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"日志配置文件不存在: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # 替换环境变量
            if env_vars is None:
                env_vars = os.environ
            config_data = cls._replace_env_vars(config_data, env_vars)
            
            # 应用日志配置
            logging.config.dictConfig(config_data)
            
            # 修复 Windows 控制台编码问题
            cls._fix_console_encoding()
            
            cls._initialized = True
            
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"日志配置YAML解析失败: {e}")
        except Exception as e:
            raise Exception(f"日志系统初始化失败: {e}")

    @staticmethod
    def _replace_env_vars(obj: Any, env_vars: Dict[str, str]) -> Any:
        """
        递归替换环境变量
        
        支持格式：
        - ${VAR_NAME} - 必填变量，未定义时使用默认值
        - ${VAR_NAME:default_value} - 带默认值的变量
        """
        if isinstance(obj, dict):
            return {k: LoggerFactory._replace_env_vars(v, env_vars) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [LoggerFactory._replace_env_vars(item, env_vars) for item in obj]
        elif isinstance(obj, str):
            import re
            
            def replace_match(match):
                full_match = match.group(0)
                var_spec = match.group(1)
                
                # 支持 ${VAR:default} 语法
                if ':' in var_spec:
                    var_name, default_value = var_spec.split(':', 1)
                    value = env_vars.get(var_name.strip())
                    if value is None or value == '':
                        return default_value.strip()
                    return value
                else:
                    var_name = var_spec.strip()
                    value = env_vars.get(var_name)
                    
                    if value is None or value == '':
                        # 对于日志路径，提供默认值
                        if var_name == 'LOG_PATH':
                            print(f"警告: {var_name} 环境变量未定义，使用默认值: log")
                            return 'log'
                        else:
                            print(f"警告: {var_name} 环境变量未定义，保持原值: {full_match}")
                            return full_match
                    return value
            
            # 匹配 ${VAR_NAME} 或 ${VAR_NAME:default}
            return re.sub(r'\$\{([A-Za-z_][A-Za-z0-9_:.-]*)\}', replace_match, obj)
        else:
            return obj
    
    @staticmethod
    def _fix_console_encoding() -> None:
        """
        修复 Windows 控制台编码问题
        为所有 StreamHandler 设置 UTF-8 编码，避免特殊字符（如 ✓）输出错误
        """
        import sys
        import io
        
        # 获取根日志记录器
        root_logger = logging.getLogger()
        
        # 遍历所有处理器
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                # 如果是标准输出/错误流，使用 UTF-8 编码包装
                if handler.stream in (sys.stdout, sys.stderr):
                    try:
                        # 重新配置流为 UTF-8 编码，错误时替换为 '?'
                        handler.stream = io.TextIOWrapper(
                            handler.stream.buffer,
                            encoding='utf-8',
                            errors='replace',
                            line_buffering=True
                        )
                    except (AttributeError, ValueError):
                        # 如果流不支持 buffer 属性或其他错误，跳过
                        pass

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        获取或创建日志对象
        
        Args:
            name: 日志对象名称（通常使用 __name__）
            
        Returns:
            日志对象
        """
        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)
        return cls._loggers[name]


def setup_logging(config_file: str, env_vars: Optional[Dict[str, str]] = None) -> None:
    """初始化日志系统（模块级函数）"""
    LoggerFactory.setup_logging(config_file, env_vars)


def get_logger(name: str) -> logging.Logger:
    """获取日志对象（模块级函数）"""
    return LoggerFactory.get_logger(name)


# 为了向后兼容，导出常用的日志获取方式
def get_module_logger() -> logging.Logger:
    """获取当前模块的日志对象"""
    import inspect
    frame = inspect.currentframe()
    if frame and frame.f_back:
        module_name = frame.f_back.f_globals.get('__name__', 'app')
        return get_logger(module_name)
    return get_logger('app')
