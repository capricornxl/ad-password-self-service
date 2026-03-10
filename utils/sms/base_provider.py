# -*- coding: utf-8 -*-
"""
短信提供商抽象基类

所有短信提供商都应继承此类并实现所有抽象方法
"""
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional
from utils.config import get_config
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class BaseSMSProvider(ABC):
    """
    短信提供商抽象基类
    
    所有短信提供商（阿里云、腾讯云、华为云等）都应继承此类
    """
    
    def __init__(self):
        """初始化提供商"""
        self.logger = logger
        self.config = get_config()
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        提供商名称
        
        Returns:
            提供商显示名称（如：阿里云、腾讯云）
        """
        pass
    
    @property
    @abstractmethod
    def provider_type(self) -> str:
        """
        提供商类型标识
        
        Returns:
            提供商类型（如：aliyun、tencent、huawei）
        """
        pass
    
    @abstractmethod
    def send_verification_code(
        self, 
        mobile: str, 
        code: str,
        template_params: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        发送验证码短信
        
        Args:
            mobile: 手机号（已格式化，如：13800138000）
            code: 验证码
            template_params: 模板参数（可选），如：{"product": "密码服务", "expire": "5"}
            
        Returns:
            Tuple[成功状态, 消息ID或错误信息]
            
            成功: (True, "message_id_12345")
            失败: (False, "错误描述")
            
        Raises:
            SMSException: 发送失败时抛出异常
            
        Example:
            >>> provider = AliyunSMSProvider()
            >>> success, msg_id = provider.send_verification_code("13800138000", "123456")
            >>> if success:
            >>>     print(f"发送成功，消息ID: {msg_id}")
        """
        pass
    
    @abstractmethod
    def query_send_status(self, message_id: str) -> Tuple[bool, str]:
        """
        查询短信发送状态
        
        Args:
            message_id: 短信消息ID（send_verification_code返回的ID）
            
        Returns:
            Tuple[查询成功, 状态描述]
            
            成功查询: (True, "已送达")
            查询失败: (False, "查询失败原因")
            
        Note:
            某些提供商可能不支持状态查询，可以返回 (True, "不支持状态查询")
        """
        pass
    
    def validate_config(self) -> Tuple[bool, str]:
        """
        验证提供商配置是否完整
        
        Returns:
            Tuple[配置有效, 错误消息]
            
        Note:
            子类应重写此方法以验证必需的配置项
        """
        return True, "配置验证通过"
    
    def get_send_params(
        self, 
        mobile: str, 
        code: str,
        template_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        构建发送参数（可被子类重写）
        
        Args:
            mobile: 手机号
            code: 验证码
            template_params: 模板参数
            
        Returns:
            发送参数字典
        """
        return {
            'mobile': mobile,
            'code': code,
            'template_params': template_params or {}
        }
    
    def format_mobile(self, mobile: str) -> str:
        """
        格式化手机号（可被子类重写）
        
        Args:
            mobile: 原始手机号
            
        Returns:
            格式化后的手机号
            
        Note:
            默认去除空格和短横线，子类可以根据提供商要求重写
        """
        return mobile.replace(' ', '').replace('-', '').strip()
    
    def _log_send_success(
        self, 
        mobile: str, 
        code: str = None,
        message_id: str = None,
        provider_msg_id: str = None,
        extra_info: Optional[Dict[str, Any]] = None
    ):
        """
        记录发送成功日志
        
        Args:
            mobile: 手机号
            code: 验证码（可选，用于关联日志）
            message_id: 消息ID（可选，兼容旧接口）
            provider_msg_id: 提供商消息ID（可选）
            extra_info: 额外信息（可选），如模板ID、通道号等
        """
        masked_mobile = f"{mobile[:3]}****{mobile[-4:]}"
        masked_code = f"{code[:2]}**{code[-2:]}" if code else "N/A"
        msg_id = provider_msg_id or message_id or "N/A"
        
        log_msg = (
            f"[{self.provider_name}] 验证码发送成功 | "
            f"手机号: {masked_mobile} | "
            f"验证码: {masked_code} | "
            f"消息ID: {msg_id}"
        )
        
        if extra_info:
            extra_str = ", ".join([f"{k}={v}" for k, v in extra_info.items()])
            log_msg += f" | 额外信息: {extra_str}"
        
        self.logger.info(log_msg)
    
    def _log_send_failure(
        self, 
        mobile: str, 
        error: str = None,
        code: str = None,
        error_code: str = None,
        error_message: str = None,
        extra_info: Optional[Dict[str, Any]] = None
    ):
        """
        记录发送失败日志
        
        Args:
            mobile: 手机号
            error: 错误描述（可选，兼容旧接口）
            code: 验证码（可选，用于关联日志）
            error_code: 错误码（可选）
            error_message: 错误消息（可选）
            extra_info: 额外错误信息（可选）
        """
        masked_mobile = f"{mobile[:3]}****{mobile[-4:]}"
        masked_code = f"{code[:2]}**{code[-2:]}" if code else "N/A"
        
        # 构建错误信息
        if error:
            error_info = error
        elif error_code and error_message:
            error_info = f"[{error_code}] {error_message}"
        elif error_message:
            error_info = error_message
        elif error_code:
            error_info = f"错误码: {error_code}"
        else:
            error_info = "未知错误"
        
        log_msg = (
            f"[{self.provider_name}] 验证码发送失败 | "
            f"手机号: {masked_mobile} | "
            f"验证码: {masked_code} | "
            f"错误: {error_info}"
        )
        
        if extra_info:
            # 过滤敏感信息
            safe_info = {k: v for k, v in extra_info.items() 
                        if k.lower() not in ['password', 'secret', 'key', 'token']}
            if safe_info:
                extra_str = ", ".join([f"{k}={v}" for k, v in safe_info.items()])
                log_msg += f" | 额外信息: {extra_str}"
        
        self.logger.error(log_msg)
