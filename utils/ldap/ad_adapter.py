# -*- coding: utf-8 -*-
"""
Active Directory适配器实现
将AD特有的操作封装为统一的LDAP接口
"""

from ldap3 import Server, Connection, ALL, NTLM, SIMPLE, MODIFY_REPLACE, MODIFY_DELETE, MODIFY_ADD
from ldap3.core.results import RESULT_SUCCESS
from ldap3.core.exceptions import (
    LDAPInvalidCredentialsResult, 
    LDAPOperationResult, 
    LDAPException as Ldap3Exception,
    LDAPSocketOpenError
)
from ldap3.utils.dn import safe_dn
import re
from typing import Tuple, List, Dict, Optional
from .ldap_escape import LDAPEscape
from .adapter import LDAPAdapter
from .errors import LDAPException, LDAPErrorCode
from .error_messages import (
    get_ad_error_message,
    parse_ad_error_from_string,
    get_ldap_error_message,
    category_to_error_code
)
from utils.config import get_config
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class ADAdapter(LDAPAdapter):
    """Active Directory适配器"""
    
    def __init__(self):
        """初始化AD适配器"""
        super().__init__()
        
        config = get_config()
        self.ldap_type = 'ad'
        
        # 通用LDAP配置
        self.ldap_host = config.get('ldap.host')
        self.use_ssl = config.get('ldap.use_ssl', True)
        self.port = config.get('ldap.port', 636)
        self.base_dn = config.get('ldap.base_dn', '')
        self.connection_timeout = config.get('ldap.connection_timeout', 10)
        self.response_timeout = config.get('ldap.response_timeout', 30)
        
        # AD专用配置
        _domain = config.get('ldap.domain')
        # 如果domain是域名格式(company.com),只提取DOMAIN部分
        self.domain = _domain.split('.')[0] if _domain else None
        
        # 服务账号凭据
        self.login_user = config.get('ldap.login_user')
        self.login_password = config.get('ldap.login_password')
        
        # AD认证方式 (从ad配置读取,默认NTLM)
        auth_type = config.get('ldap.ad.authentication', 'ntlm').lower()
        self.authentication = NTLM if auth_type == 'ntlm' else SIMPLE
        
        # AD属性映射 (支持配置化)
        attr_config = config.get('ldap.ad.attributes', {})
        self.password_attr = attr_config.get('password', 'unicodePwd')
        self.username_attr = attr_config.get('username', 'sAMAccountName')
        self.lockout_attr = attr_config.get('lockout_time', 'lockoutTime')
        self.account_control_attr = attr_config.get('account_control', 'userAccountControl')
        self.member_of_attr = attr_config.get('member_of', 'memberOf')
        self.object_class = attr_config.get('object_class', 'user')
        
        # 搜索过滤器 (支持配置化)
        _search_filter = config.get('ldap.search_filter', '')
        self.search_filter = _search_filter if _search_filter else \
            f'(&(objectclass={self.object_class})({self.username_attr}={{}}))'
        self.search_attributes = config.get(
            'ldap.search_attributes',
            [self.username_attr, 'mail', self.account_control_attr]
        )
        
        # 用户DN模板 (可选,如果配置则不需要搜索)
        self.user_dn_template = config.get('ldap.user_dn_template', '')
        
        # 账号状态配置（从ad配置段读取）
        account_status = config.get('ldap.ad.account_status', {})
        self.enabled_codes = account_status.get('enabled', [512])
        self.disabled_codes = account_status.get('disabled', [514, 66050, 66082])
        self.locked_codes = account_status.get('locked', [8388608])
        self.password_expired_codes = account_status.get('password_expired', [8388608])
        
        # 加载TLS配置
        self.tls_config = self._load_tls_config(config)
        
        logger.debug(f"AD适配器初始化完成: host={self.ldap_host}, domain={self.domain}, auth={auth_type}")
    
    def _load_tls_config(self, config) -> Dict:
        """加载TLS配置
        
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
        
        # 获取TLS配置段
        validate_mode = config.get('ldap.ad.tls.validate', 'required').lower()
        
        # 映射验证级别到ssl常量
        if validate_mode == 'none':
            tls_config['validate'] = ssl.CERT_NONE
            logger.warning("AD TLS证书验证已禁用（validate=none），不推荐用于生产环境")
        elif validate_mode == 'optional':
            tls_config['validate'] = ssl.CERT_OPTIONAL
            logger.warning("AD TLS证书验证设置为可选（validate=optional）")
        else:  # 'required'
            tls_config['validate'] = ssl.CERT_REQUIRED
            logger.debug("✅ AD TLS证书验证已启用（validate=required）")
        
        # CA证书文件
        ca_file = config.get('ldap.ad.tls.ca_certs_file', '').strip()
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
                    'ad'
                )
        
        # CA证书目录
        ca_path = config.get('ldap.ad.tls.ca_certs_path', '').strip()
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
        client_cert = config.get('ldap.ad.tls.local_certificate_file', '').strip()
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
        private_key = config.get('ldap.ad.tls.local_private_key_file', '').strip()
        if private_key:
            if not private_key.startswith('/') and not (len(private_key) > 1 and private_key[1] == ':'):
                project_root = Path(__file__).parent.parent.parent
                private_key = str(project_root / private_key)
            
            if os.path.exists(private_key):
                tls_config['local_private_key_file'] = private_key
                
                # 私钥密码
                key_password = config.get('ldap.ad.tls.local_private_key_password', '').strip()
                if key_password:
                    tls_config['local_private_key_password'] = key_password
                
                logger.debug(f"使用客户端私钥: {private_key}")
            else:
                logger.error(f"客户端私钥文件不存在: {private_key}")
        
        # TLS版本
        tls_version = config.get('ldap.ad.tls.version', '').strip().upper()
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
        validate_hostname = config.get('ldap.ad.tls.validate_hostname', True)
        if not validate_hostname:
            tls_config['valid_names'] = []  # 禁用主机名验证
            logger.warning("主机名验证已禁用")
        
        # 自定义加密套件
        ciphers = config.get('ldap.ad.tls.ciphers', '').strip()
        if ciphers:
            tls_config['ciphers'] = ciphers
            logger.debug(f"使用自定义加密套件: {ciphers}")
        
        return tls_config
    
    # ========== 连接管理 ==========
    
    def connect(self) -> Tuple[bool, str]:
        """建立AD连接"""
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
                            'ad',
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
                logger.debug(f"AD服务器对象创建成功: {self.ldap_host}:{self.port}, TLS={'启用' if tls_obj else '未配置'}")
            
            # 创建连接对象
            if self.conn is None or not self.conn.bound:
                # 根据认证方式构造用户名
                if self.authentication == NTLM:
                    bind_user = f'{self.domain}\\{self.login_user}'
                else:
                    bind_user = self.login_user
                
                self.conn = Connection(
                    self.server,
                    user=bind_user,
                    password=self.login_password,
                    authentication=self.authentication,
                    auto_bind=True,
                    raise_exceptions=True,
                    receive_timeout=self.response_timeout
                )
                logger.info(f"AD连接建立成功: {bind_user}")
            
            return True, "AD连接成功"
        
        except LDAPInvalidCredentialsResult as e:
            logger.error(f"AD认证失败: {e}")
            raise LDAPException(
                LDAPErrorCode.BIND_FAILED,
                "AD服务账号认证失败",
                'ad',
                e
            )
        except LDAPSocketOpenError as e:
            logger.error(f"AD连接失败: {e}")
            raise LDAPException(
                LDAPErrorCode.CONNECTION_FAILED,
                f"无法连接到AD服务器 {self.ldap_host}:{self.port}",
                'ad',
                e
            )
        except Ldap3Exception as e:
            logger.error(f"AD连接异常: {e}")
            raise LDAPException(
                LDAPErrorCode.CONNECTION_FAILED,
                f"AD连接失败: {str(e)}",
                'ad',
                e
            )
    
    def disconnect(self):
        """断开AD连接"""
        if self.conn and self.conn.bound:
            try:
                self.conn.unbind()
                logger.debug("AD连接已断开")
            except Exception as e:
                logger.warning(f"AD断开连接时发生异常: {e}")
        self.conn = None
    
    # ========== 认证相关 ==========
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, str]:
        """验证用户凭据"""
        try:
            # 创建临时连接进行认证
            if self.server is None:
                self.connect()  # 确保server已创建
            
            # 根据认证方式构造用户名
            if self.authentication == NTLM:
                bind_user = f'{self.domain}\\{username}'
            else:
                # SIMPLE认证需要完整DN
                success, user_dn = self.get_user_dn(username)
                if not success:
                    raise LDAPException(
                        LDAPErrorCode.ACCOUNT_NOT_FOUND,
                        f"用户 {username} 不存在",
                        'ad'
                    )
                bind_user = user_dn
            
            # 尝试认证
            auth_conn = Connection(
                self.server,
                user=bind_user,
                password=password,
                authentication=self.authentication,
                auto_bind=True,
                raise_exceptions=True
            )
            auth_conn.unbind()
            
            logger.info(f"用户 {username} 认证成功")
            return True, "认证成功"
        
        except LDAPInvalidCredentialsResult as e:
            # 解析AD错误码
            error_code, error_msg = self._parse_ad_auth_error(e.message, username)
            logger.warning(f"用户 {username} 认证失败: {error_msg} (AD错误: {e.message})")
            raise LDAPException(error_code, error_msg, 'ad', e)
        
        except LDAPException:
            # 重新抛出我们的异常
            raise
        
        except Exception as e:
            logger.error(f"用户 {username} 认证异常: {e}")
            raise LDAPException(
                LDAPErrorCode.UNKNOWN_ERROR,
                f"认证失败: {str(e)}",
                'ad',
                e
            )
    
    def _parse_ad_auth_error(self, ad_message: str, username: str) -> Tuple[int, str]:
        """
        解析AD认证错误消息中的错误码
        
        使用统一的错误码映射表获取友好消息
        
        Args:
            ad_message: AD 错误消息字符串
            username: 用户名 (用于日志)
        
        Returns:
            (错误码, 友好消息) 元组
        """
        # 使用统一的错误码解析函数
        error_info = parse_ad_error_from_string(ad_message, lang='zh')
        
        if error_info:
            # 将错误类别转换为统一错误码
            error_code = category_to_error_code(error_info['category'])
            return error_code, error_info['message']
        
        # 未匹配到已知错误码，返回通用错误
        logger.warning(f"未识别的AD错误码: {ad_message}")
        return LDAPErrorCode.INVALID_CREDENTIALS, "认证失败,请确认账号和密码是否正确"
    
    # ========== 密码管理 ==========
    
    def reset_password(self, username: str, new_password: str, 
                      old_password: str = None) -> Tuple[bool, str]:
        """
        重置用户密码 (管理员操作)
        
        使用MODIFY_REPLACE操作,不需要旧密码
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
                    'ad'
                )
            
            # 转义DN (如果需要)
            if self.conn.check_names:
                user_dn = safe_dn(user_dn)
            
            # 编码密码 (UTF-16LE + 引号)
            encoded_password = f'"{new_password}"'.encode('utf-16-le')
            
            # 执行修改
            result = self.conn.modify(
                user_dn,
                {self.password_attr: [(MODIFY_REPLACE, [encoded_password])]}
            )
            
            # 检查结果
            if self.conn.result['result'] == RESULT_SUCCESS:
                logger.info(f"用户 {username} 密码重置成功 (管理员操作)")
                return True, "密码重置成功"
            else:
                error_msg = self.conn.result.get('description', '未知错误')
                logger.error(f"用户 {username} 密码重置失败: {error_msg}")
                raise LDAPException(
                    LDAPErrorCode.MODIFY_FAILED,
                    f"密码重置失败: {error_msg}",
                    'ad',
                    details=self.conn.result
                )
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"密码重置异常: {e}")
            raise LDAPException(
                LDAPErrorCode.MODIFY_FAILED,
                f"密码重置失败: {str(e)}",
                'ad',
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
            # 确保服务器对象已创建
            if self.server is None:
                self.connect()  # 这会创建server对象
            
            # ========== 步骤1：使用用户凭据认证（验证旧密码正确性）==========
            if self.authentication == NTLM:
                bind_user = f'{self.domain}\\{username}'
            else:
                # SIMPLE认证需要完整DN，需要先获取
                success, user_dn = self.get_user_dn(username)
                if not success:
                    raise LDAPException(
                        LDAPErrorCode.ACCOUNT_NOT_FOUND,
                        f"用户 {username} 不存在",
                        'ad'
                    )
                bind_user = user_dn
            
            # 使用用户凭据建立临时连接进行认证
            user_conn = Connection(
                self.server,
                user=bind_user,
                password=old_password,
                authentication=self.authentication,
                auto_bind=True,
                raise_exceptions=True
            )
            
            logger.info(f"用户 {username} 旧密码验证成功（用户认证通过）")
            
            # 关闭用户连接，后续使用管理员连接
            try:
                user_conn.unbind()
                user_conn = None
                logger.debug(f"用户 {username} 认证连接已关闭，切换到管理员连接")
            except Exception as e:
                logger.warning(f"关闭用户认证连接时发生异常: {e}")
                user_conn = None
            
            # ========== 步骤2：确保管理员连接可用 ==========
            if not self.is_connected():
                self.connect()
            
            # 获取用户DN
            success, user_dn = self.get_user_dn(username)
            if not success:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'ad'
                )
            
            # 转义DN
            if self.conn.check_names:
                user_dn = safe_dn(user_dn)
            
            # ========== 步骤3：使用管理员连接执行密码修改 ==========
            # 编码密码 (UTF-16LE + 引号)
            encoded_new = f'"{new_password}"'.encode('utf-16-le')
            
            # 诊断日志
            logger.debug(f"===== 管理员执行密码修改 =====")
            logger.debug(f"  用户DN: {user_dn}")
            logger.debug(f"  新密码长度: {len(new_password)} 字符")
            logger.debug(f"  编码格式: UTF-16LE + 双引号包裹")
            logger.debug(f"  密码属性: {self.password_attr}")
            logger.debug(f"  执行方式: 管理员连接 MODIFY_REPLACE")
            
            # 检查密码复杂度（本地验证）
            has_upper = bool(re.search(r'[A-Z]', new_password))
            has_lower = bool(re.search(r'[a-z]', new_password))
            has_digit = bool(re.search(r'\d', new_password))
            has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', new_password))
            logger.debug(f"  新密码复杂度检查:")
            logger.debug(f"    - 包含大写字母: {'是' if has_upper else '否'}")
            logger.debug(f"    - 包含小写字母: {'是' if has_lower else '否'}")
            logger.debug(f"    - 包含数字: {'是' if has_digit else '否'}")
            logger.debug(f"    - 包含特殊字符: {'是' if has_special else '否'}")
            logger.debug(f"  ========================")
            
            # 使用管理员连接执行密码修改 (MODIFY_REPLACE)
            result = self.conn.modify(
                user_dn,
                {self.password_attr: [(MODIFY_REPLACE, [encoded_new])]}
            )
            
            if self.conn.result['result'] == RESULT_SUCCESS:
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
                error_msg = self.conn.result.get('description', '未知错误')
                error_code = self.conn.result.get('result', '未知')
                
                # 详细错误诊断
                logger.error(f"===== 管理员密码修改错误详情 =====")
                logger.error(f"  用户: {username}")
                logger.error(f"  错误码: {error_code}")
                logger.error(f"  错误描述: {error_msg}")
                logger.error(f"  完整结果: {self.conn.result}")
                logger.error(f"  ============================")
                
                # 使用统一的错误码解析函数
                error_str = str(self.conn.result)
                error_info = parse_ad_error_from_string(error_str, lang='zh')
                
                if error_info:
                    # 找到匹配的错误码
                    logger.warning(f"用户 {username} 密码修改失败: {error_info['message']} (错误码: {error_info['code']})")
                    
                    # 如果是密码策略错误(0000052D)，尝试精确诊断
                    if error_info.get('code') == '0000052D':
                        try:
                            diagnostic_msg = self.diagnose_password_error(username, new_password)
                            logger.info(f"密码策略诊断结果: {diagnostic_msg}")
                            raise LDAPException(
                                category_to_error_code(error_info['category']),
                                diagnostic_msg,
                                'ad',
                                details=self.conn.result
                            )
                        except Exception as diag_e:
                            logger.warning(f"密码诊断失败，使用通用消息: {diag_e}")
                            # 诊断失败时使用通用消息
                            raise LDAPException(
                                category_to_error_code(error_info['category']),
                                error_info['message'],
                                'ad',
                                details=self.conn.result
                            )
                    
                    # 其他错误码直接使用通用消息
                    raise LDAPException(
                        category_to_error_code(error_info['category']),
                        error_info['message'],
                        'ad',
                        details=self.conn.result
                    )
                
                # 尝试解析标准 LDAP 错误码
                ldap_error_info = get_ldap_error_message(error_code, lang='zh')
                if ldap_error_info:
                    raise LDAPException(
                        category_to_error_code(ldap_error_info['category']),
                        ldap_error_info['message'],
                        'ad',
                        details=self.conn.result
                    )
                
                # 未匹配到已知错误码，返回原始错误
                raise LDAPException(
                    LDAPErrorCode.MODIFY_FAILED,
                    f"密码修改失败: {error_msg}",
                    'ad',
                    details=self.conn.result
                )
        
        except LDAPInvalidCredentialsResult as e:
            # 解析AD错误码（用户认证失败）
            error_code, error_msg = self._parse_ad_auth_error(e.message, username)
            logger.warning(f"用户 {username} 旧密码验证失败: {error_msg} (AD错误: {e.message})")
            raise LDAPException(error_code, error_msg, 'ad', e)
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"密码修改异常: {e}")
            logger.error(f"异常类型: {type(e).__name__}")
            logger.error(f"异常详情: {str(e)}")
            raise LDAPException(
                LDAPErrorCode.MODIFY_FAILED,
                f"密码修改失败: {str(e)}",
                'ad',
                e
            )
        finally:
            # 确保用户认证连接被关闭
            if user_conn and user_conn.bound:
                try:
                    user_conn.unbind()
                    logger.debug(f"用户 {username} 认证连接已关闭")
                except Exception as e:
                    logger.warning(f"关闭用户认证连接时发生异常: {e}")
    
    # ========== 账号管理 ==========
    
    def unlock_account(self, username: str) -> Tuple[bool, str]:
        """解锁账号"""
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
                    'ad'
                )
            
            # 使用AD扩展解锁
            self.conn.extend.microsoft.unlock_account(user=user_dn)
            
            logger.info(f"用户 {username} 账号解锁成功")
            return True, "账号解锁成功"
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"账号解锁失败: {e}")
            raise LDAPException(
                LDAPErrorCode.MODIFY_FAILED,
                f"账号解锁失败: {str(e)}",
                'ad',
                e
            )
    
    def is_account_locked(self, username: str) -> Tuple[bool, bool]:
        """检查账号是否锁定"""
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 搜索锁定时间属性
            self.conn.search(
                self.base_dn,
                self.search_filter.format(username),
                attributes=[self.lockout_attr]
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'ad'
                )
            
            # 获取属性值 - 使用 .value 属性获取实际值
            lockout_attr = self.conn.entries[0][self.lockout_attr]
            lockout_time_value = lockout_attr.value
            
            # AD的lockoutTime: 0表示未锁定，大于0表示锁定
            # 使用数值判断而非字符串匹配，更精确可靠
            if lockout_time_value is None:
                is_locked = False
            else:
                try:
                    # lockoutTime是整数类型
                    lockout_time_int = int(lockout_time_value)
                    is_locked = lockout_time_int != 0
                except (ValueError, TypeError):
                    # 如果转换失败，回退到字符串判断
                    lockout_time_str = str(lockout_time_value)
                    is_locked = lockout_time_str != '0' and '1601-01-01' not in lockout_time_str
            
            return True, is_locked
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"查询账号锁定状态失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"查询账号状态失败: {str(e)}",
                'ad',
                e
            )
    
    def is_account_disabled(self, username: str) -> Tuple[bool, bool]:
        """检查账号是否禁用"""
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 搜索userAccountControl属性
            self.conn.search(
                self.base_dn,
                self.search_filter.format(username),
                attributes=[self.account_control_attr]
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'ad'
                )
            
            # 获取属性值
            uac_attr = self.conn.entries[0][self.account_control_attr]
            uac_value = int(uac_attr.value) if uac_attr.value is not None else None
            
            if uac_value is None:
                logger.warning(f"用户 {username} 的 {self.account_control_attr} 属性为空")
                return True, False
            
            # 检查是否在禁用状态码列表中
            is_disabled = uac_value in self.disabled_codes
            
            return True, is_disabled
        
        except LDAPException:
            raise
        except (ValueError, TypeError) as e:
            logger.error(f"解析 {self.account_control_attr} 属性值失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"解析账号控制属性失败: {str(e)}",
                'ad',
                e
            )
        except Exception as e:
            logger.error(f"查询账号禁用状态失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"查询账号状态失败: {str(e)}",
                'ad',
                e
            )
    
    def get_account_status(self, username: str) -> Tuple[bool, Dict]:
        """获取账号状态信息"""
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 搜索账号状态相关属性
            self.conn.search(
                self.base_dn,
                self.search_filter.format(username),
                attributes=[
                    self.account_control_attr,
                    self.lockout_attr,
                    'pwdLastSet',
                    'accountExpires'
                ]
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'ad'
                )
            
            entry = self.conn.entries[0]
            
            # 解析状态 - 使用 .value 获取属性实际值
            uac_attr = entry[self.account_control_attr]
            uac_value = int(uac_attr.value) if uac_attr.value is not None else None
            
            lockout_attr = entry[self.lockout_attr]
            lockout_time = str(lockout_attr.value) if lockout_attr.value is not None else ''
            
            if uac_value is None:
                logger.warning(f"用户 {username} 的 {self.account_control_attr} 属性为空")
                uac_value = 0  # 默认值
            
            status = {
                'locked': '1601-01-01' not in lockout_time,
                'disabled': uac_value in self.disabled_codes,
                'expired': False,  # TODO: 解析accountExpires
                'password_expired': False,  # TODO: 解析pwdLastSet
                'details': {
                    'userAccountControl': uac_value,
                    'lockoutTime': lockout_time
                }
            }
            
            return True, status
        
        except LDAPException:
            raise
        except (ValueError, TypeError) as e:
            logger.error(f"解析账号状态属性值失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"解析账号状态属性失败: {str(e)}",
                'ad',
                e
            )
        except Exception as e:
            logger.error(f"查询账号状态失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"查询账号状态失败: {str(e)}",
                'ad',
                e
            )
    
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
                    'ad'
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
                'ad',
                e
            )
    
    def get_user_dn(self, username: str) -> Tuple[bool, str]:
        """获取用户DN"""
        try:
            # 格式验证
            is_valid, error_msg = LDAPEscape.validate_username(username)
            if not is_valid:
                raise LDAPException(
                    LDAPErrorCode.INVALID_PARAMETER,
                    f"用户名格式不正确: {error_msg}",
                    'ad'
                )
            
            # 如果配置了DN模板,直接使用
            if self.user_dn_template:
                # 转义username（防止DN注入）
                escaped_username = LDAPEscape.escape_dn_value(username)
                user_dn = self.user_dn_template.replace('{username}', escaped_username)
                logger.debug(f"使用DN模板（已转义）: {user_dn}")
                return True, user_dn
            
            # 确保连接
            if not self.is_connected():
                self.connect()
            
             # 转义username
            escaped_username = LDAPEscape.escape_filter_value(username)

            # 通过搜索获取
            self.conn.search(
                self.base_dn,
                self.search_filter.format(escaped_username),
                attributes=['distinguishedName']
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'ad'
                )
            
            user_dn = str(self.conn.entries[0]['distinguishedName'])
            return True, user_dn
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"获取用户DN失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"获取用户DN失败: {str(e)}",
                'ad',
                e
            )
    
    # ========== 组成员管理 ==========
    
    def get_user_groups(self, username: str) -> Tuple[bool, List[str]]:
        """获取用户所属组"""
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 搜索memberOf属性
            self.conn.search(
                self.base_dn,
                self.search_filter.format(username),
                attributes=[self.member_of_attr]
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'ad'
                )
            
            # 获取组DN列表
            member_of = self.conn.entries[0][self.member_of_attr]
            group_dns = [str(dn) for dn in member_of] if member_of else []
            
            logger.debug(f"用户 {username} 所属组: {group_dns}")
            return True, group_dns
        
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"查询用户组失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"查询用户组失败: {str(e)}",
                'ad',
                e
            )
    
    def extract_group_name(self, group_dn: str) -> str:
        """从组DN中提取组名"""
        # AD格式: CN=Domain Admins,CN=Users,DC=company,DC=com
        # 提取第一个CN的值
        match = re.match(r'^CN=([^,]+)', group_dn, re.IGNORECASE)
        if match:
            return match.group(1)
        return group_dn
    
    # ========== 密码策略诊断 ==========
    
    def get_domain_password_policy(self) -> Dict:
        """
        读取域密码策略
        
        从域根对象（如 DC=abc,DC=com）读取密码策略属性。
        
        Returns:
            包含以下键的字典:
            - minPwdAge: 最小密码期限（100纳秒间隔，负数）
            - pwdHistoryLength: 密码历史长度
            - minPwdLength: 最小密码长度
            - pwdProperties: 密码复杂度标志
            - maxPwdAge: 最大密码期限（可选）
            - lockoutThreshold: 锁定阈值（可选）
            - lockoutDuration: 锁定持续时间（可选）
        
        Raises:
            LDAPException: 读取失败时抛出
        """
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 构建域根DN（从base_dn提取）
            # base_dn 格式: DC=abc,DC=com -> 直接使用
            domain_dn = self.base_dn
            
            # 密码策略属性列表
            policy_attrs = [
                'minPwdAge',           # 最小密码期限
                'pwdHistoryLength',    # 密码历史长度
                'minPwdLength',        # 最小密码长度
                'pwdProperties',       # 密码复杂度标志
                'maxPwdAge',           # 最大密码期限
                'lockoutThreshold',    # 锁定阈值
                'lockoutDuration'      # 锁定持续时间
            ]
            
            # 搜索域根对象
            self.conn.search(
                search_base=domain_dn,
                search_filter='(objectClass=domain)',
                attributes=policy_attrs
            )
            
            if not self.conn.entries:
                logger.warning(f"未找到域对象: {domain_dn}")
                return {}
            
            entry = self.conn.entries[0]
            policy = {}
            
            # 提取策略值
            for attr in policy_attrs:
                try:
                    attr_value = entry[attr].value
                    if attr_value is not None:
                        # 数值类型转换
                        if attr in ['minPwdAge', 'pwdHistoryLength', 'minPwdLength',
                                   'pwdProperties', 'maxPwdAge', 'lockoutThreshold',
                                   'lockoutDuration']:
                            policy[attr] = int(attr_value)
                        else:
                            policy[attr] = attr_value
                except (KeyError, TypeError, ValueError) as e:
                    logger.debug(f"读取属性 {attr} 失败: {e}")
            
            logger.info(f"成功读取域密码策略: {list(policy.keys())}")
            logger.debug(f"密码策略详情: {policy}")
            
            return policy
            
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"读取域密码策略失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"读取域密码策略失败: {str(e)}",
                'ad',
                e
            )
    
    def get_user_password_attrs(self, username: str) -> Dict:
        """
        读取用户密码相关属性
        
        读取用于密码诊断的用户属性。
        
        Args:
            username: 用户名
        
        Returns:
            包含以下键的字典:
            - pwdLastSet: 上次密码修改时间（AD时间戳）
            - badPwdCount: 错误密码计数
            - lockoutTime: 锁定时间
            - userAccountControl: 账户控制标志
        
        Raises:
            LDAPException: 读取失败时抛出
        """
        try:
            # 确保连接
            if not self.is_connected():
                self.connect()
            
            # 密码相关属性
            password_attrs = [
                'pwdLastSet',          # 上次密码修改时间
                'badPwdCount',         # 错误密码计数
                'lockoutTime',         # 锁定时间
                'userAccountControl'   # 账户控制标志
            ]
            
            # 搜索用户
            self.conn.search(
                self.base_dn,
                self.search_filter.format(username),
                attributes=password_attrs
            )
            
            if not self.conn.entries:
                raise LDAPException(
                    LDAPErrorCode.ACCOUNT_NOT_FOUND,
                    f"用户 {username} 不存在",
                    'ad'
                )
            
            entry = self.conn.entries[0]
            user_attrs = {}
            
            # 提取属性值
            for attr in password_attrs:
                try:
                    attr_value = entry[attr].value
                    if attr_value is not None:
                        # 数值类型转换
                        if attr in ['pwdLastSet', 'badPwdCount', 'lockoutTime', 'userAccountControl']:
                            user_attrs[attr] = int(attr_value)
                        else:
                            user_attrs[attr] = attr_value
                    else:
                        user_attrs[attr] = 0
                except (KeyError, TypeError, ValueError) as e:
                    logger.debug(f"读取属性 {attr} 失败: {e}")
                    user_attrs[attr] = 0
            
            logger.debug(f"用户 {username} 密码属性: {user_attrs}")
            
            return user_attrs
            
        except LDAPException:
            raise
        except Exception as e:
            logger.error(f"读取用户密码属性失败: {e}")
            raise LDAPException(
                LDAPErrorCode.SEARCH_FAILED,
                f"读取用户密码属性失败: {str(e)}",
                'ad',
                e
            )
    
    def diagnose_password_error(self, username: str, new_password: str) -> str:
        """
        诊断密码错误的具体原因
        
        当密码修改失败（特别是0000052D错误）时，调用此方法分析具体原因。
        
        Args:
            username: 用户名
            new_password: 新密码（用于本地检查）
        
        Returns:
            精确的错误消息字符串
        """
        try:
            from .password_diagnostics import PasswordDiagnostics
            
            # 获取域密码策略
            policy = self.get_domain_password_policy()
            if not policy:
                logger.warning("无法获取域密码策略，使用通用错误消息")
                return "新密码不符合域密码策略要求，请检查密码是否符合复杂度、长度和历史记录要求。"
            
            # 获取用户密码属性
            user_attrs = self.get_user_password_attrs(username)
            if not user_attrs:
                logger.warning(f"无法获取用户 {username} 的密码属性")
                return "新密码不符合域密码策略要求，请检查密码是否符合复杂度、长度和历史记录要求。"
            
            # 执行诊断
            title, detail = PasswordDiagnostics.diagnose_52d_error(
                user_attrs, policy, new_password
            )
            
            # 格式化返回消息
            return PasswordDiagnostics.format_diagnosis_result(title, detail)
            
        except Exception as e:
            logger.error(f"密码诊断过程中发生异常: {e}")
            # 诊断失败时返回通用消息
            return "新密码不符合域密码策略要求，请检查密码是否符合复杂度、长度和历史记录要求。"
