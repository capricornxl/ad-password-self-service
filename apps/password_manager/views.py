# -*- coding: utf-8 -*-
"""
密码管理视图
"""
import json
import urllib.parse as url_encode
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from utils.config import get_config
from utils.oauth import get_oauth_factory
from utils.logger_factory import get_logger
from utils.audit_logger import get_audit_logger
from utils.format_username import format2username, get_user_is_active, get_user_identifier
from utils.password_validator import get_password_validator
from apps.password_manager.response_handler import ResponseBuilder, SessionManager
from utils.sms import SMSFactory, SMSCodeManager, MobileResolver
from utils.sms.errors import SMSException
from utils.ldap.factory import LDAPFactory
from utils.ldap.errors import LDAPException, LDAPErrorCode

# 获取日志对象
logger = get_logger(__name__)
audit_logger = get_audit_logger()

# 获取配置
config = get_config()
oauth_factory = get_oauth_factory()
provider = oauth_factory.get_current_provider()
password_validator = get_password_validator()

msg_template = 'messages.html'


@require_GET
def healthz(request: HttpRequest) -> JsonResponse:
    """
    健康检查接口 - 用于容器心跳检测
    
    GET /healthz
    
    轻量级检测，仅验证 Django 服务已启动并能够处理请求。
    不检测外部依赖（LDAP、缓存等），确保快速响应。
    
    Returns:
        JsonResponse: {"status": "ok"}
    """
    return JsonResponse({"status": "ok"}, status=200)


def _get_home_url(request: HttpRequest) -> str:
    """从请求获取主页URL"""
    home_url = config.get('oauth.home_url', 'localhost')
    # 提取域名问题
    home_domain = home_url.split('//')[-1].split('/')[0]
    return f"{request.scheme}://{home_domain}"


def _get_session_id(request: HttpRequest) -> str:
    """获取会话ID用于日志追踪"""
    return request.session.session_key or 'unknown'


def _is_mobile_client(request: HttpRequest) -> bool:
    """
    检测是否为移动端客户端（钉钉/企业微信内置浏览器）
    
    Args:
        request: Django请求对象
        
    Returns:
        是否为移动端
    """
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_keywords = ['dingtalk', 'wxwork', 'micromessenger', 'mobile', 'android', 'iphone']
    return any(keyword in user_agent for keyword in mobile_keywords)


def index(request: HttpRequest) -> HttpResponse:
    """
    首页 - 用户自行修改密码
    
    支持直接输入用户名、旧密码、新密码进行修改
    支持可配置的自动跳转行为
    """
    # GET: 渲染页面
    # 检查是否需要自动跳转到OAuth认证
    landing_page = config.get('app.landing_page', 'index')
    auto_redirect_mobile = config.get('app.auto_redirect_in_mobile', True)
    
    # 如果配置为直接跳转到auth页面
    if landing_page == 'auth':
        logger.debug("配置为自动跳转到OAuth认证页面")
        return redirect('/auth')
    
    # 如果是移动端且配置为自动跳转
    if auto_redirect_mobile and _is_mobile_client(request):
        logger.debug("检测到移动端访问，自动跳转到OAuth认证页面")
        return redirect('/auth')
    
    # 否则显示手动输入页面
    # 获取密码规则配置
    policy = password_validator.policy
    password_rules = {
        'min_length': policy.min_length,
        'max_length': policy.max_length,
        'require_uppercase': policy.require_uppercase,
        'require_lowercase': policy.require_lowercase,
        'require_digits': policy.require_digits,
        'require_special_chars': policy.require_special_chars,
    }
    
    context = {
        'global_title': config.get('app.title', 'Self-Service'),
        'scan_app': provider.provider_name,
        'home_url': _get_home_url(request),
        'password_rules': password_rules,
    }
    return render(request, 'index.html', context)


