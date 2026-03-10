# -*- coding: utf-8 -*-
"""
手机号解析器

支持从多个数据源获取用户手机号，支持可配置的优先级和字段映射
"""
from typing import Optional, Tuple, List
from utils.config import get_config
from utils.logger_factory import get_logger
from utils.ldap.factory import LDAPFactory
from utils.format_username import format2username
from .errors import SMSException, SMSErrorCode

logger = get_logger(__name__)


class MobileResolver:
    """
    手机号解析器
    
    支持：
    1. 多数据源（OAuth、LDAP）
    2. 可配置的查找顺序
    3. 可配置的字段名映射
    4. 手机号格式验证
    """
    
    def __init__(self):
        """初始化手机号解析器"""
        self.config = get_config()
        
        # 加载手机号映射配置
        self.mobile_mapping = self.config.get('sms.mobile_mapping', {})
        self.sources = self.mobile_mapping.get('sources', [])
        
        if not self.sources:
            logger.warning("未配置手机号数据源，使用默认配置：oauth → ldap")
            self.sources = [
                {'type': 'ldap', 'field': 'mobile'},
                {'type': 'oauth', 'field': 'mobile'},
            ]
    
    def resolve_mobile(
        self, 
        username: str, 
        oauth_user_info: Optional[dict] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """
        解析用户手机号
        
        Args:
            username: 用户名
            oauth_user_info: OAuth返回的用户信息（可选）
            
        Returns:
            Tuple[成功, 手机号或错误消息, 数据源]
            
        Raises:
            SMSException: 解析失败时抛出
        """
        # 格式化用户名
        fmt_status, formatted_username = format2username(username)
        if not fmt_status:
            raise SMSException(
                SMSErrorCode.INVALID_MOBILE,
                f"用户名格式不正确: {formatted_username}",
                "resolve_mobile"
            )
        username = formatted_username
        
        logger.debug(f"开始解析手机号: username={username}, 数据源顺序={[s['type'] for s in self.sources]}")
        
        for source_config in self.sources:
            source_type = source_config.get('type')
            field_name = source_config.get('field', 'mobile')
            
            try:
                if source_type == 'oauth':
                    mobile = self._resolve_from_oauth(oauth_user_info, field_name)
                elif source_type == 'ldap':
                    mobile = self._resolve_from_ldap(username, field_name)
                else:
                    logger.warning(f"未知的数据源类型: {source_type}")
                    continue
                
                if mobile:
                    # 验证手机号格式
                    if self._validate_mobile(mobile):
                        logger.info(f"手机号解析成功: username={username}, source={source_type}")
                        return True, mobile, source_type
                    else:
                        logger.warning(f"手机号格式不正确: {mobile}, source={source_type}")
                        continue
                        
            except Exception as e:
                logger.warning(f"从{source_type}获取手机号失败: {e}")
                continue
        
        # 所有数据源都失败
        logger.error(f"无法获取手机号: username={username}")
        raise SMSException(
            SMSErrorCode.MOBILE_NOT_FOUND,
            "无法获取手机号，请联系管理员",
            "resolve_mobile"
        )
    
    def _resolve_from_oauth(
        self, 
        oauth_user_info: Optional[dict],
        field_name: str
    ) -> Optional[str]:
        """
        从OAuth用户信息中获取手机号
        
        Args:
            oauth_user_info: OAuth返回的用户信息
            field_name: 手机号字段名
            
        Returns:
            手机号或None
        """
        if not oauth_user_info:
            logger.debug("OAuth用户信息为空")
            return None
        
        # 支持点号路径（如 contact.mobile）
        mobile = self._get_nested_value(oauth_user_info, field_name)
        
        if mobile:
            logger.debug(f"从OAuth获取到手机号: field={field_name}")
            return str(mobile)
        
        logger.debug(f"OAuth中未找到手机号字段: {field_name}")
        return None
    
    def _resolve_from_ldap(self, username: str, field_name: str) -> Optional[str]:
        """
        从LDAP中获取手机号
        
        Args:
            username: 用户名
            field_name: LDAP属性名
            
        Returns:
            手机号或None
        """
        try:
            adapter = LDAPFactory.create_adapter()
            
            # 查询用户属性
            attributes = [field_name]
            status, user_info = adapter.search_user(username, attributes=attributes)

            logger.debug(f"LDAP查询用户信息: username={username}, attributes={attributes}, result={user_info}")

            if not status:
                logger.debug(f"LDAP查询用户信息失败: username={username}", exc_info=True)
                return None

            
            if not user_info:
                logger.debug(f"LDAP中未找到用户: {username}", exc_info=True)
                return None
            
            # 获取手机号属性
            mobile = user_info.get(field_name)
            
            if mobile:
                # LDAP属性可能返回列表
                if isinstance(mobile, list):
                    mobile = mobile[0] if mobile else None
                
                if mobile:
                    logger.debug(f"从LDAP获取到手机号: field={field_name}")
                    return str(mobile)
            
            logger.debug(f"LDAP中未找到手机号字段: {field_name}", exc_info=True)
            return None
            
        except Exception as e:
            # 仅记录警告，继续尝试下一个数据源
            logger.warning(f"从LDAP获取手机号失败: {e}", exc_info=True)
            return None
    
    def _get_nested_value(self, data: dict, path: str) -> Optional[any]:
        """
        从嵌套字典中获取值（支持点号路径）
        
        Args:
            data: 字典
            path: 路径（如 "contact.mobile"）
            
        Returns:
            值或None
        """
        if '.' not in path:
            return data.get(path)
        
        keys = path.split('.')
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        
        return value
    
    def _validate_mobile(self, mobile: str) -> bool:
        """
        验证手机号格式
        
        Args:
            mobile: 手机号
            
        Returns:
            是否有效
        """
        if not mobile:
            return False
        
        # 清理可能的空格、短横线
        mobile = str(mobile).replace(' ', '').replace('-', '')
        
        # 中国大陆手机号：1开头，11位数字
        if mobile.startswith('1') and len(mobile) == 11 and mobile.isdigit():
            return True
        
        # 国际号码：+86开头，后跟11位数字
        if mobile.startswith('+86') and len(mobile) == 14:
            return mobile[3:].isdigit()
        
        # 其他格式（如企业短号）
        # 这里可以根据实际情况添加更多规则
        if len(mobile) >= 8 and mobile.isdigit():
            logger.debug(f"手机号格式不标准但可接受: {mobile}")
            return True
        
        logger.debug(f"手机号格式无效: {mobile}")
        return False
    
    def format_mobile(self, mobile: str) -> str:
        """
        格式化手机号（标准化）
        
        Args:
            mobile: 原始手机号
            
        Returns:
            格式化后的手机号
        """
        # 清理空格和短横线
        mobile = str(mobile).replace(' ', '').replace('-', '')
        
        # 移除+86前缀（如果有）
        if mobile.startswith('+86'):
            mobile = mobile[3:]
        elif mobile.startswith('86') and len(mobile) == 13:
            mobile = mobile[2:]
        
        return mobile
    
    def get_configured_sources(self) -> List[dict]:
        """
        获取已配置的数据源列表
        
        Returns:
            数据源配置列表
        """
        return self.sources
    
    def validate_source_config(self, source_config: dict) -> Tuple[bool, str]:
        """
        验证数据源配置
        
        Args:
            source_config: 数据源配置
            
        Returns:
            Tuple[是否有效, 错误消息]
        """
        if 'type' not in source_config:
            return False, "数据源配置缺少 'type' 字段"
        
        source_type = source_config['type']
        if source_type not in ['oauth', 'ldap']:
            return False, f"不支持的数据源类型: {source_type}"
        
        if 'field' not in source_config:
            logger.warning(f"数据源 {source_type} 未指定字段名，将使用默认值 'mobile'")
        
        return True, ""
