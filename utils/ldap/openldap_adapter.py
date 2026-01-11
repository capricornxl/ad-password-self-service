# -*- coding: utf-8 -*-
"""
OpenLDAP适配器实现
将OpenLDAP操作封装为统一的LDAP接口
"""

from ldap3 import Server, Connection, ALL, SIMPLE, MODIFY_REPLACE, MODIFY_DELETE, MODIFY_ADD
from ldap3.core.results import RESULT_SUCCESS
from ldap3.core.exceptions import (
    LDAPInvalidCredentialsResult,
    LDAPException as Ldap3Exception,
    LDAPSocketOpenError
)
from ldap3.utils.dn import safe_dn
import re
import hashlib
import base64
import os
from typing import Tuple, List, Dict, Optional
from .ldap_escape import LDAPEscape
from .adapter import LDAPAdapter
from .errors import LDAPException, LDAPErrorCode
from .error_messages import (
    get_ldap_error_message,
    get_ppolicy_error_message,
    category_to_error_code
)
from utils.config import get_config
from utils.logger_factory import get_logger
from utils.log_sanitizer import LogSanitizer
logger = get_logger(__name__)


class OpenLDAPAdapter(LDAPAdapter):
    """OpenLDAP适配器"""
    
    def __init__(self):
        """初始化OpenLDAP适配器"""
        super().__init__()
        
        config = get_config()
        self.ldap_type = 'openldap'
        
        # 通用LDAP配置
        self.ldap_host = config.get('ldap.host')
        self.use_ssl = config.get('ldap.use_ssl', True)
        self.port = config.get('ldap.port', 636)
        self.base_dn = config.get('ldap.base_dn', '')
        self.connection_timeout = config.get('ldap.connection_timeout', 10)
        self.response_timeout = config.get('ldap.response_timeout', 30)
        
        # 服务账号凭据
        self.login_user = config.get('ldap.login_user')
        self.login_password = config.get('ldap.login_password')
        
        # OpenLDAP认证方式 (通常是SIMPLE)
        auth_type = config.get('ldap.openldap.authentication', 'simple').lower()
        self.authentication = SIMPLE  # OpenLDAP主要使用SIMPLE认证
        
        # OpenLDAP属性映射 (支持配置化)
        attr_config = config.get('ldap.openldap.attributes', {})
        self.password_attr = attr_config.get('password', 'userPassword')
        self.username_attr = attr_config.get('username', 'uid')
        self.lockout_attr = attr_config.get('lockout_time', 'pwdAccountLockedTime')
        self.member_of_attr = attr_config.get('member_of', 'memberOf')
        self.object_class = attr_config.get('object_class', 'inetOrgPerson')
        
        # 密码hash算法 (支持配置化)
        self.password_hash = config.get('ldap.openldap.password_hash', 'ssha').upper()
        
        # 搜索过滤器 (支持配置化，支持多 objectClass)
        # 默认支持 inetOrgPerson、posixAccount、shadowAccount 三种 objectClass
        # 格式: (|(&(objectClass=inetOrgPerson)(uid={}))(&(objectClass=posixAccount)(uid={}))(&(objectClass=shadowAccount)(uid={})))
        self.search_filter = config.get(
            'ldap.search_filter',
            f'(|(&(objectClass=inetOrgPerson)({self.username_attr}={{}}))(&(objectClass=posixAccount)({self.username_attr}={{}}))(&(objectClass=shadowAccount)({self.username_attr}={{}})))'
        )
        self.search_attributes = config.get(
            'ldap.search_attributes',
            [self.username_attr, 'mail', 'cn', 'displayName']
        )
        
        # 用户DN模板 (可选)
        self.user_dn_template = config.get('ldap.user_dn_template', '')
        
        # ppolicy配置
        ppolicy_config = config.get('ldap.openldap.ppolicy', {})
        self.ppolicy_enabled = ppolicy_config.get('enabled', True)
        self.ppolicy_dn = ppolicy_config.get('policy_dn', '')
        
        # memberOf overlay检测
        self.memberof_overlay = config.get('ldap.openldap.memberof_overlay', True)
        
        # 账号状态配置（与AD使用统一结构）
        account_status = config.get('ldap.openldap.account_status', {})
        
        # =======================================================================
        # 新版多机制检测配置
        # =======================================================================
        
        # 锁定检测配置（按优先级尝试）
        self.lock_detection_configs = account_status.get('lock_detection', [
            {
                'attribute': 'pwdAccountLockedTime',
                'mechanism': 'ppolicy',
                'check': 'exists',
                'unlock_action': 'delete'
            }
        ])
        
        # 禁用检测配置（按优先级尝试）
        self.disable_detection_configs = account_status.get('disable_detection', [
            {
                'attribute': 'nsAccountLock',
                'mechanism': '389ds',
                'check': 'value',
                'disabled_values': ['true', 'TRUE', '1']
            }
        ])
        
        # 密码属性配置
        password_config = account_status.get('password', {})
        self.password_attributes = password_config.get('attributes', ['userPassword'])
        self.password_auto_add = password_config.get('auto_add', True)
        self.password_hash_algorithm = password_config.get('hash_algorithm', 'ssha').upper()
        
        # 是否启用自动检测机制
        self.auto_detect_mechanism = account_status.get('auto_detect_mechanism', True)
        
        # =======================================================================
        # 向后兼容配置（旧版本配置格式）
        # =======================================================================
        self.enabled_codes = account_status.get('enabled', [])  # OpenLDAP通常无统一启用标志
        self.disabled_codes = account_status.get('disabled', ['true'])  # 禁用标志值列表
        self.locked_codes = account_status.get('locked', ['exists'])  # 锁定检查方式
        self.password_expired_codes = account_status.get('password_expired', [])  # 通常依赖ppolicy
        
        # 属性配置（向后兼容）
        self.disabled_attribute = account_status.get('disabled_attribute', 'nsAccountLock')
        self.locked_attribute = account_status.get('locked_attribute', 'pwdAccountLockedTime')
        
        # 如果新配置为空，使用旧配置构建默认值
        if not self.lock_detection_configs or (len(self.lock_detection_configs) == 1 and
                self.lock_detection_configs[0].get('attribute') == 'pwdAccountLockedTime' and
                self.locked_attribute != 'pwdAccountLockedTime'):
            # 使用旧配置构建锁定检测配置
            self.lock_detection_configs = [
                {
                    'attribute': self.locked_attribute,
                    'mechanism': 'legacy',
                    'check': 'exists' if 'exists' in self.locked_codes else 'value',
                    'unlock_action': 'delete'
                }
            ]
        
        if not self.disable_detection_configs or (len(self.disable_detection_configs) == 1 and
                self.disable_detection_configs[0].get('attribute') == 'nsAccountLock' and
                self.disabled_attribute != 'nsAccountLock'):
            # 使用旧配置构建禁用检测配置
            self.disable_detection_configs = [
                {
                    'attribute': self.disabled_attribute,
                    'mechanism': 'legacy',
                    'check': 'value',
                    'disabled_values': self.disabled_codes
                }
            ]
        
        # TLS配置（与AD使用相同的加载逻辑）
        self.tls_config = self._load_tls_config(config)
        
        logger.debug(f"OpenLDAP适配器初始化完成: host={self.ldap_host}, hash={self.password_hash}, tls_validate={self.tls_config.get('validate')}")
    
    def _load_tls_config(self, config) -> Dict:
        """加载TLS配置（与AD适配器共享相同逻辑）
        
        Args:
            config: 配置管理器实例
            
        Returns:
            TLS配置字典
        """
        from ldap3 import Tls
        import ssl
        import os
        from pathlib import Path
        
        tls_config = {}
        
        # 获取TLS配置段（从openldap配置读取）
        validate_mode = config.get('ldap.openldap.tls.validate', 'required').lower()
        
        # 映射验证级别到ssl常量
        if validate_mode == 'none':
            tls_config['validate'] = ssl.CERT_NONE
            logger.warning("OpenLDAP TLS证书验证已禁用（validate=none），不推荐用于生产环境")
        elif validate_mode == 'optional':
            tls_config['validate'] = ssl.CERT_OPTIONAL
            logger.warning("OpenLDAP TLS证书验证设置为可选（validate=optional）")
        else:  # 'required'
            tls_config['validate'] = ssl.CERT_REQUIRED
            logger.debug("OpenLDAP TLS证书验证已启用（validate=required）")
        
        # CA证书文件
        ca_file = config.get('ldap.openldap.tls.ca_certs_file', '').strip()
        if ca_file:
            # 处理相对路径
            if not ca_file.startswith('/') and not (len(ca_file) > 1 and ca_file[1] == ':'):
                # 相对路径，基于项目根目录
                project_root = Path(__file__).parent.parent.parent
                ca_file = str(project_root / ca_file)
            
            if os.path.exists(ca_file):
                tls_config['ca_certs_file'] = ca_file
                logger.debug(f"使用CA证书文件: {ca_file}")
            else:
                logger.error(f"CA证书文件不存在: {ca_file}")
                raise LDAPException(
                    LDAPErrorCode.CONFIGURATION_ERROR,
                    f"CA证书文件不存在: {ca_file}",
                    'openldap'
                )
        
        # CA证书目录
        ca_path = config.get('ldap.openldap.tls.ca_certs_path', '').strip()
        if ca_path:
            if not ca_path.startswith('/') and not (len(ca_path) > 1 and ca_path[1] == ':'):
                project_root = Path(__file__).parent.parent.parent
                ca_path = str(project_root / ca_path)
            
            if os.path.exists(ca_path):
                tls_config['ca_certs_path'] = ca_path
                logger.debug(f"使用CA证书目录: {ca_path}")
            else:
                logger.warning(f"CA证书目录不存在: {ca_path}")
        
        # 客户端证书（双向TLS）
        client_cert = config.get('ldap.openldap.tls.local_certificate_file', '').strip()
        if client_cert:
            if not client_cert.startswith('/') and not (len(client_cert) > 1 and client_cert[1] == ':'):
                project_root = Path(__file__).parent.parent.parent
                client_cert = str(project_root / client_cert)
            
            if os.path.exists(client_cert):
                tls_config['local_certificate_file'] = client_cert
                logger.debug(f"使用客户端证书: {client_cert}")
            else:
                logger.error(f"客户端证书文件不存在: {client_cert}")
        
        # 客户端私钥
        private_key = config.get('ldap.openldap.tls.local_private_key_file', '').strip()
        if private_key:
            if not private_key.startswith('/') and not (len(private_key) > 1 and private_key[1] == ':'):
                project_root = Path(__file__).parent.parent.parent
                private_key = str(project_root / private_key)
            
            if os.path.exists(private_key):
                tls_config['local_private_key_file'] = private_key
                
                # 私钥密码
                key_password = config.get('ldap.openldap.tls.local_private_key_password', '').strip()
                if key_password:
                    tls_config['local_private_key_password'] = key_password
                
                logger.debug(f"使用客户端私钥: {private_key}")
            else:
                logger.error(f"客户端私钥文件不存在: {private_key}")
        
        # TLS版本
        tls_version = config.get('ldap.openldap.tls.version', '').strip().upper()
        if tls_version:
            version_map = {
                'TLSV1': ssl.PROTOCOL_TLSv1,
                'TLSV1.1': ssl.PROTOCOL_TLSv1_1,
                'TLSV1.2': ssl.PROTOCOL_TLSv1_2,
            }
            # TLSv1.3 需要Python 3.7+
            if hasattr(ssl, 'PROTOCOL_TLSv1_3'):
                version_map['TLSV1.3'] = ssl.PROTOCOL_TLSv1_3
            
            if tls_version.replace('.', '') in version_map:
                tls_config['version'] = version_map[tls_version.replace('.', '')]
                logger.debug(f"使用TLS版本: {tls_version}")
            else:
                logger.warning(f"不支持的TLS版本: {tls_version}，将使用默认版本")
        
        # 主机名验证
        validate_hostname = config.get('ldap.openldap.tls.validate_hostname', True)
        if not validate_hostname:
            tls_config['valid_names'] = []  # 禁用主机名验证
            logger.warning("主机名验证已禁用")
        
        # 自定义加密套件
        ciphers = config.get('ldap.openldap.tls.ciphers', '').strip()
        if ciphers:
            tls_config['ciphers'] = ciphers
            logger.debug(f"使用自定义加密套件: {ciphers}")
        
        return tls_config
    
    # ========== 账号状态检测方法 ==========
    
    def detect_lock_mechanism(self, username: str) -> Optional[Dict]:
        """自动检测账号使用的锁定机制
        
        根据配置的 lock_detection 列表，按优先级尝试检测用户账号使用的锁定机制。
        
        Args:
            username: 用户名
            
        Returns:
            检测到的锁定机制配置字典，如果未检测到则返回 None
            例如: {'attribute': 'pwdAccountLockedTime', 'mechanism': 'ppolicy', 'check': 'exists', 'unlock_action': 'delete'}
        """
        if not self.auto_detect_mechanism:
            # 如果禁用自动检测，返回第一个配置
            return self.lock_detection_configs[0] if self.lock_detection_configs else None
        
        # 确保连接
        if not self.is_connected():
            self.connect()
        
        # 获取用户DN
        success, user_dn = self.get_user_dn(username)
        if not success:
            logger.warning(f"无法检测锁定机制：找不到用户 {username}")
            return None
        
        try:
            for config in self.lock_detection_configs:
                attr = config['attribute']
                
                # 搜索该属性
                self.conn.search(
                    user_dn,
                    '(objectClass=*)',
                    attributes=[attr]
                )
                
                if self.conn.entries:
                    entry = self.conn.entries[0]
                    
                    # 检查属性是否存在
                    if attr in entry.entry_attributes:
                        value = getattr(entry, attr, None)
                        
                        if config['check'] == 'exists':
                            # exists 检查：属性存在即表示锁定
                            if value is not None and value.value is not None:
                                logger.debug(f"检测到锁定机制: {config['mechanism']} (属性 {attr} 存在)")
                                return config
                        elif config['check'] == 'value':
                            # value 检查：属性值在 locked_values 列表中
                            if value is not None and value.value is not None:
                                locked_values = config.get('locked_values', [])
                                if str(value.value).lower() in [v.lower() for v in locked_values]:
                                    logger.debug(f"检测到锁定机制: {config['mechanism']} (属性 {attr}={value.value})")
                                    return config
            
            logger.debug(f"未检测到锁定机制: 用户 {username}")
            return None
            
        except Exception as e:
            logger.error(f"检测锁定机制时发生错误: {e}")
            return None
    
    def detect_disable_mechanism(self, username: str) -> Optional[Dict]:
        """自动检测账号使用的禁用机制
        
        根据配置的 disable_detection 列表，按优先级尝试检测用户账号使用的禁用机制。
        
        Args:
            username: 用户名
            
        Returns:
            检测到的禁用机制配置字典，如果未检测到则返回 None
            例如: {'attribute': 'nsAccountLock', 'mechanism': '389ds', 'check': 'value', 'disabled_values': ['true']}
        """
        if not self.auto_detect_mechanism:
            # 如果禁用自动检测，返回第一个配置
            return self.disable_detection_configs[0] if self.disable_detection_configs else None
        
        # 确保连接
        if not self.is_connected():
            self.connect()
        
        # 获取用户DN
        success, user_dn = self.get_user_dn(username)
        if not success:
            logger.warning(f"无法检测禁用机制：找不到用户 {username}")
            return None
        
        try:
            for config in self.disable_detection_configs:
                attr = config['attribute']
                
                # 搜索该属性
                self.conn.search(
                    user_dn,
                    '(objectClass=*)',
                    attributes=[attr]
                )
                
                if self.conn.entries:
                    entry = self.conn.entries[0]
                    
                    # 检查属性是否存在
                    if attr in entry.entry_attributes:
                        value = getattr(entry, attr, None)
                        
                        if config['check'] == 'value':
                            # value 检查：属性值在 disabled_values 列表中
                            if value is not None and value.value is not None:
                                disabled_values = config.get('disabled_values', [])
                                if str(value.value).lower() in [v.lower() for v in disabled_values]:
                                    logger.debug(f"检测到禁用机制: {config['mechanism']} (属性 {attr}={value.value})")
                                    return config
                        
                        elif config['check'] == 'expire_date':
                            # expire_date 检查：检查日期是否已过期（shadowExpire）
                            if value is not None and value.value is not None:
                                try:
                                    import time
                                    # shadowExpire 是从 1970-01-01 起的天数
                                    expire_days = int(value.value)
                                    current_days = int(time.time() / 86400)
                                    if expire_days > 0 and expire_days < current_days:
                                        logger.debug(f"检测到禁用机制: {config['mechanism']} (属性 {attr} 已过期)")
                                        return config
                                except (ValueError, TypeError):
                                    pass
            
            logger.debug(f"未检测到禁用机制: 用户 {username}")
            return None
            
        except Exception as e:
            logger.error(f"检测禁用机制时发生错误: {e}")
            return None
    
    # ========== 连接管理 ==========
    
    def connect(self) -> Tuple[bool, str]:
        """建立OpenLDAP连接"""
        try:
            # 创建服务器对象
            if self.server is None:
                from ldap3 import Tls
                
                # 构建TLS对象
                tls_obj = None
                if self.use_ssl and self.tls_config:
                    try:
                        tls_obj = Tls(**self.tls_config)
                        logger.debug(f"TLS对象创建成功: validate={self.tls_config.get('validate')}")
                    except Exception as e:
                        logger.error(f"TLS对象创建失败: {e}")
                        raise LDAPException(
                            LDAPErrorCode.CONFIGURATION_ERROR,
                            f"TLS配置错误: {str(e)}",
                            'openldap',
                            e
                        )
                
                self.server = Server(
                    host=self.ldap_host,
                    use_ssl=self.use_ssl,
                    port=self.port,
                    connect_timeout=self.connection_timeout,
                    get_info=ALL,
                    tls=tls_obj
                )
                logger.debug(f"OpenLDAP服务器对象创建成功: {self.ldap_host}:{self.port}, TLS={'启用' if tls_obj else '未配置'}")
            
            # 创建连接对象
            if self.conn is None or not self.conn.bound:
                # OpenLDAP使用DN绑定
                bind_dn = self.login_user  # 应该是完整DN,如: cn=admin,dc=company,dc=com
                
                self.conn = Connection(
                    self.server,
                    user=bind_dn,
                    password=self.login_password,
                    authentication=self.authentication,
                    auto_bind=True,
                    raise_exceptions=True,
                    receive_timeout=self.response_timeout
                )
                logger.info(f"OpenLDAP连接建立成功: {bind_dn}")
            
            return True, "OpenLDAP连接成功"
        
        except LDAPInvalidCredentialsResult as e:
            logger.error(f"OpenLDAP认证失败: {e}")
            raise LDAPException(
                LDAPErrorCode.BIND_FAILED,
                "OpenLDAP服务账号认证失败",
                'openldap',
                e
            )
        except LDAPSocketOpenError as e:
            logger.error(f"OpenLDAP连接失败: {e}")
            raise LDAPException(
                LDAPErrorCode.CONNECTION_FAILED,
                f"无法连接到OpenLDAP服务器 {self.ldap_host}:{self.port}",
                'openldap',
                e
            )
        except Ldap3Exception as e:
            logger.error(f"OpenLDAP连接异常: {e}")
            raise LDAPException(
                LDAPErrorCode.CONNECTION_FAILED,
                f"OpenLDAP连接失败: {str(e)}",
                'openldap',
                e
            )
    
    def disconnect(self):
        """断开OpenLDAP连接"""
        if self.conn and self.conn.bound:
            try:
                self.conn.unbind()
                logger.debug("OpenLDAP连接已断开")
            except Exception as e:
                logger.warning(f"OpenLDAP断开连接时发生异常: {e}")
        self.conn = None
    
    # ========== 认证相关 ==========
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """验证用户凭据"""
        try:
            # 创建临时连接进行认证
            if self.server is None:
                self.connect()  # 确保server已创建
            
            # 获取用户DN
            success, user_dn = self.get_user_dn(username)
            if not success:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'openldap'
                )
            
            # 尝试绑定认证
            auth_conn = Connection(
                self.server,
                user=user_dn,
                password=password,
                authentication=SIMPLE,
                auto_bind=True,
                raise_exceptions=True
            )
            auth_conn.unbind()
            
            logger.info(f"用户 {username} 认证成功")
            return True, "认证成功"
        
        except LDAPInvalidCredentialsResult as e:
            # OpenLDAP的错误码比较简单,需要额外查询账号状态
            error_code, error_msg = self._check_auth_failure_reason(username, e)
            logger.warning(f"用户 {username} 认证失败: {error_msg}")
            raise LDAPException(error_code, error_msg, 'openldap', e)
        
        except LDAPException:
            raise
        
        except Exception as e:
            logger.error(f"用户 {username} 认证异常: {e}")
            raise LDAPException(
                LDAPErrorCode.UNKNOWN_ERROR,
                f"认证失败: {str(e)}",
                'openldap',
                e
            )
    
    def _check_auth_failure_reason(self, username: str, error) -> Tuple[int, str]:
        """
        检查OpenLDAP认证失败的原因
        
        OpenLDAP的result code 49 (invalidCredentials) 可能是多种原因:
        - 密码错误
        - 账号锁定
        - 账号禁用
        需要额外查询账号状态来确定
        
        同时检查 ppolicy 响应控制以获取更详细的错误信息
        """
        try:
            # 尝试从 ppolicy 响应控制获取错误信息
            if hasattr(error, 'controls'):
                ppolicy_control = error.controls.get('1.3.6.1.4.1.42.2.27.8.5.1')
                if ppolicy_control and hasattr(ppolicy_control, 'error'):
                    ppolicy_error = get_ppolicy_error_message(ppolicy_control.error, lang='zh')
                    if ppolicy_error:
                        return category_to_error_code(ppolicy_error['category']), ppolicy_error['message']
            
            # 检查账号是否锁定
            _, is_locked = self.is_account_locked(username)
            if is_locked:
                return LDAPErrorCode.ACCOUNT_LOCKED, "账号已锁定"
            
            # 检查账号是否禁用 (OpenLDAP可能没有统一的禁用标志)
            # 这里简化处理,返回密码错误
            return LDAPErrorCode.INVALID_CREDENTIALS, "账号或密码不正确"
        
        except Exception as e:
            # 如果查询失败,记录日志并返回通用错误
            logger.warning(f"检查认证失败原因时发生异常: {e}")
            return LDAPErrorCode.INVALID_CREDENTIALS, "认证失败,请确认账号和密码"
    
    # ========== 密码管理 ==========
    
    def reset_password(self, username: str, new_password: str,
                      old_password: str = None) -> Tuple[bool, str]:
        """
        重置用户密码 (管理员操作)
        
        检测userPassword属性是否存在:
        - 存在则使用MODIFY_REPLACE
        - 不存在则使用MODIFY_ADD (避免namingViolation错误)
        """
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 获取用户DN
            success, user_dn = self.get_user_dn(username)
            if not success:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'openldap'
                )
            
            # hash密码
            hashed_password = self._hash_password(new_password)
            
            # 检查userPassword属性是否存在
            # 如果用户条目中没有该属性，需要使用MODIFY_ADD而非MODIFY_REPLACE
            self.conn.search(
                user_dn,
                '(objectClass=*)',
                attributes=[self.password_attr]
            )
            
            # 判断属性是否存在，选择正确的修改操作
            password_attr_exists = False
            if self.conn.entries:
                entry = self.conn.entries[0]
                # 检查条目是否有password属性且该属性有值
                if hasattr(entry, self.password_attr):
                    attr_value = getattr(entry, self.password_attr)
                    if attr_value and str(attr_value).strip():
                        password_attr_exists = True
            
            if password_attr_exists:
                # 属性存在，使用REPLACE
                modify_op = MODIFY_REPLACE
                logger.debug(f"用户 {username} 密码属性已存在，使用 MODIFY_REPLACE")
            else:
                # 属性不存在，使用ADD
                modify_op = MODIFY_ADD
                logger.debug(f"用户 {username} 密码属性不存在，使用 MODIFY_ADD")
            
            # 执行修改
            result = self.conn.modify(
                user_dn,
                {self.password_attr: [(modify_op, [hashed_password])]}
            )
            
            # 检查结果
            if self.conn.result['result'] == RESULT_SUCCESS:
                logger.info(f"用户 {username} 密码重置成功 (管理员操作)")
                return True, "密码重置成功"
            else:
                error_code = self.conn.result.get('result', '未知')
                error_msg = self.conn.result.get('description', '未知错误')
                
                # 详细错误诊断
                logger.error(f"===== OpenLDAP修改错误详情 =====")
                logger.error(f"  用户: {username}")
                logger.error(f"  错误码: {error_code}")
                logger.error(f"  错误描述: {error_msg}")
                logger.error(f"  ================================")
                
                # 尝试从标准 LDAP 错误码获取友好消息
                ldap_error_info = get_ldap_error_message(error_code, lang='zh')
                if ldap_error_info:
                    logger.warning(f"用户 {username} 密码重置失败: {ldap_error_info['message']}")
                    raise LDAPException(
                        category_to_error_code(ldap_error_info['category']),
                        ldap_error_info['message'],
                        'openldap',
                        details=self.conn.result
                    )
                
                # 未匹配到已知错误码，返回原始错误
                logger.error(f"用户 {username} 密码重置失败: {error_msg}")
                raise LDAPException(
                    LDAPErrorCode.MODIFY_FAILED,
                    f"密码重置失败: {error_msg}",
                    'openldap',
                    details=self.conn.result
                )
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"密码重置异常: {e}")
            raise LDAPException(
                LDAPErrorCode.MODIFY_FAILED,
                f"密码重置失败: {str(e)}",
                'openldap',
                e
            )
    
    def change_password(self, username: str, old_password: str,
                       new_password: str) -> Tuple[bool, str]:
        """
        用户修改自己的密码 (需要提供旧密码)
        
        流程：
        1. 使用用户凭据认证（验证旧密码正确性）
        2. 检查账号状态
        3. 使用管理员连接执行密码修改
        4. 解锁账号（如需要）
        """
        user_conn = None
        try:
            # ========== 步骤1：使用用户凭据认证（验证旧密码正确性）==========
            # 首先验证旧密码
            self.authenticate(username, old_password)
            
            logger.info(f"用户 {username} 旧密码验证成功（用户认证通过）")
            
            # ========== 步骤2：确保管理员连接可用 ==========
            if not self.is_connected():
                self.connect()
            
            # 获取用户DN
            success, user_dn = self.get_user_dn(username)
            if not success:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'openldap'
                )
            
            # ========== 步骤3：使用管理员连接执行密码修改 ==========
            # hash新密码
            hashed_password = self._hash_password(new_password)
            
            # 检查userPassword属性是否存在
            self.conn.search(
                user_dn,
                '(objectClass=*)',
                attributes=[self.password_attr]
            )
            
            # 判断属性是否存在，选择正确的修改操作
            password_attr_exists = False
            if self.conn.entries:
                entry = self.conn.entries[0]
                if hasattr(entry, self.password_attr):
                    attr_value = getattr(entry, self.password_attr)
                    if attr_value and str(attr_value).strip():
                        password_attr_exists = True
            
            if password_attr_exists:
                modify_op = MODIFY_REPLACE
                logger.debug(f"用户 {username} 密码属性已存在，使用 MODIFY_REPLACE（管理员执行）")
            else:
                modify_op = MODIFY_ADD
                logger.debug(f"用户 {username} 密码属性不存在，使用 MODIFY_ADD（管理员执行）")
            
            # 使用管理员连接修改密码
            result = self.conn.modify(
                user_dn,
                {self.password_attr: [(modify_op, [hashed_password])]}
            )
            
            if result:
                logger.info(f"用户 {username} 密码修改成功（管理员执行）")
                
                # ========== 步骤4：检查并解锁账号（如需要）==========
                try:
                    _, is_locked = self.is_account_locked(username)
                    if is_locked:
                        logger.info(f"检测到用户 {username} 账号已锁定，尝试解锁")
                        self.unlock_account(username)
                        logger.info(f"用户 {username} 账号已解锁")
                except Exception as unlock_e:
                    # 解锁失败不影响密码修改结果，仅记录警告
                    logger.warning(f"解锁账号失败（密码已修改）: {unlock_e}")
                
                return True, "密码修改成功"
            else:
                # 获取实际错误信息
                error_msg = self.conn.result.get('description', '未知错误')
                error_code = self.conn.result.get('result', '未知')
                
                # 详细错误诊断
                logger.error(f"===== 管理员密码修改错误详情 =====")
                logger.error(f"  用户: {username}")
                logger.error(f"  错误码: {error_code}")
                logger.error(f"  错误描述: {error_msg}")
                logger.error(f"  完整结果: {self.conn.result}")
                logger.error(f"  ================================")
                
                # 1. 尝试从 ppolicy 响应控制获取错误信息
                if hasattr(self.conn.result, 'controls'):
                    ppolicy_control = self.conn.result.controls.get('1.3.6.1.4.1.42.2.27.8.5.1')
                    if ppolicy_control and hasattr(ppolicy_control, 'error'):
                        ppolicy_error = get_ppolicy_error_message(ppolicy_control.error, lang='zh')
                        if ppolicy_error:
                            logger.warning(f"用户 {username} 密码修改失败 (ppolicy): {ppolicy_error['message']}")
                            raise LDAPException(
                                category_to_error_code(ppolicy_error['category']),
                                ppolicy_error['message'],
                                'openldap',
                                details=self.conn.result
                            )
                
                # 2. 尝试从标准 LDAP 错误码获取友好消息
                ldap_error_info = get_ldap_error_message(error_code, lang='zh')
                if ldap_error_info:
                    logger.warning(f"用户 {username} 密码修改失败: {ldap_error_info['message']}")
                    raise LDAPException(
                        category_to_error_code(ldap_error_info['category']),
                        ldap_error_info['message'],
                        'openldap',
                        details=self.conn.result
                    )
                
                # 3. 未匹配到已知错误码，返回原始错误
                logger.error(f"用户 {username} 密码修改失败: {error_msg}")
                raise LDAPException(
                    LDAPErrorCode.MODIFY_FAILED,
                    f"密码修改失败: {error_msg}",
                    'openldap',
                    details=self.conn.result
                )
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"密码修改异常: {e}")
            raise LDAPException(
                LDAPErrorCode.MODIFY_FAILED,
                f"密码修改失败: {str(e)}",
                'openldap',
                e
            )
    
    def _hash_password(self, password: str) -> str:
        """
        hash密码
        
        支持的hash算法:
        - SSHA: Salted SHA-1 (推荐)
        - SHA: SHA-1
        - MD5: MD5 (不推荐)
        - ARGON2: Argon2 (现代安全哈希，推荐)
        - BCRYPT: bcrypt (现代安全哈希，推荐)
        - CRYPT: Unix crypt
        - PLAIN: 明文 (仅测试用)
        """
        algorithm = self.password_hash.upper()
        
        if algorithm == 'SSHA':
            return self._ssha_hash(password)
        elif algorithm == 'SHA':
            return self._sha_hash(password)
        elif algorithm == 'MD5':
            return self._md5_hash(password)
        elif algorithm == 'PLAIN':
            return password  # 明文,不推荐
        elif algorithm == 'ARGON2':
            # ARGON2 - 现代安全哈希算法
            try:
                import argon2
                hasher = argon2.PasswordHasher()
                return hasher.hash(password)
            except ImportError:
                logger.warning("argon2-cffi 未安装，降级使用 SSHA")
                return self._ssha_hash(password)
        elif algorithm == 'BCRYPT':
            # BCRYPT - 现代安全哈希算法
            try:
                import bcrypt
                return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            except ImportError:
                logger.warning("bcrypt 未安装，降级使用 SSHA")
                return self._ssha_hash(password)
        else:
            # 默认使用SSHA
            logger.warning(f"未知的hash算法 {self.password_hash}, 使用SSHA")
            return self._ssha_hash(password)
    
    def _ssha_hash(self, password: str) -> str:
        """生成SSHA hash"""
        # 生成随机salt
        salt = os.urandom(4)
        
        # SHA-1 hash
        hash_obj = hashlib.sha1(password.encode('utf-8'))
        hash_obj.update(salt)
        digest = hash_obj.digest()
        
        # Base64编码 (digest + salt)
        encoded = base64.b64encode(digest + salt).decode('utf-8')
        
        return f'{{SSHA}}{encoded}'
    
    def _sha_hash(self, password: str) -> str:
        """生成SHA hash"""
        hash_obj = hashlib.sha1(password.encode('utf-8'))
        digest = hash_obj.digest()
        encoded = base64.b64encode(digest).decode('utf-8')
        return f'{{SHA}}{encoded}'
    
    def _md5_hash(self, password: str) -> str:
        """生成MD5 hash"""
        hash_obj = hashlib.md5(password.encode('utf-8'))
        digest = hash_obj.digest()
        encoded = base64.b64encode(digest).decode('utf-8')
        return f'{{MD5}}{encoded}'
    
    # ========== 账号管理 ==========
    
    def unlock_account(self, username: str) -> Tuple[bool, str]:
        """解锁账号（支持自动检测锁定机制）
        
        使用 detect_lock_mechanism 自动检测账号使用的锁定机制，
        支持多种 OpenLDAP 锁定实现：
        - ppolicy overlay (pwdAccountLockedTime)
        - 389 Directory Server (nsAccountLock)
        - 其他自定义锁定属性
        
        兼容未部署锁定机制的情况：
        - 如果未检测到支持的锁定机制，返回提示消息而非错误
        - 支持使用外部认证（如 SASL）的场景
        """
        try:
            if not self.is_connected():
                self.connect()
            
            success, user_dn = self.get_user_dn(username)
            if not success:
                raise LDAPException(LDAPErrorCode.ACCOUNT_NOT_FOUND, "账号不存在或已停用", 'openldap')
            
            # 自动检测锁定机制
            lock_config = self.detect_lock_mechanism(username)
            
            if lock_config is None:
                # 未检测到支持的锁定机制
                logger.info(f"账号 {username} 未检测到锁定机制或未锁定")
                return True, "账号未锁定或当前环境不支持锁定检测"
            
            attr = lock_config['attribute']
            check_type = lock_config.get('check', 'exists')
            
            # 检查是否真的被锁定
            self.conn.search(user_dn, '(objectClass=*)', attributes=[attr])
            
            if not self.conn.entries:
                raise LDAPException(LDAPErrorCode.ACCOUNT_NOT_FOUND, "账号不存在或已停用", 'openldap')
            
            entry = self.conn.entries[0]
            
            # 检查属性是否存在
            if attr not in entry.entry_attributes:
                return True, "账号当前未锁定"
            
            value = getattr(entry, attr, None)
            
            # 根据检查类型判断是否锁定
            is_locked = False
            if check_type == 'exists':
                is_locked = value is not None and value.value is not None
            elif check_type == 'value':
                locked_values = lock_config.get('locked_values', [])
                if value is not None and value.value is not None:
                    is_locked = str(value.value).lower() in [v.lower() for v in locked_values]
            
            if not is_locked:
                return True, "账号当前未锁定"
            
            # 执行解锁
            unlock_action = lock_config.get('unlock_action', 'delete')
            
            if unlock_action == 'delete':
                result = self.conn.modify(user_dn, {attr: [(MODIFY_DELETE, [])]})
            elif unlock_action == 'set_value':
                unlock_value = lock_config.get('unlock_value', 'false')
                result = self.conn.modify(user_dn, {attr: [(MODIFY_REPLACE, [unlock_value])]})
            else:
                result = self.conn.modify(user_dn, {attr: [(MODIFY_DELETE, [])]})
            
            if result:
                logger.info(f"账号 {username} 解锁成功 (机制: {lock_config.get('mechanism', 'unknown')})")
                return True, "账号解锁成功"
            else:
                raise LDAPException(LDAPErrorCode.MODIFY_FAILED, "解锁操作失败", 'openldap')
            
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"解锁账号异常: {str(e)}")
            raise LDAPException(LDAPErrorCode.MODIFY_FAILED, f"解锁失败: {str(e)}", 'openldap')
    
    def is_account_locked(self, username: str) -> Tuple[bool, bool]:
        """检查账号是否锁定
        
        通过 ldap.openldap.account_status.locked 配置控制检查方式
        """
        try:
            # 如果locked_codes为空,不检查锁定状态
            if not self.locked_codes:
                logger.debug(f"账号锁定检查已禁用（locked为空列表）,认为用户 {username} 未锁定")
                return True, False
            
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 搜索锁定属性
            self.conn.search(
                self.base_dn,
                self.search_filter.format(username),
                attributes=[self.locked_attribute]
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'openldap'
                )
            
            entry = self.conn.entries[0]
            
            # 检查锁定：如果locked_codes包含"exists"，则属性存在即表示锁定
            if 'exists' in [str(code).lower() for code in self.locked_codes]:
                is_locked = self.locked_attribute in entry and entry[self.locked_attribute].value is not None
            else:
                # 否则检查属性值是否在locked_codes列表中
                if self.locked_attribute in entry:
                    attr_value = str(entry[self.locked_attribute].value).lower()
                    is_locked = attr_value in [str(code).lower() for code in self.locked_codes]
                else:
                    is_locked = False
            
            logger.debug(f"用户 {username} 锁定状态: {is_locked} (检查方式: {self.locked_codes})")
            return True, is_locked
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"查询账号锁定状态失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"查询账号状态失败: {str(e)}",
                'openldap',
                e
            )
    
    def is_account_disabled(self, username: str) -> Tuple[bool, bool]:
        """检查账号是否被禁用（支持自动检测禁用机制）
        
        使用 detect_disable_mechanism 自动检测账号使用的禁用机制，
        支持多种 OpenLDAP 禁用实现：
        - 389 Directory Server (nsAccountLock)
        - FreeIPA (nsAccountLock)
        - shadowExpire 过期检查
        - 其他自定义禁用属性
        
        OpenLDAP 没有统一的账号禁用标志，不同实现方式不同。
        
        返回: (success, is_disabled)
        - success: 检查是否成功
        - is_disabled: 账号是否被禁用
        """
        try:
            if not self.is_connected():
                self.connect()
            
            success, user_dn = self.get_user_dn(username)
            if not success:
                # 账号不存在时抛出异常，与 AD 适配器行为保持一致
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'openldap'
                )
            
            # 自动检测禁用机制
            disable_config = self.detect_disable_mechanism(username)
            
            if disable_config is None:
                # 未检测到支持的禁用机制
                logger.debug(f"账号 {username} 未检测到禁用机制")
                return True, False
            
            attr = disable_config['attribute']
            check_type = disable_config.get('check', 'value')
            
            # 检查属性
            self.conn.search(user_dn, '(objectClass=*)', attributes=[attr])
            
            if not self.conn.entries:
                return True, False
            
            entry = self.conn.entries[0]
            
            # 检查属性是否存在
            if attr not in entry.entry_attributes:
                return True, False
            
            value = getattr(entry, attr, None)
            
            if value is None or value.value is None:
                return True, False
            
            # 根据检查类型判断是否禁用
            is_disabled = False
            
            if check_type == 'value':
                disabled_values = disable_config.get('disabled_values', [])
                is_disabled = str(value.value).lower() in [v.lower() for v in disabled_values]
            elif check_type == 'expire_date':
                # shadowExpire 检查：值是从 1970-01-01 开始的天数
                try:
                    expire_days = int(value.value)
                    import time
                    current_days = int(time.time() / 86400)
                    is_disabled = expire_days > 0 and expire_days < current_days
                except (ValueError, TypeError):
                    pass
            
            if is_disabled:
                logger.info(f"账号 {username} 已禁用 (机制: {disable_config.get('mechanism', 'unknown')})")
            
            return True, is_disabled
            
        except Exception as e:
            logger.error(f"检查账号禁用状态异常: {str(e)}")
            if 'invalid attribute' in str(e).lower():
                logger.warning(f"属性无效，跳过禁用状态检查")
                return True, False
            return False, False
    
    def _check_lock_status(self, username: str, lock_config: Dict) -> Tuple[bool, bool]:
        """检查账号锁定状态的内部方法
        
        Args:
            username: 用户名
            lock_config: 锁定机制配置
            
        Returns:
            (success, is_locked): 操作是否成功，账号是否锁定
        """
        try:
            if not self.is_connected():
                self.connect()
            
            success, user_dn = self.get_user_dn(username)
            if not success:
                return True, False
            
            attr = lock_config['attribute']
            check_type = lock_config.get('check', 'exists')
            
            self.conn.search(user_dn, '(objectClass=*)', attributes=[attr])
            
            if not self.conn.entries:
                return True, False
            
            entry = self.conn.entries[0]
            
            if attr not in entry.entry_attributes:
                return True, False
            
            value = getattr(entry, attr, None)
            
            if value is None or value.value is None:
                return True, False
            
            is_locked = False
            if check_type == 'exists':
                is_locked = True
            elif check_type == 'value':
                locked_values = lock_config.get('locked_values', [])
                is_locked = str(value.value).lower() in [v.lower() for v in locked_values]
            
            return True, is_locked
            
        except Exception as e:
            logger.error(f"检查锁定状态异常: {str(e)}")
            return False, False
    
    def _check_disable_status(self, username: str, disable_config: Dict) -> Tuple[bool, bool]:
        """检查账号禁用状态的内部方法
        
        Args:
            username: 用户名
            disable_config: 禁用机制配置
            
        Returns:
            (success, is_disabled): 操作是否成功，账号是否禁用
        """
        try:
            if not self.is_connected():
                self.connect()
            
            success, user_dn = self.get_user_dn(username)
            if not success:
                return True, False
            
            attr = disable_config['attribute']
            check_type = disable_config.get('check', 'value')
            
            self.conn.search(user_dn, '(objectClass=*)', attributes=[attr])
            
            if not self.conn.entries:
                return True, False
            
            entry = self.conn.entries[0]
            
            if attr not in entry.entry_attributes:
                return True, False
            
            value = getattr(entry, attr, None)
            
            if value is None or value.value is None:
                return True, False
            
            is_disabled = False
            if check_type == 'value':
                disabled_values = disable_config.get('disabled_values', [])
                is_disabled = str(value.value).lower() in [v.lower() for v in disabled_values]
            elif check_type == 'expire_date':
                try:
                    expire_days = int(value.value)
                    import time
                    current_days = int(time.time() / 86400)
                    is_disabled = expire_days > 0 and expire_days < current_days
                except (ValueError, TypeError):
                    pass
            
            return True, is_disabled
            
        except Exception as e:
            logger.error(f"检查禁用状态异常: {str(e)}")
            return False, False
    
    def get_account_status(self, username: str) -> Tuple[bool, Dict]:
        """获取账号综合状态
        
        使用自动检测机制检查账号的锁定和禁用状态，
        返回详细的状态信息包括检测到的机制类型。
        
        Args:
            username: 用户名
            
        Returns:
            (success, status):
            - success: 操作是否成功
            - status: 状态字典，包含:
                - exists: 账号是否存在
                - locked: 账号是否锁定
                - disabled: 账号是否禁用
                - lock_mechanism: 检测到的锁定机制
                - disable_mechanism: 检测到的禁用机制
                - warnings: 警告信息列表
        """
        status = {
            'exists': False,
            'locked': False,
            'disabled': False,
            'lock_mechanism': None,
            'disable_mechanism': None,
            'warnings': []
        }
        
        try:
            if not self.is_connected():
                self.connect()
            
            # 检查账号是否存在
            success, user_dn = self.get_user_dn(username)
            if not success:
                status['warnings'].append('ACCOUNT_NOT_FOUND')
                return True, status
            
            status['exists'] = True
            
            # 检查锁定状态
            lock_config = self.detect_lock_mechanism(username)
            if lock_config:
                _, is_locked = self._check_lock_status(username, lock_config)
                status['locked'] = is_locked
                status['lock_mechanism'] = lock_config.get('mechanism')
            else:
                status['warnings'].append('LOCK_DETECTION_NOT_SUPPORTED')
            
            # 检查禁用状态
            disable_config = self.detect_disable_mechanism(username)
            if disable_config:
                _, is_disabled = self._check_disable_status(username, disable_config)
                status['disabled'] = is_disabled
                status['disable_mechanism'] = disable_config.get('mechanism')
            else:
                status['warnings'].append('DISABLE_DETECTION_NOT_SUPPORTED')
            
            return True, status
            
        except Exception as e:
            logger.error(f"获取账号状态异常: {str(e)}")
            return False, status
    
    # ========== 用户信息查询 ==========
    
    def search_user(self, username: str, attributes: List[str] = None) -> Tuple[bool, Dict]:
        """搜索用户信息"""
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 使用默认属性或指定属性
            search_attrs = attributes or self.search_attributes
            
            # 搜索用户
            self.conn.search(
                self.base_dn,
                self.search_filter.format(username),
                attributes=search_attrs
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'openldap'
                )
            
            # 转换为字典
            entry = self.conn.entries[0]
            user_info = {}
            for attr in search_attrs:
                if attr in entry:
                    user_info[attr] = str(entry[attr])
            
            return True, user_info
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"搜索用户失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"搜索用户失败: {str(e)}",
                'openldap',
                e
            )
    
    def get_user_dn(self, username: str) -> Tuple[bool, str]:
        """获取用户DN"""
        try:
            # 防护：格式验证
            is_valid, error_msg = LDAPEscape.validate_username(username)
            if not is_valid:
                raise LDAPException(
                    LDAPErrorCode.INVALID_PARAMETER,
                    f"用户名格式不正确: {error_msg}",
                    'openldap'
                )

            # 如果配置了DN模板,直接使用
            if self.user_dn_template:
                # 转义username（防止DN注入）
                escaped_username = LDAPEscape.escape_dn_value(username)
                user_dn = self.user_dn_template.replace('{username}', escaped_username)
                logger.debug(f"使用DN模板: {user_dn}")
                return True, user_dn
            
            # 确保连接
            if not self.is_connected():
                self.connect()

            # 转义username（防止搜索过滤器注入）
            escaped_username = LDAPEscape.escape_filter_value(username)

            # 通过搜索获取
            # 注意: dn 是伪属性，不应在 attributes 中请求，DN 通过 entry.entry_dn 自动获取
            self.conn.search(
                self.base_dn,
                self.search_filter.format(escaped_username),
                attributes=[]
            )
            
            if not self.conn.entries:
                # 账号不存在，可能是：
                # 1. 账号确实不存在
                # 2. 账号被移动到禁用 OU（不在搜索范围内）
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    "账号不存在或已停用",  # 多义提示，避免信息泄露
                    'openldap'
                )
            
            user_dn = str(self.conn.entries[0].entry_dn)
            return True, user_dn
        
        except LDAPException:
            raise
        except Exception as e:
            # 属性不存在时的优雅处理
            error_str = str(e).lower()
            if 'invalid attribute' in error_str or 'no such attribute' in error_str:
                logger.warning(f"搜索属性无效: {str(e)}")
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    "账号不存在或已停用",
                    'openldap'
                )
            logger.error(f"获取用户DN失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"获取用户DN失败: {str(e)}",
                'openldap',
                e
            )
    
    # ========== 组成员管理 ==========
    
    def get_user_groups(self, username: str) -> Tuple[bool, List[str]]:
        """获取用户所属组"""
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            if self.memberof_overlay:
                # 方式1: 使用memberOf属性 (需要memberof overlay)
                self.conn.search(
                    self.base_dn,
                    self.search_filter.format(username),
                    attributes=[self.member_of_attr]
                )
                
                if not self.conn.entries:
                    raise LDAPException(
                        LDAPErrorCode.ACCOUNT_NOT_FOUND,
                        f"用户 {username} 不存在",
                        'openldap'
                    )
                
                entry = self.conn.entries[0]
                member_of = entry[self.member_of_attr] if self.member_of_attr in entry else []
                group_dns = [str(dn) for dn in member_of] if member_of else []
            else:
                # 方式2: 反向查询组 (无需overlay)
                # 首先获取用户DN
                success, user_dn = self.get_user_dn(username)
                if not success:
                    raise LDAPException(
                        LDAPErrorCode.ACCOUNT_NOT_FOUND,
                        f"用户 {username} 不存在",
                        'openldap'
                    )
                
                # 查询包含该用户的组
                groups_base = get_config().get('ldap.groups_base_dn', f'ou=groups,{self.base_dn}')
                self.conn.search(
                    groups_base,
                    f'(member={user_dn})',
                    attributes=['cn']
                )
                
                group_dns = [str(entry.entry_dn) for entry in self.conn.entries]
            
            logger.debug(f"用户 {username} 所属组: {group_dns}")
            return True, group_dns
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"查询用户组失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"查询用户组失败: {str(e)}",
                'openldap',
                e
            )
    
    def extract_group_name(self, group_dn: str) -> str:
        """从组DN中提取组名"""
        # OpenLDAP格式: cn=admins,ou=groups,dc=company,dc=com
        # 提取第一个cn的值
        match = re.match(r'^cn=([^,]+)', group_dn, re.IGNORECASE)
        if match:
            return match.group(1)
        return group_dn
    
    # ========== 密码策略管理 ==========
    
    def get_password_policy(self, username: str = None) -> Dict:
        """
        读取 OpenLDAP 密码策略配置
        
        优先级顺序：
        1. 用户特定策略（pwdPolicySubentry 属性指向）
        2. 默认策略（配置的 policy_dn）
        
        Args:
            username: 用户名（可选，用于获取用户特定策略）
            
        Returns:
            密码策略字典，包含：
            - pwdMinLength: 最小密码长度
            - pwdMaxAge: 密码最大使用期限（秒）
            - pwdMinAge: 密码最小修改间隔（秒）
            - pwdInHistory: 密码历史长度
            - pwdCheckQuality: 密码质量检查级别（0/1/2）
            - pwdMaxFailure: 最大失败次数
            - pwdLockout: 是否启用锁定
            - pwdLockoutDuration: 锁定持续时间（秒）
            - pwdFailureCountInterval: 失败计数重置间隔（秒）
            - pwdExpireWarning: 密码过期警告时间（秒）
            - pwdGraceAuthNLimit: 宽限认证次数
            - pwdMustChange: 是否必须在首次登录时修改密码
            - pwdAllowUserChange: 是否允许用户修改密码
            - pwdSafeModify: 是否要求修改密码时提供旧密码
        """
        # 如果未启用 ppolicy，返回空字典
        if not self.ppolicy_enabled:
            logger.debug("ppolicy 未启用，返回空策略")
            return {}
        
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            policy_dn = None
            
            # 1. 尝试获取用户特定策略
            if username:
                config = get_config()
                detect_user_policy = config.get('ldap.openldap.ppolicy.detect_user_policy', True)
                
                if detect_user_policy:
                    success, user_dn = self.get_user_dn(username)
                    if success:
                        # 查询用户的 pwdPolicySubentry 属性
                        self.conn.search(
                            user_dn,
                            '(objectClass=*)',
                            attributes=['pwdPolicySubentry']
                        )
                        
                        if self.conn.entries:
                            entry = self.conn.entries[0]
                            if 'pwdPolicySubentry' in entry.entry_attributes:
                                policy_attr = getattr(entry, 'pwdPolicySubentry', None)
                                if policy_attr and policy_attr.value:
                                    policy_dn = str(policy_attr.value)
                                    logger.debug(f"用户 {username} 使用特定策略: {policy_dn}")
            
            # 2. 使用默认策略
            if not policy_dn:
                policy_dn = self.ppolicy_dn
                if not policy_dn:
                    logger.warning("未配置默认策略 DN，返回空策略")
                    return {}
                logger.debug(f"使用默认策略: {policy_dn}")
            
            # 3. 读取策略属性
            # PPolicy 属性列表
            ppolicy_attrs = [
                'pwdMinLength',
                'pwdMaxAge',
                'pwdMinAge',
                'pwdInHistory',
                'pwdCheckQuality',
                'pwdMaxFailure',
                'pwdLockout',
                'pwdLockoutDuration',
                'pwdFailureCountInterval',
                'pwdExpireWarning',
                'pwdGraceAuthNLimit',
                'pwdMustChange',
                'pwdAllowUserChange',
                'pwdSafeModify',
                'cn',
                'objectClass'
            ]
            
            self.conn.search(
                policy_dn,
                '(objectClass=pwdPolicy)',
                attributes=ppolicy_attrs
            )
            
            if not self.conn.entries:
                logger.warning(f"策略 DN 不存在或不是有效的密码策略: {policy_dn}")
                return {}
            
            entry = self.conn.entries[0]
            policy = {}
            
            # 提取策略属性值
            attr_mapping = {
                'pwdMinLength': ('min_length', int),
                'pwdMaxAge': ('max_age', int),
                'pwdMinAge': ('min_age', int),
                'pwdInHistory': ('history_length', int),
                'pwdCheckQuality': ('check_quality', int),
                'pwdMaxFailure': ('max_failure', int),
                'pwdLockout': ('lockout_enabled', lambda x: str(x).upper() in ['TRUE', '1', 'YES']),
                'pwdLockoutDuration': ('lockout_duration', int),
                'pwdFailureCountInterval': ('failure_count_interval', int),
                'pwdExpireWarning': ('expire_warning', int),
                'pwdGraceAuthNLimit': ('grace_auth_limit', int),
                'pwdMustChange': ('must_change', lambda x: str(x).upper() in ['TRUE', '1', 'YES']),
                'pwdAllowUserChange': ('allow_user_change', lambda x: str(x).upper() in ['TRUE', '1', 'YES']),
                'pwdSafeModify': ('safe_modify', lambda x: str(x).upper() in ['TRUE', '1', 'YES'])
            }
            
            for attr_name, (key, converter) in attr_mapping.items():
                if attr_name in entry.entry_attributes:
                    value = getattr(entry, attr_name, None)
                    if value is not None and value.value is not None:
                        try:
                            policy[key] = converter(value.value)
                        except (ValueError, TypeError) as e:
                            logger.warning(f"转换策略属性 {attr_name} 值失败: {e}")
                            policy[key] = value.value
            
            logger.debug(f"读取密码策略成功: {policy}")
            return policy
            
        except LDAPException as e:
            logger.error(f"读取密码策略失败: {e}")
            return {}
        except Exception as e:
            logger.error(f"读取密码策略异常: {e}")
            return {}
    
    def get_user_password_attrs(self, username: str) -> Dict:
        """
        读取用户密码相关属性
        
        Args:
            username: 用户名
            
        Returns:
            用户密码属性字典，包含：
            - pwdChangedTime: 上次密码修改时间（datetime 对象或字符串）
            - pwdFailureTime: 认证失败时间列表
            - pwdAccountLockedTime: 账户锁定时间
            - pwdReset: 是否需要重置密码
            - pwdPolicySubentry: 用户特定策略 DN
            - pwdGraceUseTime: 宽限认证使用时间列表
            - pwdExpireWarningSent: 是否已发送过期警告
        """
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 获取用户 DN
            success, user_dn = self.get_user_dn(username)
            if not success:
                logger.warning(f"用户 {username} 不存在")
                return {}
            
            # PPolicy 用户操作属性列表
            ppolicy_user_attrs = [
                'pwdChangedTime',
                'pwdFailureTime',
                'pwdAccountLockedTime',
                'pwdReset',
                'pwdPolicySubentry',
                'pwdGraceUseTime',
                'pwdExpireWarningSent'
            ]
            
            self.conn.search(
                user_dn,
                '(objectClass=*)',
                attributes=ppolicy_user_attrs
            )
            
            if not self.conn.entries:
                logger.warning(f"无法读取用户 {username} 的属性")
                return {}
            
            entry = self.conn.entries[0]
            attrs = {}
            
            # 提取属性值
            for attr_name in ppolicy_user_attrs:
                if attr_name in entry.entry_attributes:
                    value = getattr(entry, attr_name, None)
                    if value is not None:
                        # 处理多值属性
                        if attr_name in ['pwdFailureTime', 'pwdGraceUseTime']:
                            if hasattr(value, 'values'):
                                attrs[attr_name] = [str(v) for v in value.values]
                            elif isinstance(value.value, list):
                                attrs[attr_name] = [str(v) for v in value.value]
                            else:
                                attrs[attr_name] = [str(value.value)] if value.value else []
                        else:
                            attrs[attr_name] = str(value.value) if value.value else None
            
            logger.debug(f"用户 {username} 密码属性: {attrs}")
            return attrs
            
        except LDAPException as e:
            logger.error(f"读取用户密码属性失败: {e}")
            return {}
        except Exception as e:
            logger.error(f"读取用户密码属性异常: {e}")
            return {}
    
    def get_password_requirements(self, username: str = None) -> Dict:
        """
        获取密码要求（用于前端显示）
        
        将密码策略转换为前端友好的格式，包含描述文本和验证规则。
        
        Args:
            username: 用户名（可选，用于获取用户特定策略）
            
        Returns:
            格式化的密码要求字典，包含：
            - min_length: 最小长度
            - max_length: 最大长度（通常为空或不限制）
            - history_count: 密码历史数量
            - requirements: 要求列表，每项包含：
                - key: 要求标识
                - label: 显示文本
                - value: 配置值
            - rules: 前端验证规则（可用于表单验证）
        """
        # 获取密码策略
        policy = self.get_password_policy(username)
        
        # 构建密码要求
        requirements = []
        
        # 最小长度
        if 'min_length' in policy:
            requirements.append({
                'key': 'min_length',
                'label': f"密码长度至少 {policy['min_length']} 个字符",
                'value': policy['min_length']
            })
        
        # 密码历史
        if 'history_length' in policy and policy['history_length'] > 0:
            requirements.append({
                'key': 'history',
                'label': f"不能使用最近 {policy['history_length']} 次使用过的密码",
                'value': policy['history_length']
            })
        
        # 密码质量检查
        if 'check_quality' in policy:
            quality_map = {
                0: "不检查密码质量",
                1: "检查密码质量（建议）",
                2: "严格检查密码质量"
            }
            quality = policy['check_quality']
            if quality > 0:
                requirements.append({
                    'key': 'quality',
                    'label': "密码需满足复杂度要求",
                    'value': quality,
                    'description': quality_map.get(quality, "")
                })
        
        # 密码过期
        if 'max_age' in policy and policy['max_age'] > 0:
            days = policy['max_age'] // 86400
            if days > 0:
                requirements.append({
                    'key': 'max_age',
                    'label': f"密码有效期为 {days} 天",
                    'value': policy['max_age']
                })
        
        # 账户锁定策略
        if policy.get('lockout_enabled') and 'max_failure' in policy:
            requirements.append({
                'key': 'lockout',
                'label': f"连续 {policy['max_failure']} 次密码错误将锁定账户",
                'value': policy['max_failure']
            })
        
        # 构建验证规则
        rules = {}
        
        if 'min_length' in policy:
            rules['minLength'] = policy['min_length']
        
        if 'history_length' in policy and policy['history_length'] > 0:
            rules['historyCount'] = policy['history_length']
        
        # 构建返回结果
        result = {
            'min_length': policy.get('min_length', 0),
            'max_length': None,  # OpenLDAP 通常不限制最大长度
            'history_count': policy.get('history_length', 0),
            'requirements': requirements,
            'rules': rules,
            'policy_source': 'ppolicy' if policy else None
        }
        
        # 添加原始策略数据（供高级用途）
        result['raw_policy'] = policy
        
        logger.debug(f"密码要求: {result}")
        return result