def auth(request: HttpRequest) -> HttpResponse:
    """
    OAuth授权入口
    
    支持两种模式：
    1. GET 渲染授权页面（自动跳转到OAuth提供商）
    2. GET 处理OAuth回调（code参数）
    """
    session_id = _get_session_id(request)
    
    if request.method == 'GET':
        code = request.GET.get('code')
        username = request.GET.get('username')
        
        # 检查是否已有有效的会话认证
        if username and code and SessionManager.verify_auth_code(request, username, code):
            logger.debug(f"[{session_id}] 使用现有会话认证: {username}")
            context = {
                'global_title': config.get('app.title', 'Self-Service'),
                'username': username,
                'code': code,
                'enable_sms_verification': config.get('sms.enabled', False),
            }
            return render(request, 'reset_password.html', context)
        
        # 否则渲染授权页面
        home_url = _get_home_url(request)
        redirect_url_prefix = config.get('oauth.redirect_url_prefix', '/resetPassword')
        # 不要对完整URL编码，只保留原始URL
        # 飞书要求 redirect_uri 与后台配置完全匹配
        redirect_url = f"{home_url}{redirect_url_prefix}"
        
        # 获取OAuth配置
        oauth_config = provider.get_auth_config(home_url, redirect_url)
        
        context = {
            'global_title': config.get('app.title', 'Self-Service'),
            'provider_type': provider.provider_type,
            'provider_name': provider.provider_name,
            'oauth_config': oauth_config,
            'oauth_config_json': json.dumps(oauth_config, ensure_ascii=False),
        }
        logger.debug(f"[{session_id}] 渲染{provider.provider_name}授权页面")
        return render(request, 'auth.html', context)
    
    else:
        logger.error(f"[{session_id}] auth端点不支持的请求方法: {request.method}")
        context = ResponseBuilder.error("不支持的请求方法")
        return render(request, msg_template, context)


