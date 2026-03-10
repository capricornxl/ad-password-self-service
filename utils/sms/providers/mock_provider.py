# -*- coding: utf-8 -*-
"""
Mock SMS 提供商

用于开发和测试环境的模拟SMS服务
"""
import time
from typing import Tuple, Optional
from utils.logger_factory import get_logger
from ..base_provider import BaseSMSProvider
from ..errors import SMSException, SMSErrorCode

logger = get_logger(__name__)


class MockSMSProvider(BaseSMSProvider):
    """
    Mock SMS 提供商
    
    功能：
    1. 模拟短信发送（不实际发送）
    2. 可配置的自动通过模式
    3. 可配置的延迟模拟
    4. 测试用的固定验证码
    """
    
    @property
    def provider_name(self) -> str:
        """提供商显示名称"""
        return "Mock SMS服务"
    
    @property
    def provider_type(self) -> str:
        """提供商类型标识"""
        return "mock"
    
    def __init__(self):
        """初始化 Mock 提供商"""
        super().__init__()
        
        # Mock 特定配置
        self.auto_pass = self.config.get('sms.mock.auto_pass', True)
        self.simulate_delay = self.config.get('sms.mock.simulate_delay', 0)
        self.fixed_code = self.config.get('sms.mock.fixed_code', None)
        self.fail_rate = self.config.get('sms.mock.fail_rate', 0.0)
        
        logger.info(f"Mock SMS提供商初始化: auto_pass={self.auto_pass}, delay={self.simulate_delay}s")
    
    def send_verification_code(
        self,
        mobile: str,
        code: str,
        template_id: Optional[str] = None,
        template_params: Optional[dict] = None
    ) -> Tuple[bool, str]:
        """
        模拟发送验证码
        
        Args:
            mobile: 手机号
            code: 验证码
            template_id: 模板ID（Mock中忽略）
            template_params: 模板参数（Mock中忽略）
            
        Returns:
            Tuple[成功, 消息]
        """
        # 使用固定验证码（如果配置了）
        if self.fixed_code:
            code = self.fixed_code
            logger.debug(f"使用固定验证码: {code}")
        
        # 模拟延迟
        if self.simulate_delay > 0:
            logger.debug(f"模拟延迟: {self.simulate_delay}秒")
            time.sleep(self.simulate_delay)
        
        # 模拟失败率
        if self.fail_rate > 0:
            import random
            if random.random() < self.fail_rate:
                self._log_send_failure(
                    mobile=mobile,
                    code=code,
                    error_code="MOCK_RANDOM_FAILURE",
                    error_message="模拟随机失败"
                )
                return False, "模拟发送失败（随机失败）"
        
        # 验证手机号格式
        formatted_mobile = self.format_mobile(mobile)
        if not formatted_mobile:
            self._log_send_failure(
                mobile=mobile,
                code=code,
                error_code="INVALID_MOBILE",
                error_message="手机号格式不正确"
            )
            return False, "手机号格式不正确"
        
        # 记录发送成功（仅日志，不实际发送）
        self._log_send_success(
            mobile=formatted_mobile,
            code=code,
            provider_msg_id=f"mock_{int(time.time())}",
            extra_info={
                'auto_pass': self.auto_pass,
                'fixed_code': self.fixed_code,
                'mode': 'mock'
            }
        )
        
        logger.warning(f"[MOCK] 验证码已生成（未实际发送）: {formatted_mobile[:3]}****{formatted_mobile[-4:]}, 验证码: {code}")
        
        return True, "验证码发送成功（Mock模式）"
    
    def query_send_status(self, message_id: str) -> Tuple[bool, str, str]:
        """
        查询发送状态（Mock中自动返回成功）
        
        Args:
            message_id: 消息ID
            
        Returns:
            Tuple[查询成功, 发送状态, 状态描述]
        """
        if self.auto_pass:
            return True, "delivered", "已送达（Mock）"
        else:
            return True, "pending", "等待送达（Mock）"
    
    def validate_config(self):
        """
        验证配置（Mock提供商配置始终有效）
        """
        logger.debug("Mock SMS配置验证通过")
    
    def format_mobile(self, mobile: str) -> str:
        """
        格式化手机号
        
        Args:
            mobile: 原始手机号
            
        Returns:
            格式化后的手机号
        """
        # 移除空格和短横线
        mobile = mobile.replace(' ', '').replace('-', '')
        
        # 移除+86前缀
        if mobile.startswith('+86'):
            mobile = mobile[3:]
        elif mobile.startswith('86') and len(mobile) == 13:
            mobile = mobile[2:]
        
        # 验证格式
        if not mobile.isdigit():
            return ""
        
        if len(mobile) != 11:
            return ""
        
        return mobile
    
    def get_send_params(self, mobile: str, code: str) -> dict:
        """
        获取发送参数（Mock模式返回空字典）
        
        Args:
            mobile: 手机号
            code: 验证码
            
        Returns:
            参数字典
        """
        return {
            'mobile': mobile,
            'code': code,
            'provider': 'mock',
            'auto_pass': self.auto_pass
        }
