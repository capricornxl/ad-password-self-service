# -*- coding: utf-8 -*-
"""
钉钉OAuth提供商实现 - 使用新版 API
基于钉钉开放平台 v2 接口（https://open.dingtalk.com）
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


class DingTalkAPIClient:
    """
    钉钉新版 API 客户端
    
    使用钉钉开放平台 v2 接口，支持：
    1. 自动 access_token 管理和刷新
    2. HTTP 代理支持
    3. 完善的错误处理和重试机制
    """
    
    # API 基础地址
    BASE_URL = "https://oapi.dingtalk.com"
    
    def __init__(self, app_key: str, app_secret: str):
        """
        初始化钉钉 API 客户端
        
        Args:
            app_key: 应用的 AppKey
            app_secret: 应用的 AppSecret
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.proxies = get_proxies()
        
        # access_token 缓存
        self._access_token = None
        self._token_expires_at = 0
        
        if self.proxies:
            logger.info("[钉钉API] 已启用HTTP代理")
    
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
            # logger.debug(f"[钉钉API] 请求成功: {url}, 响应: {json.dumps(result, ensure_ascii=False)[:200]}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"[钉钉API] 请求失败: {url}, 错误: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"[钉钉API] JSON解析失败: {e}")
            raise
    
    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        获取 access_token（自动缓存和刷新）
        
        Args:
            force_refresh: 是否强制刷新 token
            
        Returns:
            access_token 字符串
            
        Raises:
            Exception: 获取 token 失败时抛出
        """
        # 检查缓存是否有效（提前 5 分钟刷新）
        current_time = time.time()
        if not force_refresh and self._access_token and current_time < self._token_expires_at - 300:
            logger.debug("[钉钉API] 使用缓存的 access_token")
            return self._access_token
        
        # 获取新的 access_token
        url = f"{self.BASE_URL}/gettoken"
        params = {
            'appkey': self.app_key,
            'appsecret': self.app_secret
        }
        
        logger.debug("[钉钉API] 获取新的 access_token")
        result = self._request('GET', url, params=params)
        logger.debug(f"[钉钉API] 获取新的 access_token响应: {result}")
        
        if result.get('errcode') == 0:
            self._access_token = result.get('access_token')
            expires_in = result.get('expires_in', 7200)  # 默认 7200 秒
            self._token_expires_at = current_time + expires_in
            
            logger.info(f"[钉钉API] access_token 获取成功，有效期: {expires_in}秒")
            return self._access_token
        else:
            error_msg = result.get('errmsg', '未知错误')
            logger.error(f"[钉钉API] 获取 access_token 失败: {error_msg}")
            raise Exception(f"获取钉钉 access_token 失败: {error_msg}")
    
    def get_user_info_by_code(self, code: str) -> Dict[str, Any]:
        """
        通过免登授权码获取用户信息（新版 API）
        
        API: POST /topapi/v2/user/getuserinfo
        文档: https://open.dingtalk.com/document/orgapp/obtain-the-userid-of-a-user-by-using-the-log-free
        
        Args:
            code: 免登授权码（临时授权码）
            
        Returns:
            用户信息字典，包含 userid 等字段
            
        Raises:
            Exception: 请求失败时抛出
        """
        access_token = self.get_access_token()
        url = f"{self.BASE_URL}/topapi/v2/user/getuserinfo"
        
        params = {'access_token': access_token}
        data = {'code': code}
        
        logger.debug(f"[钉钉API] 通过免登码获取用户信息, code={code[:10]}...")
        result = self._request('POST', url, params=params, json=data)
        logger.debug(f"[钉钉API] 获取用户信息响应: {result}")

        if result.get('errcode') == 0:
            user_info = result.get('result', {})
            user_id = user_info.get('userid')
            logger.info(f"[钉钉API] 成功获取用户信息: userid={user_id}")
            return user_info
        else:
            error_code = result.get('errcode')
            error_msg = result.get('errmsg', '未知错误')
            logger.error(f"[钉钉API] 获取用户信息失败: errcode={error_code}, errmsg={error_msg}")
            raise Exception(f"获取用户信息失败: {error_msg} (错误码: {error_code})")
    
    def get_user_detail(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户详细信息（新版 API）
        
        API: POST /topapi/v2/user/get
        文档: https://open.dingtalk.com/document/orgapp/query-user-details
        
        Args:
            user_id: 用户 userid
            
        Returns:
            用户详细信息字典
            
        Raises:
            Exception: 请求失败时抛出
        """
        access_token = self.get_access_token()
        url = f"{self.BASE_URL}/topapi/v2/user/get"
        
        params = {'access_token': access_token}
        data = {'userid': user_id}
        
        logger.debug(f"[钉钉API] 获取用户详细信息, userid={user_id}")
        result = self._request('POST', url, params=params, json=data)
        logger.debug(f"[钉钉API] 获取用户详细信息响应: {result}")

        if result.get('errcode') == 0:
            user_detail = result.get('result', {})
            logger.info(f"[钉钉API] 成功获取用户详细信息: name={user_detail.get('name')}")
            return user_detail
        else:
            error_code = result.get('errcode')
            error_msg = result.get('errmsg', '未知错误')
            logger.error(f"[钉钉API] 获取用户详细信息失败: errcode={error_code}, errmsg={error_msg}")
            raise Exception(f"获取用户详细信息失败: {error_msg} (错误码: {error_code})")


