# -*- coding: utf-8 -*-
"""
密码管理 API 接口
"""
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from utils.config import get_config
from utils.logger_factory import get_logger
from utils.audit_logger import get_audit_logger
from utils.ldap.factory import LDAPFactory
from utils.ldap.errors import LDAPException, LDAPErrorCode
from utils.format_username import format2username
from utils.password_validator import get_password_validator
from apps.password_manager.response_handler import ResponseBuilder, SessionManager
from apps.password_manager.form import CheckForm
from utils.rate_limiter import RateLimiter

# 获取日志对象
logger = get_logger(__name__)
audit_logger = get_audit_logger()

# 获取配置
config = get_config()
password_validator = get_password_validator()


def _get_session_id(request: HttpRequest) -> str:
    """获取会话ID用于日志追踪"""
    return request.session.session_key or 'unknown'


def _get_ldap_adapter():
    """
    获取LDAP适配器实例
    
    Returns:
        LDAPAdapter实例
        
    Raises:
        LDAPException: 创建适配器失败
    """
    try:
        return LDAPFactory.create_adapter()
    except Exception as e:
        logger.error(f"创建LDAP适配器失败: {e}")
        raise LDAPException(
            LDAPErrorCode.CONFIGURATION_ERROR,
            f"LDAP适配器创建失败: {str(e)}",
            'factory',
            e
        )


@require_POST
def api_change_password(request: HttpRequest) -> JsonResponse:
    """
    直接密码修改 API
    POST /api/password/change
    
    参数：
    - username: 用户名
    - old_password: 旧密码
    - new_password: 新密码
    - confirm_password: 确认密码
    
    返回：JsonResponse
    """
    session_id = _get_session_id(request)
    
    # 第一步：表单验证
    check_form = CheckForm(request.POST)
    if not check_form.is_valid():
        logger.warning(f"[{session_id}] 表单验证失败: {check_form.errors}")
        audit_logger.log_validation_error('form', str(check_form.errors), session_id)
        return ResponseBuilder.json_error(
            message=str(check_form.errors),
            error_code="FORM_VALIDATION_ERROR"
        )
    
    form_data = check_form.cleaned_data
    username = form_data.get("username")
    old_password = form_data.get("old_password")
    new_password = form_data.get("new_password")
    
    logger.info(f"[{session_id}] 用户 {username} 请求直接修改密码")
    
    # 第二步：格式化用户名
    is_valid, formatted_username = format2username(username)
    if not is_valid:
        logger.warning(f"[{session_id}] 用户名格式化失败: {formatted_username}")
        audit_logger.log_validation_error('username_format', str(formatted_username), session_id)
        return ResponseBuilder.json_error(
            message=str(formatted_username),
            error_code="USERNAME_FORMAT_ERROR"
        )
    
    username = formatted_username
    
    # 第三步：验证新密码格式
    is_valid, error_msg = password_validator.validate(new_password)
    if not is_valid:
        logger.warning(f"[{session_id}] 新密码不符合策略: {username}")
        audit_logger.log_validation_error('password', error_msg, session_id)
        return ResponseBuilder.json_error(
            message=error_msg,
            error_code="PASSWORD_VALIDATION_ERROR"
        )
    
    # 第四步：检查账号状态（使用管理员连接）
    try:
        adapter = _get_ldap_adapter()
        
        # 检查账号是否禁用
        _, is_disabled = adapter.is_account_disabled(username)
        if is_disabled:
            logger.error(f"[{session_id}] 账号已禁用: {username}")
            audit_logger.log_password_reset(username, 'failure', 'account_disabled', 'direct', session_id)
            return ResponseBuilder.json_error(
                message="此账号已禁用，请联系HR确认账号状态",
                error_code="ACCOUNT_DISABLED"
            )
    except LDAPException as e:
        if e.code == LDAPErrorCode.ACCOUNT_NOT_FOUND:
            logger.error(f"[{session_id}] 账号不存在: {username}")
            audit_logger.log_password_reset(username, 'failure', 'account_not_found', 'direct', session_id)
            return ResponseBuilder.json_error(
                message=f"账号 [{username}] 不存在，请确认账号是否正确",
                error_code="ACCOUNT_NOT_FOUND"
            )
        else:
            logger.error(f"[{session_id}] 账号状态检查失败: {e.get_log_message()}")
            return ResponseBuilder.json_error(
                message="账号验证失败，无法修改密码",
                error_code=str(e.code)
            )
    
    # 第五步：执行密码修改（使用用户自己的连接）
    try:
        # 使用 change_password 方法，该方法会：
        # 1. 使用用户凭据建立连接（验证旧密码）
        # 2. 使用用户连接修改密码
        adapter.change_password(username, old_password, new_password)
        
        logger.info(f"[{session_id}] 用户 {username} 密码修改成功")
        audit_logger.log_password_reset(username, 'success', 'Password changed by user', 'direct', session_id)
        
        return ResponseBuilder.json_success(
            message="密码已修改成功，请妥善保管"
        )
    
    except LDAPException as e:
        logger.error(f"[{session_id}] 密码修改失败: {e.get_log_message()}")
        audit_logger.log_password_reset(username, 'failure', str(e.code), 'direct', session_id)
        return ResponseBuilder.json_error(
            message=f"密码修改失败: {e.get_user_message()}",
            error_code=str(e.code)
        )
    
    except Exception as e:
        logger.exception(f"[{session_id}] 密码修改未预期错误: {str(e)}")
        audit_logger.log_password_reset(username, 'failure', 'unexpected_error', 'direct', session_id)
        return ResponseBuilder.json_error(
            message="系统错误，请稍后重试",
            error_code="SYSTEM_ERROR"
        )