def reset_password(request: HttpRequest) -> HttpResponse:
    """
    重置密码 - OAuth流程
    
    GET: OAuth回调处理 + 展示重置密码表单
    POST 逻辑已迁移至 api_reset_password
    """
    session_id = _get_session_id(request)
    home_url = _get_home_url(request)
    
    if request.method == 'GET':
        code = request.GET.get('code')
        username = request.GET.get('username')
        
        # 如果已有有效认证，直接显示表单
        if username and code and SessionManager.verify_auth_code(request, username, code):
            logger.debug(f"[{session_id}] 显示重置密码表单: {username}")
            context = {
                'global_title': config.get('app.title', 'Self-Service'),
                'username': username,
                'code': code,
                'enable_sms_verification': config.get('sms.enabled', False),
            }
            return render(request, 'reset_password.html', context)
        
        # 否则处理OAuth回调
        if not code:
            logger.error(f"[{session_id}] 未能获取授权码")
            audit_logger.log_oauth_failure(provider.provider_type, 'no_code', session_id)
            context = ResponseBuilder.error(
                message="错误，授权码无效或已过期，请重新认证授权",
                error_code="INVALID_CODE",
                button_click="window.location.href='/auth'",
                button_display="重新认证授权"
            )
            return render(request, msg_template, context)
        
        try:
            user_info = {}
            # 通过OAuth获取用户信息
            logger.debug(f"[{session_id}] 通过OAuth获取用户信息")
            status, user_id, user_info = provider.get_user_detail(code, home_url)
            
            if not status:
                logger.warning(f"[{session_id}] OAuth获取用户信息失败")
                audit_logger.log_oauth_failure(
                    provider.provider_type,
                    f"get_user_detail failed: {user_info}",
                    session_id
                )
                # user_id 此时是错误消息字符串，需要构建正确的上下文
                error_msg = user_id if isinstance(user_id, str) else str(user_id)
                context = ResponseBuilder.error(
                    message=error_msg,
                    error_code="OAUTH_FAILED",
                    button_click="window.location.href='/auth'",
                    button_display="重新认证授权"
                )
                return render(request, msg_template, context)
            
            # 检查用户是否激活
            is_active_status, _ = get_user_is_active(user_info)
            if not is_active_status:
                logger.warning(f"[{session_id}] 用户未激活或已离职")
                context = ResponseBuilder.error(
                    message=f"用户未激活或已离职，用户信息：{user_info}",
                    button_click=f"window.location.href='{home_url}'",
                    button_display="返回主页"
                )
                return render(request, msg_template, context)
            
            # 提取用户标识（使用可配置的字段映射）
            identifier_status, identifier = get_user_identifier(user_info, provider.provider_type)
            if not identifier_status:
                logger.warning(f"[{session_id}] 无法提取用户标识: {identifier}")
                context = ResponseBuilder.error(
                    message=identifier,
                    button_click="window.location.href='/auth'",
                    button_display="重新认证授权"
                )
                return render(request, msg_template, context)
            
            # 格式化用户名
            fmt_status, username = format2username(identifier)
            if not fmt_status:
                logger.warning(f"[{session_id}] 用户名格式化失败: {username}")
                context = ResponseBuilder.error(
                    message=str(username),
                    button_click="window.location.href='/auth'",
                    button_display="重新认证授权"
                )
                return render(request, msg_template, context)
            
            # 验证用户在 LDAP/AD 中是否存在（关键安全检查）
            try:
                ldap_adapter = LDAPFactory.create_adapter()
                # 尝试获取用户信息以验证存在性
                # get_user_dn 返回 (success, user_dn) 元组
                success, user_dn = ldap_adapter.get_user_dn(username)
                if not success or not user_dn:
                    logger.warning(f"[{session_id}] 用户在LDAP/AD中不存在: {username}")
                    audit_logger.log_security_event(
                        event_type='ldap_user_not_found',
                        details=f'OAuth认证成功但用户在LDAP/AD中不存在: {username}',
                        session_id=session_id
                    )
                    context = ResponseBuilder.error(
                        message=f"账号 [{username}] 在系统中不存在，请联系管理员确认账号状态",
                        error_code="ACCOUNT_NOT_FOUND",
                        button_click="window.location.href='/auth'",
                        button_display="重新认证授权"
                    )
                    return render(request, msg_template, context)
                logger.debug(f"[{session_id}] 用户在LDAP/AD中存在: {username}, DN={user_dn}")
            except LDAPException as e:
                if e.code == LDAPErrorCode.ACCOUNT_NOT_FOUND:
                    logger.warning(f"[{session_id}] 用户在LDAP/AD中不存在: {username}")
                    audit_logger.log_security_event(
                        event_type='ldap_user_not_found',
                        details=f'OAuth认证成功但用户在LDAP/AD中不存在: {username}',
                        session_id=session_id
                    )
                    context = ResponseBuilder.error(
                        message=f"账号 [{username}] 在系统中不存在，请联系管理员确认账号状态",
                        error_code="ACCOUNT_NOT_FOUND",
                        button_click="window.location.href='/auth'",
                        button_display="重新认证授权"
                    )
                    return render(request, msg_template, context)
                else:
                    logger.error(f"[{session_id}] LDAP查询失败: {e.get_log_message()}")
                    context = ResponseBuilder.error(
                        message=f"系统验证失败，请稍后重试",
                        error_code=str(e.code),
                        button_click="window.location.href='/auth'",
                        button_display="重新认证授权"
                    )
                    return render(request, msg_template, context)
            
            # 提取OAuth用户ID（用于身份绑定）
            oauth_id = user_info.get('userid') or user_info.get('UserId') or user_info.get('user_id', '')
            
            # 绑定OAuth认证身份（新的安全方式）
            SessionManager.bind_oauth_identity(
                request, 
                username=username, 
                code=code, 
                oauth_id=oauth_id,
                user_info=user_info
            )
            # 存储OAuth用户信息（用于SMS手机号解析，保持向后兼容）
            SessionManager.store_oauth_user_info(request, username, user_info)
            
            logger.info(f"[{session_id}] OAuth认证成功: {username} (oauth_id={oauth_id})")
            audit_logger.log_oauth_success(
                provider.provider_type,
                user_id,
                user_info,
                session_id
            )
            
            context = {
                'global_title': config.get('app.title', 'Self-Service'),
                'username': username,
                'code': code,
                'enable_sms_verification': config.get('sms.enabled', False),
            }
            return render(request, 'reset_password.html', context)
            
        except Exception as e:
            logger.exception(f"[{session_id}] OAuth处理异常: {str(e)}")
            audit_logger.log_exception(e, "OAuth get_user_detail", session_id)
            context = ResponseBuilder.error(
                message=f"处理失败: {str(e)}",
                error_code="OAUTH_ERROR",
                button_click=f"window.location.href='{home_url}'",
                button_display="返回主页"
            )
            return render(request, msg_template, context)
    
    else:
        logger.error(f"[{session_id}] 不支持的请求方法: {request.method}")
        context = ResponseBuilder.error("不支持的请求方法")
        return render(request, msg_template, context)