class DingTalkProvider(BaseOAuthProvider):
    """钉钉OAuth提供商 - 新版 API 实现"""
    
    def __init__(self):
        """初始化钉钉提供商"""
        super().__init__()
        config = get_config()
        ding_config = config.get_dict('oauth_providers.ding')
        
        self._corp_id = ding_config.get('corp_id')
        self._app_key = ding_config.get('app_key')
        self._app_secret = ding_config.get('app_secret')
        self._app_id = ding_config.get('app_id')
        
        # 初始化新版 API 客户端
        self._client = DingTalkAPIClient(self._app_key, self._app_secret)
        
        logger.info("[钉钉Provider] 初始化完成，使用新版 API v2")
    
    @property
    def provider_name(self) -> str:
        """提供商名称"""
        return "钉钉"
    
    @property
    def provider_type(self) -> str:
        """提供商类型"""
        return "ding"
    
    @property
    def corp_id(self) -> str:
        """企业ID"""
        return self._corp_id
    
    @property
    def app_id(self) -> str:
        """应用ID"""
        return self._app_id
    
    def get_user_id_by_code(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        通过授权码获取用户ID
        
        Args:
            code: 免登授权码
            
        Returns:
            (成功状态, 用户ID 或 错误信息)
        """
        try:
            user_info = self._client.get_user_info_by_code(code)
            user_id = user_info.get('userid')
            
            if user_id:
                logger.info(f"[钉钉] 成功获取 user_id: {user_id}")
                return True, user_id
            else:
                logger.warning("[钉钉] 响应中缺少 userid 字段")
                return False, "获取用户ID失败: 响应数据不完整"
                
        except Exception as e:
            logger.exception(f"[钉钉] 获取用户ID异常: {str(e)}")
            return False, f"获取用户ID异常: {str(e)}"
    
    def get_user_detail_by_user_id(self, user_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        通过用户ID获取用户详情
        
        Args:
            user_id: 用户ID
            
        Returns:
            (成功状态, 用户信息字典 或 错误信息)
        """
        try:
            user_detail = self._client.get_user_detail(user_id)
            logger.info(f"[钉钉] 成功获取用户详情: {user_detail.get('name')}")
            return True, user_detail
            
        except Exception as e:
            logger.exception(f"[钉钉] 获取用户详情异常: {str(e)}")
            return False, f"获取用户详情异常: {str(e)}"
    
    def get_user_detail(self, code: str, home_url: str) -> Tuple[bool, Any, Optional[Dict[str, Any]]]:
        """
        通过授权码获取用户详情（完整流程）
        
        Args:
            code: 免登授权码
            home_url: 主页URL
            
        Returns:
            (成功状态, 用户ID/错误上下文, 用户信息/错误信息)
        """
        logger.info(f"[钉钉] 开始OAuth流程, home_url={home_url}")
        
        # 步骤1: 通过免登码获取 user_id
        status, user_id = self.get_user_id_by_code(code)
        if not status:
            config = get_config()
            context = {
                'global_title': config.get('app.title', 'Self-Service'),
                'msg': f'获取用户ID失败，错误信息：{user_id}',
                'button_click': f"window.location.href='{home_url}'",
                'button_display': "返回主页"
            }
            return False, context, user_id
        
        # 步骤2: 通过 user_id 获取用户详情
        status, user_info = self.get_user_detail_by_user_id(user_id)
        if not status:
            config = get_config()
            context = {
                'global_title': config.get('app.title', 'Self-Service'),
                'msg': f'获取用户信息失败，错误信息：{user_info}',
                'button_click': f"window.location.href='{home_url}'",
                'button_display': "返回主页"
            }
            return False, context, user_info
        
        logger.info(f"[钉钉] OAuth流程成功完成, user_id={user_id}")
        return True, user_id, user_info
