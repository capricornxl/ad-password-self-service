# -*- coding: utf-8 -*-
"""
审计日志 - 记录操作审计和关键事件
"""
import logging
from typing import Optional, Any, Dict
from datetime import datetime


class AuditLogger:
    """
    审计日志记录器
    
    记录关键操作，便于审计和故障排查
    """
    
    def __init__(self, logger_name: str = 'audit'):
        """
        初始化审计日志
        
        Args:
            logger_name: 日志对象名称
        """
        self.logger = logging.getLogger(logger_name)
    
    def log_oauth_success(self, provider: str, user_id: str, user_info: Dict[str, Any], 
                         session_id: str = '') -> None:
        """
        记录OAuth认证成功
        
        Args:
            provider: OAuth提供商（ding/wework）
            user_id: 用户ID
            user_info: 用户信息
            session_id: 会话ID
        """
        msg = (f"OAuth认证成功 | provider={provider} | user_id={user_id} | "
               f"user_name={user_info.get('name', 'N/A')} | "
               f"email={user_info.get('email', 'N/A')} | session_id={session_id}")
        self.logger.info(msg)
    
    def log_oauth_failure(self, provider: str, reason: str, session_id: str = '') -> None:
        """
        记录OAuth认证失败
        
        Args:
            provider: OAuth提供商
            reason: 失败原因
            session_id: 会话ID
        """
        msg = f"OAuth认证失败 | provider={provider} | reason={reason} | session_id={session_id}"
        self.logger.warning(msg)
    
    def log_password_reset(self, username: str, status: str, message: str = '', 
                          method: str = 'direct', session_id: str = '') -> None:
        """
        记录密码重置操作
        
        Args:
            username: 用户名
            status: 状态（success/failure）
            message: 详细信息
            method: 重置方法（direct/oauth）
            session_id: 会话ID
        """
        msg = (f"密码重置 | username={username} | status={status} | method={method} | "
               f"message={message} | session_id={session_id}")
        log_level = logging.INFO if status == 'success' else logging.ERROR
        self.logger.log(log_level, msg)
    
    def log_account_unlock(self, username: str, status: str, message: str = '', 
                          session_id: str = '') -> None:
        """
        记录账号解锁操作
        
        Args:
            username: 用户名
            status: 状态（success/failure）
            message: 详细信息
            session_id: 会话ID
        """
        msg = (f"账号解锁 | username={username} | status={status} | "
               f"message={message} | session_id={session_id}")
        log_level = logging.INFO if status == 'success' else logging.ERROR
        self.logger.log(log_level, msg)
    
    def log_auth_failure(self, username: str, reason: str, method: str = 'direct',
                        session_id: str = '') -> None:
        """
        记录认证失败
        
        Args:
            username: 用户名
            reason: 失败原因（如：invalid_credentials, account_locked等）
            method: 认证方法
            session_id: 会话ID
        """
        msg = (f"认证失败 | username={username} | reason={reason} | method={method} | "
               f"session_id={session_id}")
        self.logger.warning(msg)
    
    def log_ldap_operation(self, operation: str, username: str, status: str, 
                          details: str = '', session_id: str = '') -> None:
        """
        记录LDAP操作
        
        Args:
            operation: 操作类型（authenticate/reset_password/unlock等）
            username: 用户名
            status: 状态
            details: 详细信息
            session_id: 会话ID
        """
        msg = (f"LDAP操作 | operation={operation} | username={username} | "
               f"status={status} | details={details} | session_id={session_id}")
        log_level = logging.INFO if status == 'success' else logging.ERROR
        self.logger.log(log_level, msg)
    
    def log_validation_error(self, field: str, reason: str, session_id: str = '') -> None:
        """
        记录验证错误
        
        Args:
            field: 字段名
            reason: 错误原因
            session_id: 会话ID
        """
        msg = f"验证错误 | field={field} | reason={reason} | session_id={session_id}"
        self.logger.warning(msg)
    
    def log_exception(self, exception: Exception, context: str = '', 
                     session_id: str = '') -> None:
        """
        记录异常
        
        Args:
            exception: 异常对象
            context: 上下文信息
            session_id: 会话ID
        """
        msg = f"异常捕获 | context={context} | session_id={session_id}"
        self.logger.exception(msg)
    
    def log_security_event(self, event_type: str, details: str, 
                          session_id: str = '', **extra) -> None:
        """
        记录安全事件（限流、会话劫持、CSRF攻击等）
        
        Args:
            event_type: 事件类型（rate_limit_hit, csrf_attack, session_hijack等）
            details: 详细信息
            session_id: 会话ID
            **extra: 额外信息（client_ip, user_agent等）
        """
        extra_info = ' | '.join(f"{k}={v}" for k, v in extra.items())
        msg = (f"安全事件 | type={event_type} | details={details} | "
               f"session_id={session_id}")
        if extra_info:
            msg += f" | {extra_info}"
        
        # 使用CRITICAL级别便于安全告警
        self.logger.critical(msg)
    
    def log_rate_limit_hit(self, identifier: str, limiter_type: str, 
                          wait_seconds: int, session_id: str = '', **extra) -> None:
        """
        记录限流触发事件
        
        Args:
            identifier: 限流标识（IP或用户名）
            limiter_type: 限流器类型（ip/user/oauth）
            wait_seconds: 需等待秒数
            session_id: 会话ID
            **extra: 额外信息
        """
        extra_info = ' | '.join(f"{k}={v}" for k, v in extra.items())
        msg = (f"限流触发 | identifier={identifier} | type={limiter_type} | "
               f"wait={wait_seconds}s | session_id={session_id}")
        if extra_info:
            msg += f" | {extra_info}"
        
        self.logger.warning(msg)
    
    def log_password_change_attempt(self, username: str, success: bool, 
                                   method: str = 'direct', error_code: str = '',
                                   session_id: str = '', **extra) -> None:
        """
        记录密码修改尝试（成功或失败）
        
        Args:
            username: 用户名
            success: 是否成功
            method: 修改方法（direct/oauth）
            error_code: 错误代码（失败时）
            session_id: 会话ID
            **extra: 额外信息（client_ip, duration_ms等）
        """
        status = 'success' if success else 'failure'
        client_ip = extra.get('client_ip', 'unknown')
        duration_ms = extra.get('duration_ms', 0)
        
        msg = (f"密码修改尝试 | username={username} | status={status} | method={method} | "
               f"ip={client_ip} | duration={duration_ms}ms | session_id={session_id}")
        
        if not success and error_code:
            msg += f" | error_code={error_code}"
        
        log_level = logging.INFO if success else logging.WARNING
        self.logger.log(log_level, msg)


# 全局审计日志单例
_audit_logger = AuditLogger('audit')


def get_audit_logger() -> AuditLogger:
    """获取全局审计日志实例"""
    return _audit_logger
