# -*- coding: utf-8 -*-
""" 
响应处理器 - 统一构建API响应和错误处理
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from utils.logger_factory import get_logger
from apps.password_manager.error_codes import ErrorCode, get_error_message
from utils.config import get_config

logger = get_logger(__name__)
config = get_config()


@dataclass
class ApiResponse:
    """API响应数据类"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error_code: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error_code': self.error_code
        }


class ResponseBuilder:
    """
    响应构建器 - 统一构建前端响应上下文
    """
    
    MSG_TEMPLATE = 'messages.html'
    
    @staticmethod
    def build_context(
        message: str,
        button_click: str = "window.location.href='/'",
        button_display: str = "返回首页",
        msg_type: str = "info"
    ) -> Dict[str, Any]:
        """
        构建通用响应上下文
        
        Args:
            message: 提示消息
            button_click: 按钮点击事件
            button_display: 按钮显示文本
            msg_type: 消息类型（info/success/warning/error）
            
        Returns:
            响应上下文字典
        """
        config = get_config()
        return {
            'global_title': config.get('app.title', 'Self-Service'),
            'msg': message,
            'button_click': button_click,
            'button_display': button_display,
            'msg_type': msg_type
        }
    
    @staticmethod
    def success(
        message: str = "操作成功",
        button_click: str = "window.location.href='/'",
        button_display: str = "返回首页",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        构建成功响应
        
        Args:
            message: 成功消息
            button_click: 按钮点击事件
            button_display: 按钮显示文本
            data: 额外数据
            
        Returns:
            响应上下文
        """
        context = ResponseBuilder.build_context(message, button_click, button_display, "success")
        if data:
            context.update(data)
        return context
    
    @staticmethod
    def error(
        message: str = "操作失败",
        button_click: str = "window.location.href='/auth'",
        button_display: str = "重新认证授权",
        error_code: str = "",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        构建错误响应
        
        Args:
            message: 错误消息
            button_click: 按钮点击事件
            button_display: 按钮显示文本
            error_code: 错误代码（支持ErrorCode枚举或字符串）
            data: 额外数据
            
        Returns:
            响应上下文
        """
        # 如果传入的是ErrorCode枚举，自动获取错误消息
        if isinstance(error_code, ErrorCode):
            message = get_error_message(error_code)
            error_code = error_code.value
        elif error_code and not message:
            message = get_error_message(error_code, message)
        
        context = ResponseBuilder.build_context(message, button_click, button_display, "error")
        if error_code:
            context['error_code'] = error_code
        if data:
            context.update(data)
        return context
    
    @staticmethod
    def warning(
        message: str = "警告",
        button_click: str = "window.location.href='/auth'",
        button_display: str = "重新认证授权",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        构建警告响应
        
        Args:
            message: 警告消息
            button_click: 按钮点击事件
            button_display: 按钮显示文本
            data: 额外数据
            
        Returns:
            响应上下文
        """
        context = ResponseBuilder.build_context(message, button_click, button_display, "warning")
        if data:
            context.update(data)
        return context
    
    @staticmethod
    def render_success(
        request: HttpRequest,
        message: str = "操作成功",
        button_click: str = "window.location.href='/'",
        button_display: str = "返回首页"
    ) -> HttpResponse:
        """
        直接渲染成功响应（简化视图代码）
        
        Args:
            request: Django请求对象
            message: 成功消息
            button_click: 按钮点击事件
            button_display: 按钮显示文本
            
        Returns:
            HttpResponse
        """
        context = ResponseBuilder.success(message, button_click, button_display)
        return render(request, ResponseBuilder.MSG_TEMPLATE, context)
    
    @staticmethod
    def render_error(
        request: HttpRequest,
        message: str = "操作失败",
        error_code: str = "",
        button_click: str = "window.location.href='/auth'",
        button_display: str = "重新认证授权"
    ) -> HttpResponse:
        """
        直接渲染错误响应（简化视图代码）
        
        Args:
            request: Django请求对象
            message: 错误消息或ErrorCode枚举
            error_code: 错误代码
            button_click: 按钮点击事件
            button_display: 按钮显示文本
            
        Returns:
            HttpResponse
        """
        context = ResponseBuilder.error(message, button_click, button_display, error_code)
        return render(request, ResponseBuilder.MSG_TEMPLATE, context)
    
    @staticmethod
    def json_success(
        message: str = "操作成功",
        data: Optional[Dict[str, Any]] = None
    ) -> JsonResponse:
        """
        构建JSON成功响应
        
        Args:
            message: 成功消息
            data: 额外数据
            
        Returns:
            JsonResponse
        """
        response_data = {
            'success': True,
            'message': message,
            'data': data or {}
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})
    
    @staticmethod
    def json_error(
        message: str = "操作失败",
        error_code: str = "",
        data: Optional[Dict[str, Any]] = None
    ) -> JsonResponse:
        """
        构建JSON错误响应
        
        Args:
            message: 错误消息
            error_code: 错误代码
            data: 额外数据
            
        Returns:
            JsonResponse
        """
        response_data = {
            'success': False,
            'message': message,
            'error_code': error_code,
            'data': data or {}
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


class ErrorHandler:
    """
    错误处理器 - 统一的异常处理和错误消息映射
    """
    
    # 错误代码映射
    ERROR_MESSAGES = {
        'INVALID_CODE': '授权码无效或已过期',
        'SESSION_EXPIRED': '会话已过期，请重新认证',
        'AUTH_EXPIRED': '认证已过期，请重新授权',
        'INVALID_CREDENTIALS': '账号或密码不正确',
        'ACCOUNT_LOCKED': '账号已被锁定',
        'ACCOUNT_DISABLED': '账号已被禁用',
        'PASSWORD_EXPIRED': '密码已过期',
        'ACCOUNT_NOT_FOUND': '账号不存在',
        'ACCOUNT_EXPIRED': '账号已过期',
        'INVALID_PASSWORD': '密码格式不符合要求',
        'PASSWORD_UNCHANGED': '新旧密码相同',
        'PASSWORD_TOO_SHORT': '密码长度不足',
        'PASSWORD_TOO_LONG': '密码长度超出限制',
        'PASSWORD_WEAK': '密码强度不足',
        'PASSWORD_HISTORY': '密码不能与最近使用过的密码相同',
        'LDAP_CONNECTION_ERROR': 'AD连接失败',
        'LDAP_TIMEOUT_ERROR': 'AD服务器响应超时',
        'LDAP_SSL_ERROR': 'AD安全连接失败',
        'LDAP_BIND_ERROR': 'AD认证失败',
        'LDAP_SEARCH_ERROR': 'AD查询失败',
        'LDAP_MODIFY_ERROR': 'AD修改操作失败',
        'LDAP_INSUFFICIENT_RIGHTS': '权限不足，无法执行操作',
        'LDAP_UNWILLING_TO_PERFORM': '服务器拒绝执行此操作',
        'OAUTH_ERROR': 'OAuth认证失败',
        'INTERNAL_ERROR': '系统内部错误',
        'RATE_LIMIT_EXCEEDED': '操作过于频繁，请稍后重试',
        'SMS_SEND_FAILED': '短信发送失败',
        'SMS_VERIFY_FAILED': '短信验证失败',
    }
    
    @staticmethod
    def get_error_message(error_code: str, default_message: str = "") -> str:
        """
        获取错误消息
        
        Args:
            error_code: 错误代码
            default_message: 默认错误消息
            
        Returns:
            错误消息
        """
        return ErrorHandler.ERROR_MESSAGES.get(
            error_code,
            default_message or "发生未知错误，请稍后重试"
        )
    
    @staticmethod
    def handle_ldap_error(error_code: str, message: str = "") -> Dict[str, str]:
        """
        处理LDAP错误
        
        Args:
            error_code: LDAP错误代码
            message: 原始错误消息
            
        Returns:
            统一的错误消息字典
        """
        # AD 错误码映射 (Windows LDAP error codes)
        error_mapping = {
            # 认证相关错误
            '52e': 'INVALID_CREDENTIALS',     # 用户名或密码错误
            '525': 'ACCOUNT_NOT_FOUND',       # 用户不存在
            '530': 'ACCOUNT_NOT_FOUND',       # 不允许在此时间登录
            '531': 'ACCOUNT_NOT_FOUND',       # 不允许在此工作站登录
            '532': 'PASSWORD_EXPIRED',        # 密码已过期
            '533': 'ACCOUNT_DISABLED',        # 账号已禁用
            '701': 'ACCOUNT_EXPIRED',         # 账号已过期
            '773': 'PASSWORD_EXPIRED',        # 用户必须在下次登录时更改密码
            '775': 'ACCOUNT_LOCKED',          # 账号已锁定
            
            # 密码策略相关错误
            '19': 'PASSWORD_HISTORY',         # 密码历史限制
            '22': 'PASSWORD_TOO_SHORT',       # 密码太短
            '23': 'PASSWORD_TOO_LONG',        # 密码太长
            '24': 'PASSWORD_WEAK',            # 密码复杂度不足
            '25': 'PASSWORD_TOO_SHORT',       # 密码不满足长度要求
            '26': 'PASSWORD_WEAK',            # 密码不满足复杂度要求
            '27': 'PASSWORD_HISTORY',         # 密码在历史记录中
            
            # 操作权限错误
            '50': 'LDAP_INSUFFICIENT_RIGHTS', # 权限不足
            '53': 'LDAP_UNWILLING_TO_PERFORM', # 服务器拒绝执行
            
            # 连接相关错误
            '81': 'LDAP_CONNECTION_ERROR',    # 连接失败
            '85': 'LDAP_TIMEOUT_ERROR',       # 连接超时
            '91': 'LDAP_CONNECTION_ERROR',    # 无法连接到LDAP服务器
            '112': 'LDAP_SSL_ERROR',          # TLS/SSL错误
        }
        
        mapped_code = error_mapping.get(error_code, 'LDAP_CONNECTION_ERROR')
        error_message = ErrorHandler.get_error_message(mapped_code, message)
        
        # 记录详细的错误日志
        logger.warning(f"LDAP错误: code={error_code}, mapped={mapped_code}, message={message}")
        
        return {
            'error_code': mapped_code,
            'error_message': error_message,
            'original_message': message,
            'ldap_code': error_code
        }


class SessionManager:
    """
    会话管理器 - 统一处理会话和授权码验证
    
    设计说明：
    1. Django的request.session不会自动包含POST/GET参数，必须显式写入
    2. 参考Django的auth机制，使用固定的内部key（_oauth_auth）而非用户可控的username
    3. 认证成功后调用cycle_key()防止会话固定攻击
    """
    
    # 固定的session key（类似Django的SESSION_KEY）
    OAUTH_AUTH_SESSION_KEY = '_oauth_auth'
    
    @staticmethod
    def store_auth_code(request, username: str, code: str) -> None:
        """
        存储授权码到会话（推荐使用bind_oauth_identity替代）
        
        Args:
            request: Django请求对象
            username: 用户名
            code: 授权码
        
        注意：此方法仅保留向后兼容，建议使用bind_oauth_identity
        """
        # 使用命名空间的key，避免session污染
        request.session[f'auth_{username}'] = code
    
    @staticmethod
    def bind_oauth_identity(request, username: str, code: str, 
                          oauth_id: str = '', user_info: Optional[Dict[str, Any]] = None) -> None:
        """
        绑定OAuth认证的真实身份（推荐方式，参考Django auth机制）
        
        Args:
            request: Django请求对象
            username: 用户标识（email/mobile等）
            code: OAuth授权码
            oauth_id: OAuth提供商返回的唯一用户ID
            user_info: OAuth用户信息
        
        设计说明：
        - 使用固定的'_oauth_auth' key（类似Django的'_auth_user_id'）
        - 存储完整的认证上下文，而非简单的username=code
        - 调用cycle_key()防止会话固定攻击
        """
        import time
        import hashlib
        import json
        
        # 关键：重新生成session key（防止会话固定攻击）
        # 类似Django的login()会调用session.cycle_key()
        old_session_key = request.session.session_key
        if not request.session.session_key:
            request.session.create()
        else:
            request.session.cycle_key()
        new_session_key = request.session.session_key
        logger.info(f"Session 轮换: {old_session_key} -> {new_session_key} (user={username})")
        
        # 计算用户信息hash（用于完整性校验）
        user_info_hash = ''
        if user_info:
            user_info_hash = hashlib.sha256(
                json.dumps(user_info, sort_keys=True).encode()
            ).hexdigest()
        
        # 存储到固定的key（不使用用户可控的username作为key）
        auth_data = {
            'oauth_username': username,          # OAuth认证的用户标识
            'oauth_id': oauth_id or '',          # OAuth唯一ID
            'code': code,                         # 授权码
            'timestamp': time.time(),             # 认证时间戳
            'user_info_hash': user_info_hash,    # 用户信息hash
            'verified': True,                     # 已验证标记
            'ip_address': SessionManager.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200]
        }
        
        # 使用固定的内部key（类似Django的SESSION_KEY）
        request.session[SessionManager.OAUTH_AUTH_SESSION_KEY] = auth_data
        
        # 保留向后兼容
        request.session[f'auth_{username}'] = code
        
        logger.info(f"OAuth身份绑定成功: {username} (oauth_id={oauth_id})")

    @staticmethod
    def verify_auth_code(request, username: str, code: str) -> bool:
        """
        验证授权码（增强版，增加身份一致性检查）
        
        Args:
            request: Django请求对象
            username: 用户名
            code: 授权码
            
        Returns:
            授权码是否有效
        """
        # 参数校验
        if not username or not code:
            logger.warning("username或code参数为空")
            return False
        
        # 优先从OAuth认证数据中验证（更安全）
        oauth_auth = request.session.get(SessionManager.OAUTH_AUTH_SESSION_KEY)
        if oauth_auth and isinstance(oauth_auth, dict):
            # 验证身份一致性
            if oauth_auth.get('oauth_username') != username:
                logger.error(f"用户身份不一致：OAuth={oauth_auth.get('oauth_username')}, 请求={username}")
                return False
            
            # 验证授权码
            if oauth_auth.get('code') != code:
                logger.warning(f"授权码不匹配: {username}")
                return False
            
            # 验证时效性（5分钟）
            import time
            timestamp = oauth_auth.get('timestamp', 0)
            if time.time() - timestamp > 300:
                logger.warning("OAuth认证已过期")
                return False
            
            return oauth_auth.get('verified', False)
        
        # 降级到旧方式（向后兼容）
        stored_code = request.session.get(f'auth_{username}')
        return stored_code == code
    
    @staticmethod
    def verify_identity(request, username: str) -> bool:
        """
        验证操作的username与OAuth认证的用户一致（防止越权攻击）
        
        Args:
            request: HTTP请求对象
            username: 待验证的用户名
            strict_ip_check: 是否启用严格IP检查（企业内网建议启用）
            
        Returns:
            bool: 验证是否通过
        """
        oauth_auth = request.session.get(SessionManager.OAUTH_AUTH_SESSION_KEY)
        
        if not oauth_auth or not isinstance(oauth_auth, dict):
            logger.warning(f"会话中无OAuth认证数据")
            return False
        
        # 验证1：username一致性
        oauth_username = oauth_auth.get('oauth_username')
        if oauth_username != username:
            logger.error(f"用户身份不一致：OAuth认证={oauth_username}, 请求={username}")
            return False
        
        # 验证2：认证时效性（5分钟）
        import time
        timestamp = oauth_auth.get('timestamp', 0)
        age = time.time() - timestamp
        if age > 300:
            logger.warning(f"OAuth认证已过期: {age:.1f}秒（超过300秒）")
            return False
        
        # 验证3：verified标记
        if not oauth_auth.get('verified'):
            logger.warning(f"OAuth认证未标记为已验证")
            return False
        
        # 验证4：IP地址一致性（可选）
        if config.get("security.strict_ip_check", False):
            stored_ip = oauth_auth.get('ip_address', '')
            current_ip = SessionManager.get_client_ip(request)
            if stored_ip and stored_ip != current_ip:
                logger.warning(f"IP地址不一致：OAuth认证时={stored_ip}, 当前请求={current_ip}")
                return False
        
        # 验证5：User-Agent一致性（防止会话劫持）
        stored_ua = oauth_auth.get('user_agent', '')
        current_ua = request.META.get('HTTP_USER_AGENT', '')[:200]
        if stored_ua and stored_ua != current_ua:
            logger.warning(f"User-Agent不一致：OAuth认证时={stored_ua[:50]}..., 当前请求={current_ua[:50]}...")
            # User-Agent变化较常见（浏览器更新等），仅记录警告，不阻止操作
            # 如需严格模式，可改为 return False
        
        return True
    
    @staticmethod
    def get_client_ip(request) -> str:
        """获取客户端真实IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
    
    @staticmethod
    def clear_auth_code(request, username: str) -> None:
        """
        清除授权码
        
        Args:
            request: Django请求对象
            username: 用户名
        """
        # 清除旧方式的数据
        auth_key = f'auth_{username}'
        if auth_key in request.session:
            del request.session[auth_key]
    
    @staticmethod
    def clear_session(request) -> None:
        """
        清除所有认证相关的session数据
        
        Args:
            request: Django请求对象
        """
        # 清除OAuth认证数据
        if SessionManager.OAUTH_AUTH_SESSION_KEY in request.session:
            del request.session[SessionManager.OAUTH_AUTH_SESSION_KEY]
        
        # 清除所有auth_*开头的key
        keys_to_delete = [k for k in request.session.keys() if k.startswith('auth_')]
        for key in keys_to_delete:
            del request.session[key]
        
        # 清除所有oauth_user_info_*开头的key
        keys_to_delete = [k for k in request.session.keys() if k.startswith('oauth_user_info_')]
        for key in keys_to_delete:
            del request.session[key]
        
        # 清除所有sms_verified_*开头的key
        keys_to_delete = [k for k in request.session.keys() if k.startswith('sms_verified_')]
        for key in keys_to_delete:
            del request.session[key]

    @staticmethod
    def get_auth_code(request, username: str) -> Optional[str]:
        """
        获取授权码
        
        Args:
            request: Django请求对象
            username: 用户名
            
        Returns:
            授权码或None
        """
        # 优先从OAuth认证数据获取
        oauth_auth = request.session.get(SessionManager.OAUTH_AUTH_SESSION_KEY)
        if oauth_auth and isinstance(oauth_auth, dict):
            if oauth_auth.get('oauth_username') == username:
                return oauth_auth.get('code')
        
        # 降级到旧方式（向后兼容）
        return request.session.get(f'auth_{username}')
    
    @staticmethod
    def store_oauth_user_info(request, username: str, user_info: Dict[str, Any]) -> None:
        """
        存储OAuth用户信息到会话（用于SMS手机号解析）
        
        Args:
            request: Django请求对象
            username: 用户名
            user_info: OAuth用户信息
        """
        session_key = f"oauth_user_info_{username}"
        request.session[session_key] = user_info
    
    @staticmethod
    def get_oauth_user_info(request, username: str) -> Optional[Dict[str, Any]]:
        """
        获取OAuth用户信息
        
        Args:
            request: Django请求对象
            username: 用户名
            
        Returns:
            OAuth用户信息或None
        """
        session_key = f"oauth_user_info_{username}"
        return request.session.get(session_key)
    
    @staticmethod
    def store_sms_verification(request, username: str, mobile: str) -> None:
        """
        存储SMS验证信息到会话
        
        Args:
            request: Django请求对象
            username: 用户名
            mobile: 手机号
        """
        session_key = f"sms_verified_{username}"
        request.session[session_key] = {
            'mobile': mobile,
            'verified': True,
            'timestamp': __import__('time').time()
        }
    
    @staticmethod
    def verify_sms_verification(request, username: str) -> bool:
        """
        验证SMS验证是否有效
        
        Args:
            request: Django请求对象
            username: 用户名
            
        Returns:
            验证是否有效
        """
        session_key = f"sms_verified_{username}"
        sms_info = request.session.get(session_key)
        
        if not sms_info:
            return False
        
        # 检查是否过期（5分钟）
        import time
        current_time = time.time()
        timestamp = sms_info.get('timestamp', 0)
        
        if current_time - timestamp > 300:  # 5分钟
            SessionManager.clear_sms_verification(request, username)
            return False
        
        return sms_info.get('verified', False)
    
    @staticmethod
    def get_sms_mobile(request, username: str) -> str:
        """
        获取存储的SMS手机号（用于验证码验证时获取完整手机号）
        
        Args:
            request: Django请求对象
            username: 用户名
            
        Returns:
            存储的手机号或空字符串
        """
        session_key = f"sms_mobile_{username}"
        return request.session.get(session_key, '')
    
    @staticmethod
    def store_sms_mobile(request, username: str, mobile: str) -> None:
        """
        存储发送验证码时的完整手机号（用于后续验证）
        
        Args:
            request: Django请求对象
            username: 用户名
            mobile: 完整手机号
        """
        session_key = f"sms_mobile_{username}"
        request.session[session_key] = mobile
    
    @staticmethod
    def clear_sms_verification(request, username: str) -> None:
        """
        清除SMS验证信息
        
        Args:
            request: Django请求对象
            username: 用户名
        """
        session_key = f"sms_verified_{username}"
        if session_key in request.session:
            del request.session[session_key]
        # 同时清除存储的手机号
        mobile_key = f"sms_mobile_{username}"
        if mobile_key in request.session:
            del request.session[mobile_key]
