# -*- coding: utf-8 -*-
"""
LDAP安全验证器
验证服务账号的权限是否符合安全要求
"""

import re
import traceback
from typing import Tuple, List, Dict, Optional
from .adapter import LDAPAdapter
from .errors import LDAPException, LDAPErrorCode
from utils.config import get_config
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class LDAPSecurityValidator:
    """LDAP安全验证器"""
    
    def __init__(self, adapter: LDAPAdapter):
        """
        初始化安全验证器
        
        Args:
            adapter: LDAP适配器实例
        """
        self.adapter = adapter
        config = get_config()
        
        # 读取安全配置
        security_config = config.get('ldap.security', {})
        
        # 是否启用验证
        self.enabled = security_config.get('validate_permissions_on_startup', True)
        
        # 危险组配置 (列表,每项可以是字典或字符串)
        self.dangerous_groups = security_config.get('dangerous_groups', [])
        
        # 推荐组配置 (列表,每项可以是字典或字符串)
        self.recommended_groups = security_config.get('recommended_groups', [])
        
        # 是否强制要求推荐组
        self.require_recommended = security_config.get('require_recommended_group', False)
        
        # 验证模式: strict(严格), warning(警告), disabled(禁用)
        self.validation_mode = security_config.get('validation_mode', 'warning').lower()
        
        logger.debug(f"安全验证器初始化: mode={self.validation_mode}, "
                    f"dangerous_groups={len(self.dangerous_groups)}, "
                    f"recommended_groups={len(self.recommended_groups)}")
    
    def validate_service_account(self, username: Optional[str] = None) -> Tuple[bool, str]:
        """
        验证服务账号权限
        
        Args:
            username: 服务账号用户名,如果为None则从配置读取
            
        Returns:
            (是否通过验证, 消息)
            
        Raises:
            LDAPException: 验证过程中发生错误
        """
        # 检查是否启用验证
        if not self.enabled:
            logger.debug("安全验证已禁用")
            return True, "安全验证已禁用"
        
        # 检查验证模式
        if self.validation_mode == 'disabled':
            logger.debug("验证模式为disabled")
            return True, "验证模式为disabled"
        
        try:
            # 获取服务账号用户名
            if username is None:
                config = get_config()
                username = config.get('ldap.login_user')
                if not username:
                    raise ValueError("配置文件中未找到 ldap.login_user")
                # 处理DOMAIN\username格式 (AD)
                if '\\' in username:
                    username = username.split('\\')[1]
                # 处理DN格式 (OpenLDAP)
                elif '=' in username:
                    # 从DN中提取用户名,如: cn=admin,dc=company,dc=com -> admin
                    match = re.match(r'^(?:cn|uid)=([^,]+)', username, re.IGNORECASE)
                    if match:
                        username = match.group(1)
            
            logger.info(f"开始验证服务账号权限: {username}")
            
            # 类型断言: 确保username不为None
            assert username is not None, "username不能为None"
            
            # 确保连接
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            # 获取用户所属组
            try:
                success, group_dns = self.adapter.get_user_groups(username)
                if not success:
                    logger.error(f"无法获取服务账号 {username} 的组信息")
                    return False, f"无法获取服务账号 {username} 的组信息"
            except LDAPException as ldap_ex:
                # 特殊处理: 用户不存在的情况 (可能是系统管理员)
                if ldap_ex.code == LDAPErrorCode.ACCOUNT_NOT_FOUND:
                    logger.warning(f"服务账号 {username} 在LDAP目录中未找到，检查是否为系统管理员")
                    return self._handle_system_admin(username)
                # 其他LDAP异常继续抛出
                raise
            
            # 提取组名
            group_names = [self.adapter.extract_group_name(dn) for dn in group_dns]
            
            logger.debug(f"服务账号 {username} 所属组: {group_names}")
            
            # 检查危险组
            dangerous_matches = self._check_dangerous_groups(group_dns, group_names)
            if dangerous_matches:
                msg = f"服务账号属于高危组: {dangerous_matches}"
                logger.error(msg)
                return False, msg
            
            # 检查推荐组
            if self.recommended_groups:
                in_recommended = self._check_recommended_groups(group_dns, group_names)
                
                if not in_recommended:
                    msg = f"服务账号不属于推荐组: {self._format_group_list(self.recommended_groups)}"
                    
                    if self.require_recommended:
                        # 强制要求推荐组
                        logger.error(f"{msg} (强制要求)")
                        return False, f"{msg}\n强制要求服务账号属于推荐组之一"
                    else:
                        # 仅警告
                        logger.warning(msg)
                        print(f"\n{msg}")
                        print("建议: 将服务账号添加到专用组以便管理\n")
            
            # 验证通过
            msg = "服务账号权限检查通过"
            logger.info(msg)
            return True, msg
        
        except LDAPException as e:
            logger.error(f"权限验证失败: {e.get_log_message()}", exc_info=True)
            logger.debug(f"{traceback.format_exc()}")
            raise
        except Exception as e:
            logger.error(f"权限验证异常: {e}", exc_info=True)
            raise LDAPException(
                LDAPErrorCode.INTERNAL_ERROR,
                f"权限验证失败: {str(e)}",
                self.adapter.ldap_type,
                e
            )
    
    def _handle_system_admin(self, username: str) -> Tuple[bool, str]:
        """
        处理系统管理员账号 (无法通过常规LDAP查询验证)
        
        Args:
            username: 用户名
            
        Returns:
            (是否通过验证, 消息)
        """
        is_system_admin, reason = self._is_system_admin(username)
        
        if is_system_admin:
            msg = f"检测到系统级管理员账号: {username} ({reason})"
            
            if self.validation_mode == 'strict':
                # 严格模式: 禁止使用系统管理员
                logger.error(f"{msg} - 禁止使用 (严格模式)")
                return False, f"{msg}\n\n不允许使用系统管理员账号。\n建议: 创建专用服务账号并授予必要权限"
            
            else:  # warning 模式
                # 警告模式: 允许但强烈警告
                logger.warning(f"{msg} - 允许使用但存在严重安全风险")
                return True, f"{msg}\n\n严重警告: 生产环境禁止使用系统管理员账号！\n建议: 创建专用服务账号以降低安全风险"
        else:
            # 不是已知的系统管理员, 用户确实不存在
            logger.error(f"服务账号 {username} 不存在且不是已知的系统管理员")
            return False, f"服务账号 {username} 不存在\n\n请检查: \n  1. ldap.login_user 配置是否正确\n  2. LDAP目录中是否存在该用户\n  3. base_dn 配置是否包含该用户"
    
    def _is_system_admin(self, username: str) -> Tuple[bool, str]:
        """
        检查是否为系统管理员账号
        
        Args:
            username: 用户名
            
        Returns:
            (是否为系统管理员, 匹配原因)
        """
        config = get_config()
        system_admins = config.get('ldap.security.system_admins', {})
        
        # 获取完整的 login_user (可能是DN格式)
        login_user = config.get('ldap.login_user', '')
        
        # 1. 精确匹配检查
        exact_matches = system_admins.get('exact_matches', [])
        if username in exact_matches:
            return True, "精确匹配配置的系统管理员用户名"
        if login_user in exact_matches:
            return True, "精确匹配配置的系统管理员DN"
        
        # 2. 正则表达式模式匹配
        patterns = system_admins.get('patterns', [])
        for pattern in patterns:
            try:
                if re.search(pattern, login_user, re.IGNORECASE):
                    return True, f"匹配配置的模式: {pattern}"
            except re.error as e:
                logger.warning(f"无效的正则表达式模式 '{pattern}': {e}")
                continue
        
        # 3. 默认模式识别 (如果未配置任何规则, 使用默认规则)
        if not exact_matches and not patterns:
            default_patterns = [
                r'^cn=admin,dc=',
                r'^cn=Manager,dc=',
                r'^uid=root,',
            ]
            for pattern in default_patterns:
                if re.search(pattern, login_user, re.IGNORECASE):
                    return True, f"匹配默认系统管理员模式: {pattern}"
        
        return False, "不是系统管理员"
    
    def _check_dangerous_groups(self, group_dns: List[str], group_names: List[str]) -> List[str]:
        """
        检查是否属于危险组
        
        Returns:
            匹配的危险组列表
        """
        matches = []
        
        for group_config in self.dangerous_groups:
            if self._is_group_matched(group_config, group_dns, group_names):
                # 获取组的显示名称
                display_name = self._get_group_display_name(group_config)
                matches.append(display_name)
        
        return matches
    
    def _check_recommended_groups(self, group_dns: List[str], group_names: List[str]) -> bool:
        """
        检查是否属于推荐组
        
        Returns:
            是否属于任意推荐组
        """
        for group_config in self.recommended_groups:
            if self._is_group_matched(group_config, group_dns, group_names):
                return True
        
        return False
    
    def _is_group_matched(self, group_config, group_dns: List[str], group_names: List[str]) -> bool:
        """
        检查组配置是否匹配
        
        Args:
            group_config: 组配置 (可以是字符串或字典)
            group_dns: 用户所属的组DN列表
            group_names: 用户所属的组名列表
            
        Returns:
            是否匹配
        """
        # 如果是字符串,当作组名处理
        if isinstance(group_config, str):
            return group_config in group_names
        
        # 如果是字典,支持多种匹配方式
        if isinstance(group_config, dict):
            # 方式1: DN完整匹配
            if 'dn' in group_config:
                if group_config['dn'] in group_dns:
                    return True
            
            # 方式2: 组名匹配
            if 'name' in group_config:
                if group_config['name'] in group_names:
                    return True
            
            # 方式3: DN模式匹配 (正则)
            if 'pattern' in group_config:
                pattern = re.compile(group_config['pattern'], re.IGNORECASE)
                for dn in group_dns:
                    if pattern.match(dn):
                        return True
        
        return False
    
    def _get_group_display_name(self, group_config) -> str:
        """获取组的显示名称"""
        if isinstance(group_config, str):
            return group_config
        elif isinstance(group_config, dict):
            return group_config.get('name', group_config.get('dn', str(group_config)))
        else:
            return str(group_config)
    
    def _format_group_list(self, groups: List) -> str:
        """格式化组列表为字符串"""
        return ', '.join([self._get_group_display_name(g) for g in groups])
