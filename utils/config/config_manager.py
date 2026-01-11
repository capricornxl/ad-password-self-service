# -*- coding: utf-8 -*-
"""
配置管理器 - 单例模式
支持YAML配置加载、环境变量注入、点访问语法
"""
import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path
import re


class ConfigManager:
    """全局配置管理器单例"""
    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_config(self, config_file: str) -> None:
        """
        加载YAML配置文件
        
        Args:
            config_file: 配置文件路径
            
        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: YAML解析错误
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                
            # 尝试解析YAML
            try:
                config_data = yaml.safe_load(file_content)
            except yaml.YAMLError as yaml_err:
                # 提取详细的错误信息
                error_details = self._format_yaml_error(yaml_err, config_file, file_content)
                raise yaml.YAMLError(error_details)
            
            # 递归替换环境变量
            try:
                self._config = self._replace_env_vars(config_data)
            except Exception as env_err:
                error_details = self._format_env_var_error(env_err, config_file)
                raise ValueError(error_details)
                
        except yaml.YAMLError:
            raise
        except Exception as e:
            raise Exception(f"配置加载失败: {e}")

    @staticmethod
    def _replace_env_vars(obj: Any) -> Any:
        """
        递归替换对象中的环境变量 ${VAR_NAME}
        
        Args:
            obj: 任意对象（dict, list, str等）
            
        Returns:
            替换后的对象
        """
        if isinstance(obj, dict):
            return {k: ConfigManager._replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ConfigManager._replace_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # 替换 ${VAR_NAME} 格式的环境变量
            def replace_match(match):
                try:
                    var_name = match.group(1)
                    # 支持 ${VAR:default} 格式，group(2) 是完整的 :default 部分
                    default_part = match.group(2)
                    default_value = default_part[1:] if default_part else ''  # 去掉冒号
                    return os.getenv(var_name, default_value)
                except IndexError as e:
                    raise ValueError(
                        f"环境变量模式匹配失败: '{match.group(0)}'\n"
                        f"  原始字符串: {obj}\n"
                        f"  错误: {e}"
                    )
            
            # 支持 ${VAR} 和 ${VAR:default} 格式
            pattern = r'\$\{([A-Za-z_][A-Za-z0-9_]*)(:([^}]*))?\}'
            try:
                return re.sub(pattern, replace_match, obj)
            except Exception as e:
                raise ValueError(
                    f"环境变量替换失败: '{obj}'\n"
                    f"  错误: {e}"
                )
        else:
            return obj

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        获取配置值，支持点访问语法
        
        Example:
            config.get('ldap.host')
            config.get('oauth_providers.wework.corp_id')
            config.get('nonexistent.key', 'default_value')
        
        Args:
            key_path: 配置键路径（使用点分隔）
            default: 键不存在时的默认值
            
        Returns:
            配置值或默认值
        """
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value

    def get_dict(self, key_path: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        获取配置字典
        
        Args:
            key_path: 配置键路径
            default: 默认值（当配置不存在或不是字典时返回）
            
        Returns:
            配置字典
            
        Raises:
            ValueError: 配置值不是字典类型且未提供默认值
        """
        if default is None:
            default = {}
        
        result = self.get(key_path, default)
        if not isinstance(result, dict):
            if default is not None:
                return default
            raise ValueError(f"配置值 {key_path} 不是字典类型")
        return result

    def validate(self) -> bool:
        """
        验证配置完整性
        
        Returns:
            配置是否有效
            
        Raises:
            ValueError: 缺少必要配置
        """
        required_keys = [
            'app.title',
            'auth.provider',
            'ldap.host',
            'ldap.domain',
            'password_policy.min_length',
            'oauth_providers.ding.corp_id' if self.get('auth.provider') == 'ding' else None,
            'oauth_providers.wework.corp_id' if self.get('auth.provider') == 'wework' else None,
        ]
        
        for key in required_keys:
            if key and self.get(key) is None:
                raise ValueError(f"缺少必要配置: {key}")
        
        return True

    def reload(self, config_file: str) -> None:
        """热重载配置"""
        self._config.clear()
        self.load_config(config_file)

    def to_dict(self) -> Dict[str, Any]:
        """返回全部配置字典"""
        return self._config.copy()
    
    @staticmethod
    def _format_yaml_error(error: yaml.YAMLError, file_path: str, content: str) -> str:
        """
        格式化YAML解析错误信息，类似yamllint的输出
        
        Args:
            error: YAML错误对象
            file_path: 文件路径
            content: 文件内容
            
        Returns:
            格式化的错误消息
        """
        lines = content.split('\n')
        error_msg = str(error)
        
        # 尝试提取行号和列号
        line_num = None
        col_num = None
        
        if hasattr(error, 'problem_mark'):
            mark = error.problem_mark
            line_num = mark.line + 1  # YAML行号从0开始
            col_num = mark.column + 1
        
        # 构建详细错误信息
        formatted_error = [
            "\n" + "="*70,
            "YAML 语法错误",
            "="*70,
            f"文件: {file_path}",
        ]
        
        if line_num:
            formatted_error.append(f"行号: {line_num}, 列号: {col_num}")
            formatted_error.append("")
            
            # 显示问题所在的行及其上下文
            start_line = max(0, line_num - 3)
            end_line = min(len(lines), line_num + 2)
            
            formatted_error.append("问题上下文:")
            formatted_error.append("-" * 70)
            
            for i in range(start_line, end_line):
                line_number = i + 1
                prefix = ">>> " if line_number == line_num else "    "
                formatted_error.append(f"{prefix}{line_number:4d} | {lines[i]}")
                
                # 在错误行下方标记错误位置
                if line_number == line_num and col_num:
                    pointer = " " * (len(prefix) + 6) + " " * (col_num - 1) + "^"
                    formatted_error.append(pointer)
            
            formatted_error.append("-" * 70)
        
        # 添加错误描述
        formatted_error.append("")
        formatted_error.append("错误描述:")
        
        if hasattr(error, 'problem'):
            formatted_error.append(f"  {error.problem}")
        if hasattr(error, 'context'):
            formatted_error.append(f"  上下文: {error.context}")
        
        formatted_error.append("")
        formatted_error.append("原始错误信息:")
        formatted_error.append(f"  {error_msg}")
        formatted_error.append("")
        formatted_error.append("="*70)
        
        return "\n".join(formatted_error)
    
    @staticmethod
    def _format_env_var_error(error: Exception, file_path: str) -> str:
        """
        格式化环境变量替换错误
        
        Args:
            error: 异常对象
            file_path: 文件路径
            
        Returns:
            格式化的错误消息
        """
        formatted_error = [
            "\n" + "="*70,
            "环境变量替换错误",
            "="*70,
            f"文件: {file_path}",
            "",
            "错误描述:",
            f"  {str(error)}",
            "",
            "可能的原因:",
            "  1. 正则表达式模式错误",
            "  2. 环境变量格式不正确（应为 ${VAR_NAME} 或 ${VAR:default}）",
            "  3. 环境变量名包含非法字符",
            "",
            "="*70,
        ]
        
        return "\n".join(formatted_error)


# 全局配置实例
_config_manager = ConfigManager()


def init_config(config_file: str) -> ConfigManager:
    """初始化全局配置"""
    _config_manager.load_config(config_file)
    _config_manager.validate()
    return _config_manager


def get_config() -> ConfigManager:
    """获取全局配置管理器"""
    return _config_manager