def unlock_account(request: HttpRequest) -> HttpResponse:
    """
    解锁账号 - OAuth流程
    
    GET: 展示解锁确认表单
    POST 逻辑已迁移至 api_unlock_account
    """
    session_id = _get_session_id(request)
    home_url = _get_home_url(request)
    
    if request.method == 'GET':
        code = request.GET.get('code')
        username = request.GET.get('username')
        
        if not (code and username and SessionManager.verify_auth_code(request, username, code)):
            logger.warning(f"[{session_id}] 解锁账号：会话验证失败")
            context = ResponseBuilder.error(
                message="会话已过期，请重新认证",
                error_code="SESSION_EXPIRED",
                button_click="window.location.href='/auth'",
                button_display="重新认证授权"
            )
            return render(request, msg_template, context)
        
        logger.debug(f"[{session_id}] 显示解锁账号表单: {username}")
        context = {
            'global_title': config.get('app.title', 'Self-Service'),
            'username': username,
            'code': code,
            'enable_sms_verification': config.get('sms.enabled', False),
        }
        return render(request, 'unlock.html', context)
    
    else:
        logger.error(f"[{session_id}] 不支持的请求方法: {request.method}")
        context = ResponseBuilder.error("不支持的请求方法")
        return render(request, msg_template, context)


def messages(request: HttpRequest) -> HttpResponse:
    """
    消息页面 - 显示操作结果
    """
    msg = request.GET.get('msg', '')
    button_click = request.GET.get('button_click', "window.location.href='/'")
    button_display = request.GET.get('button_display', '返回首页')
    
    context = {
        'global_title': config.get('app.title', 'Self-Service'),
        'msg': msg,
        'button_click': button_click,
        'button_display': button_display
    }
    return render(request, msg_template, context)