@require_POST
def api_reset_password(request: HttpRequest) -> JsonResponse:
    """
    OAuth 密码重置 API
    POST /api/password/reset
    
    参数：
    - username: 用户名
    - code: OAuth 授权码
    - new_password: 新密码
    - confirm_password: 确认密码
    - sms_code: 短信验证码（可选）
    
    返回：JsonResponse
    """
    session_id = _get_session_id(request)
    
    username = request.POST.get('username', '').strip()
    code = request.POST.get('code', '').strip()
    new_password = request.POST.get('new_password', '').strip()
    sms_code = request.POST.get('sms_code', '').strip()
    
    # 参数完整性验证
    if not all([username, code, new_password]):
        logger.warning(f"[{session_id}] 参数缺失或为空")
        return ResponseBuilder.json_error(
            message="参数不完整，请重试",
            error_code="INVALID_PARAMS"
        )
    
    # Rate Limiting：防止暴力破解
    if config.get('security.rate_limiting.enabled', True):
        rate_limiter = RateLimiter()
        client_ip = SessionManager.get_client_ip(request)
        rate_key = f"password_reset:{client_ip}:{username}"
        allowed, remaining, wait_seconds = rate_limiter.check_rate_limit(
            rate_key, 
            max_attempts=config.get('security.rate_limiting.default_max_attempts.max_attempts', 5),
            window_seconds=config.get('security.rate_limiting.default_max_attempts.window_seconds', 300)
        )
        
        if not allowed:
            logger.warning(f"[{session_id}] 密码重置频率限制: {username}, IP={client_ip}, 需等待{wait_seconds}秒")
            audit_logger.log_security_event(
                event_type='password_reset_rate_limit',
                details=f'用户{username}密码重置过于频繁，IP={client_ip}',
                session_id=session_id
            )
            return ResponseBuilder.json_error(
                message=f"操作过于频繁，请在 {wait_seconds} 秒后重试",
                error_code="RATE_LIMIT_EXCEEDED",
                data={'wait_seconds': wait_seconds}
            )
    
    # 格式化用户名
    is_valid, formatted_username = format2username(username)
    if not is_valid:
        logger.warning(f"[{session_id}] 用户名格式化失败: {username}")
        return ResponseBuilder.json_error(
            message=str(formatted_username),
            error_code="USERNAME_FORMAT_ERROR"
        )
    username = formatted_username
    
    # 关键：验证身份一致性（防止越权攻击）
    if not SessionManager.verify_identity(request, username):
        logger.error(f"[{session_id}] 越权操作尝试: username={username}")
        audit_logger.log_security_event(
            event_type='unauthorized_password_reset_attempt',
            details=f'用户尝试修改他人密码：请求username={username}',
            session_id=session_id
        )
        return ResponseBuilder.json_error(
            message="无权操作，认证信息不匹配",
            error_code="UNAUTHORIZED"
        )
    
    # 如果启用了SMS验证，需要先验证SMS
    if config.get('sms.enabled', False):
        # 检查会话中的SMS验证状态（前端应先调用 /api/sms/verify 接口完成验证）
        if not SessionManager.verify_sms_verification(request, username):
            logger.warning(f"[{session_id}] SMS验证未通过: {username}")
            return ResponseBuilder.json_error(
                message="请先完成短信验证",
                error_code="SMS_NOT_VERIFIED"
            )
    
    # 验证新密码格式
    is_valid, error_msg = password_validator.validate(new_password)
    if not is_valid:
        logger.warning(f"[{session_id}] 新密码不符合策略: {username}")
        audit_logger.log_validation_error('password', error_msg, session_id)
        return ResponseBuilder.json_error(
            message=error_msg,
            error_code="PASSWORD_VALIDATION_ERROR"
        )
    
    # 验证会话并执行密码重置
    try:
        logger.info(f"[{session_id}] 用户 {username} 通过OAuth重置密码")
        adapter = _get_ldap_adapter()
        
        # 检查账号状态
        try:
            _, is_disabled = adapter.is_account_disabled(username)
            if is_disabled:
                logger.error(f"[{session_id}] 账号已禁用: {username}")
                audit_logger.log_password_reset(username, 'failure', 'account_disabled', 'oauth', session_id)
                return ResponseBuilder.json_error(
                    message="此账号已禁用，请联系HR确认账号状态",
                    error_code="ACCOUNT_DISABLED"
                )
        except LDAPException as e:
            if e.code == LDAPErrorCode.ACCOUNT_NOT_FOUND:
                logger.error(f"[{session_id}] 账号不存在: {username}")
                audit_logger.log_password_reset(username, 'failure', 'account_not_found', 'oauth', session_id)
                return ResponseBuilder.json_error(
                    message=f"账号 [{username}] 不存在，请确认账号是否正确",
                    error_code="ACCOUNT_NOT_FOUND"
                )
            else:
                logger.error(f"[{session_id}] 账号状态检查失败: {e.get_log_message()}")
                return ResponseBuilder.json_error(
                    message="账号验证失败，无法重置密码",
                    error_code=str(e.code)
                )
        
        # 执行密码重置
        adapter.reset_password(username, new_password)
        
        # 密码重置成功后，尝试解锁账号
        unlock_success = True
        try:
            adapter.unlock_account(username)
            logger.info(f"[{session_id}] 密码重置并解锁成功: {username}")
        except LDAPException as unlock_err:
            unlock_success = False
            logger.warning(f"[{session_id}] 密码重置成功但解锁失败: {unlock_err.get_log_message()}")
        
        audit_logger.log_password_reset(
            username, 'success',
            'Password reset via OAuth',
            'oauth', session_id
        )
        
        # 根据解锁状态返回不同的提示消息
        if unlock_success:
            return ResponseBuilder.json_success(
                message="密码已修改成功，请妥善保管"
            )
        else:
            return ResponseBuilder.json_success(
                message="密码已修改成功，但账号解锁失败，您的账号可能仍处于锁定状态，请联系管理员处理",
                data={'unlock_failed': True}
            )
        
    except LDAPException as e:
        logger.exception(f"[{session_id}] 密码重置异常: {e.get_log_message()}")
        audit_logger.log_password_reset(username, 'failure', str(e.code), 'oauth', session_id)
        return ResponseBuilder.json_error(
            message=f"重置失败: {e.get_user_message()}",
            error_code=str(e.code)
        )
    except Exception as e:
        logger.exception(f"[{session_id}] 密码重置异常: {str(e)}")
        audit_logger.log_exception(e, f"password reset username={username}", session_id)
        return ResponseBuilder.json_error(
            message=f"重置失败: {str(e)}",
            error_code="INTERNAL_ERROR"
        )


