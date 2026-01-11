# -*- coding: utf-8 -*-
"""
验证码管理器
负责验证码的生成、存储、验证和限流
"""
import random
import string
import time
from typing import Tuple, Optional
from django.core.cache import cache
from utils.config import get_config
from utils.logger_factory import get_logger
from utils.rate_limiter import RateLimiter
from .errors import SMSException, SMSErrorCode

logger = get_logger(__name__)


class SMSCodeManager:
    """
    验证码管理器
    
    功能：
    1. 生成验证码
    2. 存储验证码（使用Django Cache）
    3. 验证验证码
    4. 限流控制（防刷）
    """
    
    def __init__(self):
        """初始化验证码管理器"""
        self.config = get_config()
        self.rate_limiter = RateLimiter()
        
        # 从配置读取参数
        self.code_length = self.config.get('sms.code.length', 6)
        self.code_expire_seconds = self.config.get('sms.code.expire_seconds', 300)
        self.code_type = self.config.get('sms.code.code_type', 'numeric')
        
        # 限流配置
        self.send_interval = self.config.get('sms.rate_limiting.same_mobile_interval', 60)
        self.daily_limit = self.config.get('sms.rate_limiting.same_mobile_daily_limit', 10)
        self.verify_max_attempts = self.config.get('sms.rate_limiting.verify_max_attempts', 5)
    
    def generate_code(self, length: Optional[int] = None) -> str:
        """
        生成验证码
        
        Args:
            length: 验证码长度（可选，默认使用配置值）
            
        Returns:
            验证码字符串
            
        Raises:
            SMSException: 生成失败时抛出
        """
        length = length or self.code_length
        
        try:
            if self.code_type == 'numeric':
                # 纯数字验证码
                code = ''.join(random.choices(string.digits, k=length))
            elif self.code_type == 'alphanumeric':
                # 字母数字验证码（不包含容易混淆的字符）
                chars = string.digits + 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # 排除 I, O
                code = ''.join(random.choices(chars, k=length))
            else:
                code = ''.join(random.choices(string.digits, k=length))
            
            logger.debug(f"验证码生成成功: 长度={length}, 类型={self.code_type}")
            return code
            
        except Exception as e:
            logger.error(f"验证码生成失败: {e}")
            raise SMSException(
                SMSErrorCode.CODE_GENERATION_FAILED,
                "验证码生成失败",
                "generate_code",
                e
            )
    
    def store_code(
        self, 
        mobile: str, 
        code: str, 
        username: Optional[str] = None,
        expire_seconds: Optional[int] = None
    ):
        """
        存储验证码到缓存
        
        Args:
            mobile: 手机号
            code: 验证码
            username: 关联的用户名（可选）
            expire_seconds: 过期时间（秒），默认使用配置值
        """
        expire_seconds = expire_seconds or self.code_expire_seconds
        
        # 缓存键
        code_key = f"sms_code:{mobile}"
        info_key = f"sms_info:{mobile}"
        
        # 存储验证码
        cache.set(code_key, code, timeout=expire_seconds)
        
        # 存储附加信息
        info = {
            'code': code,
            'mobile': mobile,
            'username': username,
            'created_at': int(time.time()),
            'expire_at': int(time.time()) + expire_seconds,
            'attempts': 0,  # 验证尝试次数
            'used': False   # 是否已使用
        }
        cache.set(info_key, info, timeout=expire_seconds)
        
        logger.info(f"验证码已存储: 手机号={mobile[:3]}****{mobile[-4:]}, 有效期={expire_seconds}秒")
    
    def verify_code(self, mobile: str, code: str) -> Tuple[bool, str, Optional[str]]:
        """
        验证验证码
        
        Args:
            mobile: 手机号
            code: 用户输入的验证码
            
        Returns:
            Tuple[验证成功, 消息, 关联用户名]
            
        Raises:
            SMSException: 验证失败时抛出
        """
        code_key = f"sms_code:{mobile}"
        info_key = f"sms_info:{mobile}"
        
        # 获取验证码信息
        info = cache.get(info_key)
        
        if not info:
            logger.warning(f"验证码不存在或已过期: {mobile[:3]}****{mobile[-4:]}")
            raise SMSException(
                SMSErrorCode.CODE_NOT_FOUND,
                "验证码不存在或已过期",
                "verify_code"
            )
        
        # 检查是否已使用
        if info.get('used', False):
            logger.warning(f"验证码已使用: {mobile[:3]}****{mobile[-4:]}")
            raise SMSException(
                SMSErrorCode.CODE_ALREADY_USED,
                "验证码已使用",
                "verify_code"
            )
        
        # 检查验证尝试次数
        attempts = info.get('attempts', 0)
        if attempts >= self.verify_max_attempts:
            logger.warning(f"验证次数过多: {mobile[:3]}****{mobile[-4:]}, 次数={attempts}")
            # 删除验证码
            self.invalidate_code(mobile)
            raise SMSException(
                SMSErrorCode.TOO_MANY_ATTEMPTS,
                f"验证次数过多（{attempts}次），请重新获取验证码",
                "verify_code"
            )
        
        # 增加尝试次数
        info['attempts'] = attempts + 1
        cache.set(info_key, info, timeout=self.code_expire_seconds)
        
        # 验证验证码
        stored_code = info.get('code')
        if code == stored_code:
            # 验证成功，标记为已使用
            info['used'] = True
            cache.set(info_key, info, timeout=self.code_expire_seconds)
            
            username = info.get('username')
            logger.info(f"验证码验证成功: {mobile[:3]}****{mobile[-4:]}")
            return True, "验证码正确", username
        else:
            logger.warning(f"验证码错误: {mobile[:3]}****{mobile[-4:]}, 尝试次数={info['attempts']}")
            raise SMSException(
                SMSErrorCode.CODE_INVALID,
                f"验证码错误，剩余尝试次数：{self.verify_max_attempts - info['attempts']}",
                "verify_code"
            )
    
    def invalidate_code(self, mobile: str):
        """
        使验证码失效（立即删除）
        
        Args:
            mobile: 手机号
        """
        code_key = f"sms_code:{mobile}"
        info_key = f"sms_info:{mobile}"
        
        cache.delete(code_key)
        cache.delete(info_key)
        
        logger.debug(f"验证码已失效: {mobile[:3]}****{mobile[-4:]}")
    
    def is_send_rate_limited(self, mobile: str) -> Tuple[bool, int]:
        """
        检查发送频率限制
        
        Args:
            mobile: 手机号
            
        Returns:
            Tuple[是否被限制, 需要等待的秒数]
        """
        rate_limit_key = f"sms_send_limit:{mobile}"
        
        # 检查是否在冷却时间内
        last_send_time = cache.get(rate_limit_key)
        if last_send_time:
            elapsed = int(time.time()) - last_send_time
            if elapsed < self.send_interval:
                wait_seconds = self.send_interval - elapsed
                logger.debug(f"发送频率受限: {mobile[:3]}****{mobile[-4:]}, 等待{wait_seconds}秒")
                return True, wait_seconds
        
        return False, 0
    
    def is_daily_limit_reached(self, mobile: str) -> Tuple[bool, int]:
        """
        检查每日发送次数限制
        
        Args:
            mobile: 手机号
            
        Returns:
            Tuple[是否达到上限, 今日已发送次数]
        """
        daily_key = f"sms_daily_count:{mobile}"
        
        count = cache.get(daily_key, 0)
        if count >= self.daily_limit:
            logger.warning(f"达到每日发送上限: {mobile[:3]}****{mobile[-4:]}, 次数={count}")
            return True, count
        
        return False, count
    
    def record_send(self, mobile: str):
        """
        记录发送行为（用于限流）
        
        Args:
            mobile: 手机号
        """
        # 记录最后发送时间
        rate_limit_key = f"sms_send_limit:{mobile}"
        cache.set(rate_limit_key, int(time.time()), timeout=self.send_interval)
        
        # 增加每日发送计数
        daily_key = f"sms_daily_count:{mobile}"
        count = cache.get(daily_key, 0)
        # 设置到当天结束的过期时间（秒）
        import datetime
        now = datetime.datetime.now()
        tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        seconds_until_tomorrow = int((tomorrow - now).total_seconds())
        
        cache.set(daily_key, count + 1, timeout=seconds_until_tomorrow)
        
        logger.debug(f"记录发送行为: {mobile[:3]}****{mobile[-4:]}, 今日第{count + 1}次")
    
    def get_code_info(self, mobile: str) -> Optional[dict]:
        """
        获取验证码信息（调试用）
        
        Args:
            mobile: 手机号
            
        Returns:
            验证码信息字典或None
        """
        info_key = f"sms_info:{mobile}"
        return cache.get(info_key)