def send_sms_code(request: HttpRequest) -> HttpResponse:
    """
    发送短信验证码 API
    
    请求方式：POST
    请求参数：
        - username: 用户名（必需）
        - code: OAuth授权码（可选，OAuth流程需要）
    
    返回：JSON格式
        - success: 是否成功
        - message: 提示消息
        - mobile: 手机号（脱敏）
        - wait_seconds: 需要等待的秒数（限流时）
    """
    session_id = _get_session_id(request)
    
    if request.method != 'POST':
        return ResponseBuilder.json_error("不支持的请求方法")
    
    try:
        # 获取参数
        username = request.POST.get('username', '').strip()
        oauth_code = request.POST.get('code', '').strip()
        
        if not username:
            logger.warning(f"[{session_id}] 发送验证码缺少用户名")
            return ResponseBuilder.json_error("缺少用户名参数")
        
        # 格式化用户名
        fmt_status, formatted_username = format2username(username)
        if not fmt_status:
            logger.warning(f"[{session_id}] 用户名格式化失败: {username}")
            return ResponseBuilder.json_error(f"用户名格式不正确: {formatted_username}")
        
        username = formatted_username
        logger.info(f"[{session_id}] 请求发送验证码: {username}")
        
        # 如果提供了 OAuth code，验证认证状态
        if oauth_code:
            if not SessionManager.verify_auth_code(request, username, oauth_code):
                logger.warning(f"[{session_id}] OAuth 认证已失效: {username}")
                return ResponseBuilder.json_error(
                    message="认证已过期，请重新授权",
                    error_code="AUTH_EXPIRED"
                )
        
        # 初始化SMS组件
        mobile_resolver = MobileResolver()
        code_manager = SMSCodeManager()
        
        # 获取OAuth用户信息（如果在OAuth流程中）
        oauth_user_info = None
        if oauth_code:
            # 从会话中获取OAuth用户信息
            oauth_user_info = SessionManager.get_oauth_user_info(request, username)
        
        # 解析手机号
        try:
            success, mobile, source = mobile_resolver.resolve_mobile(username, oauth_user_info)
            logger.info(f"[{session_id}] 手机号解析成功: {username}, source={source}")
        except SMSException as e:
            logger.warning(f"[{session_id}] 手机号解析失败: {e.get_log_message()}")
            audit_logger.log_security_event(
                event_type='sms_mobile_resolve_failed',
                details=f'username={username}, error={e.get_user_message()}',
                session_id=session_id
            )
            return ResponseBuilder.json_error(e.get_user_message())
        
        # 检查发送限流
        is_limited, wait_seconds = code_manager.is_send_rate_limited(mobile)
        if is_limited:
            logger.warning(f"[{session_id}] 发送频率受限: {mobile[:3]}****{mobile[-4:]}, 等待{wait_seconds}秒")
            audit_logger.log_rate_limit_hit(
                identifier=username,
                limiter_type='sms_send',
                wait_seconds=wait_seconds,
                session_id=session_id
            )
            return ResponseBuilder.json_error(
                message=f"发送过于频繁，请{wait_seconds}秒后再试",
                data={'wait_seconds': wait_seconds}
            )
        
        # 检查每日发送次数限制
        is_daily_limited, daily_count = code_manager.is_daily_limit_reached(mobile)
        if is_daily_limited:
            logger.warning(f"[{session_id}] 达到每日发送上限: {mobile[:3]}****{mobile[-4:]}, 次数={daily_count}")
            audit_logger.log_rate_limit_hit(
                identifier=username,
                limiter_type='sms_daily_limit',
                wait_seconds=0,
                session_id=session_id
            )
            return ResponseBuilder.json_error("今日发送次数已达上限，请明天再试")
        
        # 生成验证码
        verification_code = code_manager.generate_code()
        
        # 获取SMS提供商并发送
        try:
            sms_provider = SMSFactory.get_current_provider()
            send_success, send_message = sms_provider.send_verification_code(
                mobile=mobile,
                code=verification_code
            )
            
            if not send_success:
                logger.error(f"[{session_id}] 短信发送失败: {send_message}")
                audit_logger.log_security_event(
                    event_type='sms_send_failed',
                    details=f'username={username}, mobile={mobile[:3]}****{mobile[-4:]}, error={send_message}',
                    session_id=session_id
                )
                return ResponseBuilder.json_error(f"验证码发送失败: {send_message}")
            
            # 发送成功，存储验证码和记录发送行为
            code_manager.store_code(mobile, verification_code, username)
            code_manager.record_send(mobile)
            
            # 存储完整手机号到会话（用于后续验证码验证）
            SessionManager.store_sms_mobile(request, username, mobile)
            
            logger.info(f"[{session_id}] 验证码发送成功: {username}, mobile={mobile[:3]}****{mobile[-4:]}")
            audit_logger.log_security_event(
                event_type='sms_send_success',
                details=f'username={username}, mobile={mobile[:3]}****{mobile[-4:]}, provider={config.get("sms.provider")}',
                session_id=session_id
            )
            
            # 返回成功响应
            return ResponseBuilder.json_success(
                message="验证码已发送，请查收短信",
                data={
                    'mobile': f"{mobile[:3]}****{mobile[-4:]}",
                    'expire_seconds': config.get('sms.code.expire_seconds', 300)
                }
            )
            
        except SMSException as e:
            logger.error(f"[{session_id}] SMS异常: {e.get_log_message()}")
            audit_logger.log_exception(e, f"send_sms_code username={username}", session_id)
            return ResponseBuilder.json_error(e.get_user_message())
        
    except Exception as e:
        logger.exception(f"[{session_id}] 发送验证码异常: {str(e)}")
        audit_logger.log_exception(e, "send_sms_code", session_id)
        return ResponseBuilder.json_error("系统错误，请稍后重试")