@require_POST
def api_unlock_account(request: HttpRequest) -> JsonResponse:
    """
    账户解锁 API
    POST /api/account/unlock
    
    参数：
    - username: 用户名
    - code: OAuth 授权码
    - sms_code: 短信验证码（可选）
    
    返回：JsonResponse
    """
    session_id = _get_session_id(request)
    
    username = request.POST.get('username', '').strip()
    code = request.POST.get('code', '').strip()
    sms_code = request.POST.get('sms_code', '').strip()
    
    # 参数完整性验证
    if not all([username, code]):
        logger.warning(f"[{session_id}] 解锁账号：参数缺失")
        return ResponseBuilder.json_error(
            message="参数不完整，请重试",
            error_code="INVALID_PARAMS"
        )
    
    # Rate Limiting：防止暴力破解
    if config.get('security.rate_limiting.enabled', True):
        rate_limiter = RateLimiter()
        client_ip = SessionManager.get_client_ip(request)
        rate_key = f"account_unlock:{client_ip}:{username}"
        allowed, remaining, wait_seconds = rate_limiter.check_rate_limit(
            rate_key,
            max_attempts=config.get('security.rate_limiting.default_max_attempts.max_attempts', 5),
            window_seconds=config.get('security.rate_limiting.default_max_attempts.window_seconds', 300)
        )
        
        if not allowed:
            logger.warning(f"[{session_id}] 账号解锁频率限制: {username}, IP={client_ip}, 需等待{wait_seconds}秒")
            audit_logger.log_security_event(
                event_type='account_unlock_rate_limit',
                details=f'用户{username}解锁账号过于频繁，IP={client_ip}',
                session_id=session_id
            )
            return ResponseBuilder.json_error(
                message=f"操作过于频繁，请在 {wait_seconds} 秒后重试",
                error_code="RATE_LIMIT_EXCEEDED",
                data={'wait_seconds': wait_seconds}
            )
    
    # 格式化用户名
    is_valid, formatted_username = format2username(username)
    if not is_valid:
        logger.warning(f"[{session_id}] 用户名格式化失败: {username}")
        return ResponseBuilder.json_error(
            message=str(formatted_username),
            error_code="USERNAME_FORMAT_ERROR"
        )
    username = formatted_username
    
    # 关键：验证身份一致性（防止越权攻击）
    if not SessionManager.verify_identity(request, username):
        logger.error(f"[{session_id}] 越权操作尝试: username={username}")
        audit_logger.log_security_event(
            event_type='unauthorized_unlock_attempt',
            details=f'用户尝试解锁他人账号：请求username={username}',
            session_id=session_id
        )
        return ResponseBuilder.json_error(
            message="无权操作，认证信息不匹配",
            error_code="UNAUTHORIZED"
        )
    
    if not SessionManager.verify_auth_code(request, username, code):
        logger.warning(f"[{session_id}] 解锁账号：会话验证失败")
        return ResponseBuilder.json_error(
            message="会话已过期，请重新认证",
            error_code="SESSION_EXPIRED"
        )
    
    # 如果启用了SMS验证，需要先验证SMS
    if config.get('sms.enabled', False):
        if not SessionManager.verify_sms_verification(request, username):
            logger.warning(f"[{session_id}] SMS验证未通过: {username}")
            return ResponseBuilder.json_error(
                message="短信验证未通过，请先完成短信验证",
                error_code="SMS_NOT_VERIFIED"
            )
    
    try:
        logger.info(f"[{session_id}] 用户 {username} 请求解锁账号")
        adapter = _get_ldap_adapter()
        
        # 执行解锁
        adapter.unlock_account(username)
        
        logger.info(f"[{session_id}] 账号解锁成功: {username}")
        audit_logger.log_account_unlock(username, 'success', '', session_id)
        
        return ResponseBuilder.json_success(
            message="账号已解锁成功"
        )
        
    except LDAPException as e:
        logger.exception(f"[{session_id}] 解锁账号失败: {e.get_log_message()}")
        audit_logger.log_account_unlock(username, 'failure', e.get_log_message(), session_id)
        return ResponseBuilder.json_error(
            message=e.get_user_message(),
            error_code=str(e.code)
        )
    except Exception as e:
        logger.exception(f"[{session_id}] 解锁账号异常: {str(e)}")
        audit_logger.log_exception(e, f"unlock_account username={username}", session_id)
        return ResponseBuilder.json_error(
            message=f"解锁失败: {str(e)}",
            error_code="UNKNOWN_ERROR"
        )


