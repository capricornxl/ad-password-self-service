# -*- coding: utf-8 -*-
"""
HTTP代理工具模块
用于为OAuth API请求提供代理支持
"""
from typing import Optional, Dict
from utils.config import get_config
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class ProxyManager:
    """
    HTTP代理管理器
    
    负责从配置读取代理设置并构建requests库所需的proxies字典
    """
    
    def __init__(self):
        """初始化代理管理器"""
        self.config = get_config()
        self._proxy_dict = None
        self._is_enabled = None
        self._load_config()
    
    def _load_config(self):
        """从配置加载代理设置"""
        proxy_config = self.config.get_dict('network.proxy', {})
        
        self._is_enabled = proxy_config.get('enabled', False)
        
        if not self._is_enabled:
            logger.debug("HTTP代理未启用")
            return
        
        http_proxy = proxy_config.get('http_proxy', '').strip()
        https_proxy = proxy_config.get('https_proxy', '').strip()
        proxy_username = proxy_config.get('proxy_username', '').strip()
        proxy_password = proxy_config.get('proxy_password', '').strip()
        
        # 如果配置了认证信息，构建带认证的代理URL
        if proxy_username and proxy_password:
            http_proxy = self._add_auth_to_proxy(http_proxy, proxy_username, proxy_password)
            https_proxy = self._add_auth_to_proxy(https_proxy, proxy_username, proxy_password)
        
        # 构建proxies字典
        proxies = {}
        if http_proxy:
            proxies['http'] = http_proxy
            logger.info(f"HTTP代理已启用: {self._mask_proxy_url(http_proxy)}")
        if https_proxy:
            proxies['https'] = https_proxy
            logger.info(f"HTTPS代理已启用: {self._mask_proxy_url(https_proxy)}")
        
        self._proxy_dict = proxies if proxies else None
        
        # 记录no_proxy配置
        no_proxy = proxy_config.get('no_proxy', '')
        if no_proxy:
            logger.debug(f"No proxy配置: {no_proxy}")
    
    @staticmethod
    def _add_auth_to_proxy(proxy_url: str, username: str, password: str) -> str:
        """
        为代理URL添加认证信息
        
        Args:
            proxy_url: 代理URL，如 http://proxy.company.com:3128
            username: 用户名
            password: 密码
            
        Returns:
            带认证的代理URL，如 http://user:pass@proxy.company.com:3128
        """
        if not proxy_url or not username:
            return proxy_url
        
        # 解析URL
        if '://' in proxy_url:
            protocol, rest = proxy_url.split('://', 1)
            return f"{protocol}://{username}:{password}@{rest}"
        else:
            return f"http://{username}:{password}@{proxy_url}"
    
    @staticmethod
    def _mask_proxy_url(proxy_url: str) -> str:
        """
        遮蔽代理URL中的敏感信息（用于日志）
        
        Args:
            proxy_url: 完整的代理URL
            
        Returns:
            脱敏后的URL
        """
        if not proxy_url:
            return ""
        
        # 如果包含认证信息，遮蔽密码
        if '@' in proxy_url:
            parts = proxy_url.split('@')
            if len(parts) == 2:
                auth_part, host_part = parts
                if ':' in auth_part:
                    # 提取协议部分
                    if '://' in auth_part:
                        protocol, credentials = auth_part.split('://', 1)
                        username = credentials.split(':')[0]
                        return f"{protocol}://{username}:****@{host_part}"
                    else:
                        username = auth_part.split(':')[0]
                        return f"{username}:****@{host_part}"
        
        return proxy_url
    
    def is_enabled(self) -> bool:
        """
        检查代理是否启用
        
        Returns:
            是否启用代理
        """
        return self._is_enabled and self._proxy_dict is not None
    
    def get_proxies(self) -> Optional[Dict[str, str]]:
        """
        获取proxies字典（用于requests库）
        
        Returns:
            proxies字典，如 {'http': 'http://proxy:3128', 'https': 'http://proxy:3128'}
            如果未启用代理则返回None
        """
        return self._proxy_dict if self._is_enabled else None
    
    def get_session_config(self) -> Dict:
        """
        获取requests.Session的完整配置
        
        Returns:
            包含proxies等配置的字典
        """
        config = {}
        
        if self.is_enabled():
            config['proxies'] = self.get_proxies()
            
            # 添加no_proxy环境变量（requests库会自动读取）
            no_proxy = self.config.get('network.proxy.no_proxy', '')
            if no_proxy:
                import os
                os.environ['NO_PROXY'] = no_proxy
                os.environ['no_proxy'] = no_proxy
        
        return config


# 全局代理管理器单例
_proxy_manager = None


def get_proxy_manager() -> ProxyManager:
    """
    获取全局代理管理器单例
    
    Returns:
        ProxyManager实例
    """
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager


def get_proxies() -> Optional[Dict[str, str]]:
    """
    快捷方法：获取proxies字典
    
    Returns:
        proxies字典或None
        
    Example:
        >>> proxies = get_proxies()
        >>> response = requests.get(url, proxies=proxies)
    """
    return get_proxy_manager().get_proxies()