def verify_sms_code(request: HttpRequest) -> HttpResponse:
    """
    验证短信验证码 API
    
    请求方式：POST
    请求参数：
        - username: 用户名（必需）
        - mobile: 手机号（必需）
        - sms_code: 短信验证码（必需）
    
    返回：JSON格式
        - success: 是否成功
        - message: 提示消息
        - username: 关联的用户名
    """
    session_id = _get_session_id(request)
    
    if request.method != 'POST':
        return ResponseBuilder.json_error("不支持的请求方法")
    
    try:
        # 获取参数
        username = request.POST.get('username', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        sms_code = request.POST.get('sms_code', '').strip()
        
        # 添加详细日志记录请求参数
        logger.debug(f"[{session_id}] SMS验证请求参数: username={username}, mobile={mobile}, sms_code={sms_code}")
        logger.debug(f"[{session_id}] 所有POST参数: {dict(request.POST)}")
        
        if not all([username, mobile, sms_code]):
            logger.warning(f"[{session_id}] 验证码验证缺少必需参数")
            return ResponseBuilder.json_error("缺少必需参数")
        
        # 格式化用户名
        fmt_status, formatted_username = format2username(username)
        if not fmt_status:
            return ResponseBuilder.json_error(f"用户名格式不正确: {formatted_username}")
        
        username = formatted_username
        logger.info(f"[{session_id}] 请求验证验证码: {username}")
        
        # 如果传入的是脱敏手机号（包含****），从会话获取完整手机号
        if '****' in mobile:
            stored_mobile = SessionManager.get_sms_mobile(request, username)
            if stored_mobile:
                logger.debug(f"[{session_id}] 使用会话中存储的完整手机号进行验证")
                mobile = stored_mobile
            else:
                logger.warning(f"[{session_id}] 无法获取完整手机号: username={username}")
                return ResponseBuilder.json_error("会话已过期，请重新获取验证码")
        
        # 初始化验证码管理器
        code_manager = SMSCodeManager()
        
        # 验证验证码
        try:
            verify_success, verify_message, stored_username = code_manager.verify_code(
                mobile, sms_code
            )
            
            # 验证成功
            logger.info(f"[{session_id}] 验证码验证成功: {username}, mobile={mobile[:3]}****{mobile[-4:]}")
            audit_logger.log_security_event(
                event_type='sms_verify_success',
                details=f'username={username}, mobile={mobile[:3]}****{mobile[-4:]}',
                session_id=session_id
            )
            
            # 建立验证会话（用于后续的密码重置）
            SessionManager.store_sms_verification(request, username, mobile)
            
            return ResponseBuilder.json_success(
                message="验证成功",
                data={
                    'username': username,
                    'verified': True
                }
            )
            
        except SMSException as e:
            logger.warning(f"[{session_id}] 验证码验证失败: {e.get_log_message()}")
            audit_logger.log_security_event(
                event_type='sms_verify_failed',
                details=f'username={username}, mobile={mobile[:3]}****{mobile[-4:]}, error={e.error_code.value}',
                session_id=session_id
            )
            return ResponseBuilder.json_error(e.get_user_message())
        
    except Exception as e:
        logger.exception(f"[{session_id}] 验证验证码异常: {str(e)}")
        audit_logger.log_exception(e, "verify_sms_code", session_id)
        return ResponseBuilder.json_error("系统错误，请稍后重试")