@require_GET
def api_password_rules(request: HttpRequest) -> JsonResponse:
    """
    获取密码验证规则
    GET /api/config/password-rules
    
    返回：JsonResponse 包含密码规则配置
    """
    policy = password_validator.policy
    
    rules = {
        'min_length': policy.min_length,
        'max_length': policy.max_length,
        'require_uppercase': policy.require_uppercase,
        'require_lowercase': policy.require_lowercase,
        'require_digits': policy.require_digits,
        'require_special_chars': policy.require_special_chars,
    }
    
    # 构建密码要求描述
    requirements = []
    if policy.require_uppercase:
        requirements.append("包含大写字母")
    if policy.require_lowercase:
        requirements.append("包含小写字母")
    if policy.require_digits:
        requirements.append("包含数字")
    if policy.require_special_chars:
        requirements.append("包含特殊字符")
    
    rules['requirements'] = requirements
    rules['length_hint'] = f"密码长度需在 {policy.min_length}-{policy.max_length} 个字符之间"
    
    return ResponseBuilder.json_success(
        message="获取密码规则成功",
        data=rules
    )


def api_auth_status(request: HttpRequest) -> JsonResponse:
    """
    检查 OAuth 认证状态
    GET/POST /api/auth/status
    
    参数：
    - username: 用户名
    - code: OAuth 授权码
    
    返回：JsonResponse
    """
    session_id = _get_session_id(request)
    
    username = request.GET.get('username') or request.POST.get('username', '')
    code = request.GET.get('code') or request.POST.get('code', '')
    username = username.strip()
    code = code.strip()
    
    if not username or not code:
        return ResponseBuilder.json_error(
            message="参数不完整",
            error_code="FORM_VALIDATION_ERROR"
        )
    
    if not SessionManager.verify_auth_code(request, username, code):
        logger.info(f"[{session_id}] OAuth 认证已过期: {username}")
        return ResponseBuilder.json_error(
            message="认证已过期，请重新授权",
            error_code="AUTH_EXPIRED"
        )
    
    return ResponseBuilder.json_success(message="认证有效")
