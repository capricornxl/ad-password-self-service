# -*- coding: utf-8 -*-
"""
飞书 OAuth 提供商实现
基于飞书开放平台 OAuth 2.0 协议（新版 API）

文档:
- 登录概述: https://open.feishu.cn/document/sso/web-application-sso/login-overview
- 获取授权码: https://open.feishu.cn/document/common-capabilities/sso/api/obtain-oauth-code
- 获取 user_access_token: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/authentication-management/access-token/get-user-access-token
- 获取用户信息: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/authen-v1/user_info/get
"""
from typing import Tuple, Optional, Dict, Any
import requests
import json
import time
from utils.config import get_config
from utils.oauth.base_provider import BaseOAuthProvider
from utils.proxy_manager import get_proxies
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class FeishuAPIClient:
    """
    飞书 API 客户端
    
    使用新版 OAuth 2.0 API，支持：
    1. 通过授权码获取 user_access_token
    2. 获取用户信息
    3. HTTP 代理支持
    4. 完善的错误处理
    """
    
    # API 基础地址
    BASE_URL = "https://open.feishu.cn/open-apis"
    # 授权页面地址
    AUTHORIZE_URL = "https://accounts.feishu.cn/open-apis/authen/v1/authorize"
    
    def __init__(self, app_id: str, app_secret: str):
        """
        初始化飞书 API 客户端
        
        Args:
            app_id: 应用的 App ID
            app_secret: 应用的 App Secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.proxies = get_proxies()
        
        if self.proxies:
            logger.info("[飞书API] 已启用HTTP代理")
    
    def _request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        发起 HTTP 请求
        
        Args:
            method: HTTP 方法（GET/POST）
            url: 请求 URL
            **kwargs: 其他请求参数
            
        Returns:
            响应 JSON 数据
            
        Raises:
            Exception: 请求失败时抛出
        """
        if self.proxies:
            kwargs['proxies'] = self.proxies
        
        # 设置超时
        kwargs.setdefault('timeout', 10)
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"[飞书API] 请求失败: {url}, 错误: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"[飞书API] JSON解析失败: {e}")
            raise
    
    def get_user_access_token(self, code: str, redirect_uri: str = '') -> Dict[str, Any]:
        """
        通过授权码获取 user_access_token
        
        新版 API: POST /authen/v2/oauth/token
        文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/authentication-management/access-token/get-user-access-token
        
        注意：新版 API 不需要 app_access_token，直接在请求体中传递 client_id 和 client_secret
        
        Args:
            code: 授权码（有效期 5 分钟，只能使用一次）
            redirect_uri: 回调地址（可选，需与授权时一致）
            
        Returns:
            包含 access_token、refresh_token 等信息的字典
        """
        url = f"{self.BASE_URL}/authen/v2/oauth/token"
        
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'code': code,
        }
        
        # 如果提供了 redirect_uri，添加到请求中
        if redirect_uri:
            data['redirect_uri'] = redirect_uri
        
        logger.debug(f"[飞书API] 通过授权码获取 user_access_token, code={code[:10]}...")
        result = self._request('POST', url, headers=headers, json=data)
        
        if result.get('code') == 0:
            logger.info("[飞书API] user_access_token 获取成功")
            return {
                'access_token': result.get('access_token'),
                'expires_in': result.get('expires_in', 7200),
                'refresh_token': result.get('refresh_token'),
                'refresh_token_expires_in': result.get('refresh_token_expires_in'),
                'token_type': result.get('token_type', 'Bearer'),
                'scope': result.get('scope'),
            }
        else:
            error_code = result.get('code', 'unknown')
            error_msg = result.get('msg', result.get('error_description', '未知错误'))
            logger.error(f"[飞书API] 获取 user_access_token 失败: {error_code}-{error_msg}")
            raise Exception(f"获取飞书 user_access_token 失败: {error_msg} (code: {error_code})")
    
    def get_user_info(self, user_access_token: str) -> Dict[str, Any]:
        """
        获取用户信息
        
        API: GET /authen/v1/user_info
        文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/authen-v1/user_info/get
        
        Args:
            user_access_token: 用户访问令牌
            
        Returns:
            用户信息字典
        """
        url = f"{self.BASE_URL}/authen/v1/user_info"
        
        headers = {
            'Authorization': f'Bearer {user_access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        
        logger.debug("[飞书API] 获取用户信息")
        result = self._request('GET', url, headers=headers)
        
        if result.get('code') == 0:
            logger.info("[飞书API] 用户信息获取成功")
            return result.get('data', {})
        else:
            error_code = result.get('code', 'unknown')
            error_msg = result.get('msg', '未知错误')
            logger.error(f"[飞书API] 获取用户信息失败: {error_code}-{error_msg}")
            raise Exception(f"获取飞书用户信息失败: {error_msg}")
    
    def get_user_info_by_code(self, code: str, redirect_uri: str = '') -> Dict[str, Any]:
        """
        通过授权码直接获取用户信息（一步到位）
        
        Args:
            code: 授权码
            redirect_uri: 回调地址（可选）
            
        Returns:
            用户信息字典
        """
        # 先获取 user_access_token
        token_data = self.get_user_access_token(code, redirect_uri)
        user_access_token = token_data.get('access_token')
        
        if not user_access_token:
            raise Exception("未能获取 user_access_token")
        
        # 再获取用户信息
        return self.get_user_info(user_access_token)


class FeishuProvider(BaseOAuthProvider):
    """
    飞书 OAuth 提供商
    
    配置项（在 oauth_providers.feishu 下）：
    - app_id: 应用的 App ID
    - app_secret: 应用的 App Secret
    
    用户标识字段（可通过 user_identifier_mapping 配置）：
    - open_id: 用户在应用内的唯一标识（推荐）
    - union_id: 用户在同一企业下所有应用内的唯一标识
    - user_id: 用户在企业内的唯一标识（仅自建应用可用）
    - employee_no: 员工工号（仅自建应用可用）
    """
    
    def __init__(self):
        """初始化飞书 OAuth 提供商"""
        super().__init__()
        
        config = get_config()
        feishu_config = config.get_dict('oauth_providers.feishu')
        
        self._app_id = feishu_config.get('app_id', '')
        self._app_secret = feishu_config.get('app_secret', '')
        
        # 用户标识字段映射（默认使用 open_id）
        self._user_identifier_field = feishu_config.get('user_identifier_mapping', 'open_id')
        
        # 初始化 API 客户端
        self._client = None
        if self._app_id and self._app_secret:
            self._client = FeishuAPIClient(self._app_id, self._app_secret)
            logger.info(f"[飞书] OAuth 提供商初始化成功, app_id={self._app_id[:8]}...")
        else:
            logger.warning("[飞书] OAuth 提供商配置不完整，缺少 app_id 或 app_secret")
    
    @property
    def provider_name(self) -> str:
        """提供商名称"""
        return "飞书"
    
    @property
    def provider_type(self) -> str:
        """提供商类型"""
        return "feishu"
    
    @property
    def corp_id(self) -> str:
        """企业ID（飞书使用 app_id）"""
        return self._app_id
    
    @property
    def app_id(self) -> str:
        """应用ID"""
        return self._app_id
    
    def get_auth_config(self, home_url: str, redirect_url: str) -> Dict[str, Any]:
        """
        获取前端 OAuth 授权配置
        
        飞书网页应用登录授权 URL 格式（新版 API）：
        https://accounts.feishu.cn/open-apis/authen/v1/authorize?client_id={app_id}&redirect_uri={redirect_uri}&response_type=code&state={state}
        
        文档: https://open.feishu.cn/document/common-capabilities/sso/api/obtain-oauth-code
        
        Args:
            home_url: 主页URL
            redirect_url: 回调URL
            
        Returns:
            前端授权配置字典
        """
        return {
            'provider_type': self.provider_type,
            'provider_name': self.provider_name,
            'app_id': self._app_id,
            'corp_id': self._app_id,  # 兼容旧配置
            'redirect_url': redirect_url,
            # 飞书特有配置（新版 API）
            'auth_url': 'https://accounts.feishu.cn/open-apis/authen/v1/authorize',
            'response_type': 'code',
        }
    
    def get_user_id_by_code(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        通过授权码获取用户ID
        
        Args:
            code: 授权码（有效期约 5 分钟）
            
        Returns:
            (成功状态, 用户ID 或 错误信息)
        """
        if not self._client:
            return False, "飞书 OAuth 提供商未正确配置"
        
        try:
            logger.debug(f"[飞书] 通过授权码获取用户ID, code={code[:10]}...")
            
            # 获取用户信息
            user_info = self._client.get_user_info_by_code(code)
            
            # 提取用户标识
            user_id = self._extract_user_identifier(user_info)
            
            if user_id:
                logger.info(f"[飞书] 成功获取用户ID: {user_id}")
                return True, user_id
            else:
                logger.warning(f"[飞书] 响应中缺少用户标识字段: {user_info}")
                return False, "获取用户ID失败: 响应数据不完整"
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[飞书] 获取用户ID异常: {error_msg}")
            
            # 处理常见错误
            if '授权码' in error_msg or 'code' in error_msg.lower():
                return False, "授权码已过期，请重新授权"
            elif 'token' in error_msg.lower():
                return False, "系统凭证失效，请重试"
            else:
                return False, f"获取用户ID异常: {error_msg}"
    
    def get_user_detail_by_user_id(self, user_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        通过用户ID获取用户详情
        
        注意：飞书 OAuth 流程中，用户详情在获取 user_access_token 时已返回。
        此方法返回一个包含用户ID的占位字典，实际用户信息应在 get_user_detail 中获取。
        
        Args:
            user_id: 用户ID（open_id/union_id/user_id）
            
        Returns:
            (成功状态, 用户信息字典 或 错误信息)
        """
        # 飞书的用户详情在 OAuth 流程中已获取
        # 这里返回一个包含用户ID的占位字典
        logger.debug(f"[飞书] get_user_detail_by_user_id 被调用, user_id={user_id}")
        
        # 返回基本信息，实际信息需要通过其他 API 获取（需要额外权限）
        return True, {
            'open_id': user_id,
            'user_id': user_id,
            'name': user_id,  # 占位，实际名称需要通过通讯录 API 获取
        }
    
    def get_user_detail(self, code: str, home_url: str) -> Tuple[bool, Any, Optional[Dict[str, Any]]]:
        """
        通过授权码获取用户详情（OAuth2 完整流程）
        
        Args:
            code: 授权码
            home_url: 主页URL
            
        Returns:
            (成功状态, 用户ID/错误上下文, 用户信息/错误信息)
        """
        if not self._client:
            return False, "配置错误", {"error": "飞书 OAuth 提供商未正确配置"}
        
        logger.info(f"[飞书] 开始 OAuth 流程, home_url={home_url}")
        
        try:
            # 步骤1: 通过授权码获取 user_access_token
            # 注意：需要传递 redirect_uri，必须与授权请求时的 redirect_uri 一致
            logger.debug("[飞书] 步骤1: 获取 user_access_token")
            
            # 构建 redirect_uri（与授权请求保持一致）
            redirect_uri = f"{home_url}/resetPassword"
            logger.debug(f"[飞书] redirect_uri: {redirect_uri}")
            
            token_data = self._client.get_user_access_token(code, redirect_uri)
            user_access_token = token_data.get('access_token')
            
            if not user_access_token:
                logger.error(f"[飞书] 未能获取 user_access_token: {token_data}")
                return False, "获取访问令牌失败", {"error": "未能获取 user_access_token"}
            
            # 步骤2: 获取用户信息
            logger.debug("[飞书] 步骤2: 获取用户信息")
            user_info = self._client.get_user_info(user_access_token)
            
            # 提取用户标识
            user_id = self._extract_user_identifier(user_info)
            
            if not user_id:
                logger.error(f"[飞书] 响应中缺少用户标识: {user_info}")
                return False, "获取用户ID失败", {"error": "响应数据不完整"}
            
            # 构建标准化的用户信息
            standardized_info = self._standardize_user_info(user_info)
            
            logger.info(f"[飞书] OAuth 流程完成, user_id={user_id}, name={standardized_info.get('name')}")
            return True, user_id, standardized_info
            
        except Exception as e:
            error_msg = str(e)
            logger.exception(f"[飞书] OAuth 流程异常: {error_msg}")
            return False, "OAuth流程异常", {"error": error_msg}
    
    def _extract_user_identifier(self, user_info: Dict[str, Any]) -> Optional[str]:
        """
        从用户信息中提取用户标识
        
        根据 user_identifier_mapping 配置提取对应的用户标识字段
        
        Args:
            user_info: 用户信息字典
            
        Returns:
            用户标识字符串
        """
        field = self._user_identifier_field
        
        # 支持的字段映射
        field_mapping = {
            'open_id': 'open_id',
            'openid': 'open_id',
            'union_id': 'union_id',
            'unionid': 'union_id',
            'user_id': 'user_id',
            'userid': 'user_id',
            'employee_no': 'employee_no',
            'employeeno': 'employee_no',
        }
        
        actual_field = field_mapping.get(field.lower(), 'open_id')
        return user_info.get(actual_field)
    
    def _standardize_user_info(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化用户信息
        
        将飞书返回的用户信息转换为统一格式
        
        Args:
            user_info: 原始用户信息
            
        Returns:
            标准化后的用户信息
        """
        return {
            # 用户标识
            'open_id': user_info.get('open_id'),
            'union_id': user_info.get('union_id'),
            'user_id': user_info.get('user_id'),
            'employee_no': user_info.get('employee_no'),
            
            # 基本信息
            'name': user_info.get('name'),
            'en_name': user_info.get('en_name'),
            'avatar_url': user_info.get('avatar_url') or user_info.get('picture'),
            'email': user_info.get('email'),
            'mobile': user_info.get('mobile'),
            
            # 企业信息
            'tenant_key': user_info.get('tenant_key'),
            
            # 原始数据
            'raw_data': user_info,
        }