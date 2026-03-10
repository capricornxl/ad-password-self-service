# -*- coding: utf-8 -*-
"""
LDAP 错误码映射表和友好消息

包含:
- AD 特有错误码映射 (Windows 错误码)
- 标准 LDAP 错误码映射 (RFC 4511)
- OpenLDAP 特有错误码映射 (PPolicy 等)
"""

from typing import Dict, Optional, Tuple, Any


# =============================================================================
# Active Directory 错误码映射
# 参考: https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes
# =============================================================================

AD_ERROR_MESSAGES: Dict[str, Dict[str, str]] = {
    # -------------------------------------------------------------------------
    # 密码策略相关错误
    # -------------------------------------------------------------------------
    '0000052D': {
        'en': 'Password does not meet password policy requirements',
        'zh': '密码不符合密码策略要求。可能原因：密码历史限制、密码复杂度不足、密码最小长度未满足、密码最大使用期限未到等',
        'category': 'password_policy'
    },
    '0000052E': {
        'en': 'Logon failure: unknown user name or bad password',
        'zh': '登录失败：用户名不存在或密码错误',
        'category': 'authentication'
    },
    '0000052F': {
        'en': 'Logon failure: account restriction',
        'zh': '登录失败：账户受到限制',
        'category': 'account_restriction'
    },
    '00000530': {
        'en': 'Logon failure: invalid logon hours',
        'zh': '登录失败：不在允许的登录时间段内',
        'category': 'account_restriction'
    },
    '00000531': {
        'en': 'Logon failure: invalid workstation',
        'zh': '登录失败：不允许从此工作站登录',
        'category': 'account_restriction'
    },
    '00000532': {
        'en': 'Logon failure: password expired',
        'zh': '登录失败：密码已过期',
        'category': 'password_expired'
    },
    '00000533': {
        'en': 'Logon failure: account currently disabled',
        'zh': '登录失败：账户已禁用',
        'category': 'account_disabled'
    },
    '00000525': {
        'en': 'The specified account does not exist',
        'zh': '指定的账户不存在',
        'category': 'account_not_found'
    },
    '00000701': {
        'en': 'The user account has expired',
        'zh': '用户账户已过期',
        'category': 'account_expired'
    },
    '00000773': {
        'en': 'The user must change their password before logging on',
        'zh': '用户必须在登录前修改密码',
        'category': 'password_must_change'
    },
    '00000775': {
        'en': 'The referenced account is currently locked out',
        'zh': '账户已锁定，请联系管理员解锁',
        'category': 'account_locked'
    },
    '00000776': {
        'en': 'The user password has expired',
        'zh': '用户密码已过期',
        'category': 'password_expired'
    },
    '00000777': {
        'en': 'The user account has expired',
        'zh': '用户账户已过期',
        'category': 'account_expired'
    },
    '00000570': {
        'en': 'The user account has automatically expired',
        'zh': '用户账户已自动过期',
        'category': 'account_expired'
    },
    '000006A6': {
        'en': 'The password is too short or does not meet password policy requirements',
        'zh': '密码太短或不符合密码策略要求',
        'category': 'password_policy'
    },
    
    # -------------------------------------------------------------------------
    # 权限和安全相关错误
    # -------------------------------------------------------------------------
    '00000005': {
        'en': 'Access is denied',
        'zh': '访问被拒绝，权限不足',
        'category': 'permission_denied'
    },
    '00000522': {
        'en': 'A required privilege is not held by the client',
        'zh': '客户端没有所需的权限',
        'category': 'permission_denied'
    },
    '00000534': {
        'en': 'No mapping between account names and security IDs was done',
        'zh': '无法将账户名映射到安全标识符',
        'category': 'account_error'
    },
    '00000535': {
        'en': 'The specified account password has expired',
        'zh': '指定的账户密码已过期',
        'category': 'password_expired'
    },
    '00000536': {
        'en': 'The specified account is locked out',
        'zh': '指定的账户已锁定',
        'category': 'account_locked'
    },
    
    # -------------------------------------------------------------------------
    # 连接和服务器相关错误
    # -------------------------------------------------------------------------
    '000020EF': {
        'en': 'The server is not operational',
        'zh': '服务器无法操作，请检查网络连接',
        'category': 'connection_error'
    },
    '000020F8': {
        'en': 'The LDAP server is unavailable',
        'zh': 'LDAP 服务器不可用',
        'category': 'connection_error'
    },
    '000020FD': {
        'en': 'The LDAP server requires a secure connection',
        'zh': 'LDAP 服务器需要安全连接 (SSL/TLS)',
        'category': 'connection_error'
    },
    
    # -------------------------------------------------------------------------
    # 数据和属性相关错误
    # -------------------------------------------------------------------------
    '00002071': {
        'en': 'The attribute cannot be modified because it is owned by the system',
        'zh': '属性由系统所有，无法修改',
        'category': 'attribute_error'
    },
    '0000207D': {
        'en': 'The specified value is invalid for the attribute',
        'zh': '指定的属性值无效',
        'category': 'attribute_error'
    },
    '0000208D': {
        'en': 'The object does not exist',
        'zh': '对象不存在',
        'category': 'object_not_found'
    },
    '00002097': {
        'en': 'The object already exists',
        'zh': '对象已存在',
        'category': 'object_exists'
    },
    
    # -------------------------------------------------------------------------
    # 密码历史和复杂度相关详细错误 (扩展)
    # -------------------------------------------------------------------------
    '0000052C': {
        'en': 'Logon failure: the user has not been granted the requested logon type',
        'zh': '登录失败：用户未被授予请求的登录类型',
        'category': 'account_restriction'
    },
    '00000537': {
        'en': 'The user account has time restrictions and may not be logged onto at this time',
        'zh': '用户账户有时间限制，当前时间不允许登录',
        'category': 'account_restriction'
    },
}

# AD 错误码简写映射 (用于部分系统只返回简写形式)
AD_ERROR_SHORT_CODES: Dict[str, str] = {
    '52D': '0000052D',
    '52E': '0000052E',
    '52F': '0000052F',
    '530': '00000530',
    '531': '00000531',
    '532': '00000532',
    '533': '00000533',
    '525': '00000525',
    '701': '00000701',
    '773': '00000773',
    '775': '00000775',
    '776': '00000776',
    '777': '00000777',
    '005': '00000005',
    '522': '00000522',
    '534': '00000534',
    '535': '00000535',
    '536': '00000536',
}


# =============================================================================
# 标准 LDAP 错误码映射 (RFC 4511)
# 参考: https://www.rfc-editor.org/rfc/rfc4511#section-4.1.9
# =============================================================================

LDAP_ERROR_MESSAGES: Dict[int, Dict[str, str]] = {
    # -------------------------------------------------------------------------
    # 成功
    # -------------------------------------------------------------------------
    0: {
        'name': 'success',
        'en': 'The operation completed successfully',
        'zh': '操作成功完成',
        'category': 'success'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 1-9: 一般错误
    # -------------------------------------------------------------------------
    1: {
        'name': 'operationsError',
        'en': 'An operations error occurred',
        'zh': '服务器遇到内部错误',
        'category': 'server_error'
    },
    2: {
        'name': 'protocolError',
        'en': 'A protocol error was detected',
        'zh': '协议错误，客户端发送了错误格式的请求',
        'category': 'protocol_error'
    },
    3: {
        'name': 'timeLimitExceeded',
        'en': 'The time limit for the operation was exceeded',
        'zh': '操作超时',
        'category': 'timeout'
    },
    4: {
        'name': 'sizeLimitExceeded',
        'en': 'The size limit for the operation was exceeded',
        'zh': '搜索结果超过大小限制',
        'category': 'limit_exceeded'
    },
    5: {
        'name': 'compareFalse',
        'en': 'The compare operation returned false',
        'zh': '比较操作返回 false',
        'category': 'compare_result'
    },
    6: {
        'name': 'compareTrue',
        'en': 'The compare operation returned true',
        'zh': '比较操作返回 true',
        'category': 'compare_result'
    },
    7: {
        'name': 'authMethodNotSupported',
        'en': 'The authentication method is not supported',
        'zh': '不支持此认证方法',
        'category': 'authentication'
    },
    8: {
        'name': 'strongerAuthRequired',
        'en': 'A stronger authentication method is required',
        'zh': '需要更强的认证方法（如 SASL 或 TLS）',
        'category': 'authentication'
    },
    9: {
        'name': 'partialResults',
        'en': 'Partial results and referral received',
        'zh': '收到部分结果和引用',
        'category': 'referral'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 10-15: 引用和限制相关
    # -------------------------------------------------------------------------
    10: {
        'name': 'referral',
        'en': 'A referral was returned',
        'zh': '服务器返回了引用',
        'category': 'referral'
    },
    11: {
        'name': 'adminLimitExceeded',
        'en': 'An administrative limit was exceeded',
        'zh': '超过管理限制',
        'category': 'limit_exceeded'
    },
    12: {
        'name': 'unavailableCriticalExtension',
        'en': 'A critical extension is not available',
        'zh': '关键扩展不可用',
        'category': 'extension_error'
    },
    13: {
        'name': 'confidentialityRequired',
        'en': 'Confidentiality is required',
        'zh': '需要保密连接（TLS/SSL）',
        'category': 'security'
    },
    14: {
        'name': 'saslBindInProgress',
        'en': 'SASL bind in progress',
        'zh': 'SASL 绑定正在进行中',
        'category': 'authentication'
    },
    15: {
        'name': 'noSuchAttribute',
        'en': 'The attribute type does not exist in the entry',
        'zh': '条目中不存在指定的属性',
        'category': 'attribute_error'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 16-21: 属性相关错误
    # -------------------------------------------------------------------------
    16: {
        'name': 'undefinedAttributeTypes',
        'en': 'The attribute type is not defined',
        'zh': '属性类型未定义',
        'category': 'attribute_error'
    },
    17: {
        'name': 'inappropriateMatching',
        'en': 'The matching rule is inappropriate',
        'zh': '匹配规则不合适',
        'category': 'attribute_error'
    },
    18: {
        'name': 'constraintViolation',
        'en': 'A constraint violation occurred',
        'zh': '约束违规，属性值不符合定义的约束',
        'category': 'constraint_error'
    },
    19: {
        'name': 'attributeOrValueExists',
        'en': 'The attribute or value already exists',
        'zh': '属性或值已存在',
        'category': 'attribute_error'
    },
    20: {
        'name': 'invalidAttributeSyntax',
        'en': 'The attribute syntax is invalid',
        'zh': '属性语法无效',
        'category': 'attribute_error'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 32-36: 名称相关错误
    # -------------------------------------------------------------------------
    32: {
        'name': 'noSuchObject',
        'en': 'The specified object does not exist',
        'zh': '指定的对象不存在',
        'category': 'not_found'
    },
    33: {
        'name': 'aliasProblem',
        'en': 'An alias problem occurred',
        'zh': '别名问题',
        'category': 'name_error'
    },
    34: {
        'name': 'invalidDNSyntax',
        'en': 'The distinguished name syntax is invalid',
        'zh': '可分辨名称 (DN) 语法无效',
        'category': 'name_error'
    },
    35: {
        'name': 'isLeaf',
        'en': 'The entry is a leaf entry',
        'zh': '条目是叶节点',
        'category': 'name_error'
    },
    36: {
        'name': 'aliasDereferencingProblem',
        'en': 'An alias dereferencing problem occurred',
        'zh': '别名解引用问题',
        'category': 'name_error'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 48-54: 安全和认证相关错误
    # -------------------------------------------------------------------------
    48: {
        'name': 'inappropriateAuthentication',
        'en': 'The authentication is inappropriate',
        'zh': '认证方式不合适，可能需要使用更强的认证',
        'category': 'authentication'
    },
    49: {
        'name': 'invalidCredentials',
        'en': 'The provided credentials are invalid',
        'zh': '凭据无效，用户名或密码错误',
        'category': 'authentication'
    },
    50: {
        'name': 'insufficientAccessRights',
        'en': 'The user has insufficient access rights',
        'zh': '权限不足，无法执行此操作',
        'category': 'permission_denied'
    },
    51: {
        'name': 'busy',
        'en': 'The server is busy',
        'zh': '服务器繁忙，请稍后重试',
        'category': 'server_error'
    },
    52: {
        'name': 'unavailable',
        'en': 'The server is unavailable',
        'zh': '服务器不可用',
        'category': 'server_error'
    },
    53: {
        'name': 'unwillingToPerform',
        'en': 'The server is unwilling to perform the operation',
        'zh': '服务器拒绝执行此操作',
        'category': 'server_error'
    },
    54: {
        'name': 'loopDetect',
        'en': 'A loop was detected',
        'zh': '检测到循环引用',
        'category': 'server_error'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 64-71: 更新相关错误
    # -------------------------------------------------------------------------
    64: {
        'name': 'namingViolation',
        'en': 'A naming violation occurred',
        'zh': '命名违规',
        'category': 'update_error'
    },
    65: {
        'name': 'objectClassViolation',
        'en': 'An object class violation occurred',
        'zh': '对象类违规',
        'category': 'update_error'
    },
    66: {
        'name': 'notAllowedOnNonLeaf',
        'en': 'The operation is not allowed on a non-leaf entry',
        'zh': '不允许在非叶节点上执行此操作',
        'category': 'update_error'
    },
    67: {
        'name': 'notAllowedOnRDN',
        'en': 'The operation is not allowed on the RDN',
        'zh': '不允许在 RDN 上执行此操作',
        'category': 'update_error'
    },
    68: {
        'name': 'entryAlreadyExists',
        'en': 'The entry already exists',
        'zh': '条目已存在',
        'category': 'update_error'
    },
    69: {
        'name': 'objectClassModsProhibited',
        'en': 'Object class modifications are prohibited',
        'zh': '禁止修改对象类',
        'category': 'update_error'
    },
    71: {
        'name': 'affectsMultipleDSAs',
        'en': 'The operation affects multiple DSAs',
        'zh': '操作影响多个目录服务代理',
        'category': 'update_error'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 80: 其他错误
    # -------------------------------------------------------------------------
    80: {
        'name': 'other',
        'en': 'An unknown error occurred',
        'zh': '发生未知错误',
        'category': 'unknown'
    },
    
    # -------------------------------------------------------------------------
    # 结果码 81-90: 连接相关错误 (ldap3 扩展)
    # -------------------------------------------------------------------------
    81: {
        'name': 'serverDown',
        'en': 'The LDAP server is down',
        'zh': 'LDAP 服务器已关闭或无法连接',
        'category': 'connection_error'
    },
    82: {
        'name': 'localError',
        'en': 'A local error occurred',
        'zh': '本地错误',
        'category': 'local_error'
    },
    83: {
        'name': 'encodingError',
        'en': 'An encoding error occurred',
        'zh': '编码错误',
        'category': 'protocol_error'
    },
    84: {
        'name': 'decodingError',
        'en': 'A decoding error occurred',
        'zh': '解码错误',
        'category': 'protocol_error'
    },
    85: {
        'name': 'timeout',
        'en': 'The operation timed out',
        'zh': '操作超时',
        'category': 'timeout'
    },
    86: {
        'name': 'authUnknown',
        'en': 'Unknown authentication method',
        'zh': '未知的认证方法',
        'category': 'authentication'
    },
    87: {
        'name': 'filterError',
        'en': 'The search filter is invalid',
        'zh': '搜索过滤器无效',
        'category': 'search_error'
    },
    88: {
        'name': 'userCancelled',
        'en': 'The operation was cancelled by the user',
        'zh': '操作被用户取消',
        'category': 'cancelled'
    },
    89: {
        'name': 'paramError',
        'en': 'A parameter error occurred',
        'zh': '参数错误',
        'category': 'parameter_error'
    },
    90: {
        'name': 'noMemory',
        'en': 'Out of memory',
        'zh': '内存不足',
        'category': 'resource_error'
    },
    91: {
        'name': 'connectError',
        'en': 'A connection error occurred',
        'zh': '连接错误，无法连接到 LDAP 服务器',
        'category': 'connection_error'
    },
    92: {
        'name': 'notSupported',
        'en': 'The operation is not supported',
        'zh': '不支持此操作',
        'category': 'not_supported'
    },
    93: {
        'name': 'controlNotFound',
        'en': 'The control was not found',
        'zh': '未找到控制',
        'category': 'control_error'
    },
    94: {
        'name': 'noResultsReturned',
        'en': 'No results were returned',
        'zh': '未返回结果',
        'category': 'search_error'
    },
    95: {
        'name': 'moreResultsToReturn',
        'en': 'More results are available',
        'zh': '还有更多结果可返回',
        'category': 'search_error'
    },
    96: {
        'name': 'clientLoop',
        'en': 'Client detected a loop',
        'zh': '客户端检测到循环',
        'category': 'referral'
    },
    97: {
        'name': 'referralLimitExceeded',
        'en': 'Referral hop limit exceeded',
        'zh': '超过引用跳转限制',
        'category': 'referral'
    },
}


# =============================================================================
# OpenLDAP PPolicy 扩展错误码
# 参考: https://www.openldap.org/doc/admin24/overlays.html#Password%20Policies
# =============================================================================

OPENLDAP_PPOLICY_ERRORS: Dict[int, Dict[str, str]] = {
    0: {
        'name': 'passwordExpired',
        'en': 'The password has expired',
        'zh': '密码已过期',
        'category': 'password_expired'
    },
    1: {
        'name': 'accountLocked',
        'en': 'The account has been locked',
        'zh': '账户已锁定',
        'category': 'account_locked'
    },
    2: {
        'name': 'changeAfterReset',
        'en': 'Password must be changed after reset',
        'zh': '密码重置后必须更改',
        'category': 'password_must_change'
    },
    3: {
        'name': 'passwordModNotAllowed',
        'en': 'Password modification is not allowed',
        'zh': '不允许修改密码',
        'category': 'permission_denied'
    },
    4: {
        'name': 'mustSupplyOldPassword',
        'en': 'Must supply the old password to change',
        'zh': '必须提供旧密码才能更改',
        'category': 'authentication'
    },
    5: {
        'name': 'insufficientPasswordQuality',
        'en': 'The password does not meet quality requirements',
        'zh': '密码不符合质量要求（复杂度不足）',
        'category': 'password_policy'
    },
    6: {
        'name': 'passwordTooShort',
        'en': 'The password is too short',
        'zh': '密码太短',
        'category': 'password_policy'
    },
    7: {
        'name': 'passwordTooYoung',
        'en': 'The password has been changed too recently',
        'zh': '密码最近已更改，请等待后再试',
        'category': 'password_policy'
    },
    8: {
        'name': 'passwordInHistory',
        'en': 'The password is in the history of old passwords',
        'zh': '密码不能与最近使用过的密码相同',
        'category': 'password_policy'
    },
}

# OpenLDAP 密码策略错误码 (Behera 草案)
# 参考: draft-behera-ldap-password-policy-10
BEHERA_PPOLICY_ERROR_CODES: Dict[int, Dict[str, str]] = {
    0: {
        'name': 'passwordExpired',
        'en': 'The password has expired and must be reset',
        'zh': '密码已过期，必须重置',
        'category': 'password_expired'
    },
    1: {
        'name': 'accountLocked',
        'en': 'The account has been locked due to too many failed login attempts',
        'zh': '账户因多次登录失败已锁定',
        'category': 'account_locked'
    },
    2: {
        'name': 'changeAfterReset',
        'en': 'Password must be changed after a reset operation',
        'zh': '密码重置后必须更改',
        'category': 'password_must_change'
    },
    3: {
        'name': 'passwordModNotAllowed',
        'en': 'User is not allowed to change their password',
        'zh': '用户不允许修改自己的密码',
        'category': 'permission_denied'
    },
    4: {
        'name': 'mustSupplyOldPassword',
        'en': 'Must provide the old password to change to a new password',
        'zh': '必须提供旧密码才能设置新密码',
        'category': 'authentication'
    },
    5: {
        'name': 'insufficientPasswordQuality',
        'en': 'The password does not meet the quality requirements',
        'zh': '密码不符合质量要求（可能需要更复杂的密码）',
        'category': 'password_policy'
    },
    6: {
        'name': 'passwordTooShort',
        'en': 'The password is shorter than the minimum required length',
        'zh': '密码长度不足',
        'category': 'password_policy'
    },
    7: {
        'name': 'passwordTooYoung',
        'en': 'The password was changed too recently to be changed again',
        'zh': '密码最近已更改，需等待更长时间才能再次更改',
        'category': 'password_policy'
    },
    8: {
        'name': 'passwordInHistory',
        'en': 'The password is already in the password history',
        'zh': '密码不能与历史密码重复',
        'category': 'password_policy'
    },
}


# =============================================================================
# 工具函数
# =============================================================================

def get_ad_error_message(error_code: str, lang: str = 'zh') -> Optional[Dict[str, str]]:
    """
    获取 AD 错误码对应的友好消息
    
    Args:
        error_code: AD 错误码，支持完整格式 (0000052D) 或简写格式 (52D)
        lang: 语言，'zh' 或 'en'
    
    Returns:
        错误信息字典，包含 'message' 和 'category'，未找到返回 None
    """
    # 标准化错误码格式
    normalized_code = error_code.upper()
    
    # 尝试完整格式
    if normalized_code in AD_ERROR_MESSAGES:
        error_info = AD_ERROR_MESSAGES[normalized_code]
        return {
            'message': error_info.get(lang, error_info.get('zh', '')),
            'category': error_info.get('category', 'unknown'),
            'code': normalized_code
        }
    
    # 尝试简写格式
    if normalized_code in AD_ERROR_SHORT_CODES:
        full_code = AD_ERROR_SHORT_CODES[normalized_code]
        if full_code in AD_ERROR_MESSAGES:
            error_info = AD_ERROR_MESSAGES[full_code]
            return {
                'message': error_info.get(lang, error_info.get('zh', '')),
                'category': error_info.get('category', 'unknown'),
                'code': full_code
            }
    
    return None


def get_ldap_error_message(error_code: int, lang: str = 'zh') -> Optional[Dict[str, str]]:
    """
    获取标准 LDAP 错误码对应的友好消息
    
    Args:
        error_code: LDAP 结果码 (整数)
        lang: 语言，'zh' 或 'en'
    
    Returns:
        错误信息字典，包含 'name', 'message' 和 'category'，未找到返回 None
    """
    if error_code in LDAP_ERROR_MESSAGES:
        error_info = LDAP_ERROR_MESSAGES[error_code]
        return {
            'name': error_info.get('name', ''),
            'message': error_info.get(lang, error_info.get('zh', '')),
            'category': error_info.get('category', 'unknown'),
            'code': error_code
        }
    
    return None


def get_ppolicy_error_message(error_code: int, lang: str = 'zh') -> Optional[Dict[str, str]]:
    """
    获取 OpenLDAP PPolicy 错误码对应的友好消息
    
    Args:
        error_code: PPolicy 错误码 (整数)
        lang: 语言，'zh' 或 'en'
    
    Returns:
        错误信息字典，包含 'name', 'message' 和 'category'，未找到返回 None
    """
    if error_code in BEHERA_PPOLICY_ERROR_CODES:
        error_info = BEHERA_PPOLICY_ERROR_CODES[error_code]
        return {
            'name': error_info.get('name', ''),
            'message': error_info.get(lang, error_info.get('zh', '')),
            'category': error_info.get('category', 'unknown'),
            'code': error_code
        }
    
    return None


def parse_ad_error_from_string(error_str: str, lang: str = 'zh') -> Optional[Dict[str, str]]:
    """
    从 AD 错误字符串中解析错误码并返回友好消息
    
    AD 错误字符串通常格式为 "0000052D: ..." 或包含 "data 525" 等
    
    Args:
        error_str: AD 错误消息字符串
        lang: 语言，'zh' 或 'en'
    
    Returns:
        错误信息字典，未找到返回 None
    """
    import re
    
    # 尝试匹配完整格式 "0000052D" 或 "data 525" 或 "52D"
    patterns = [
        r'([0-9A-Fa-f]{8})',           # 完整8位错误码: 0000052D
        r'data\s+([0-9A-Fa-f]{3,4})',   # data 后跟错误码: data 525
        r'([0-9A-Fa-f]{3,4})[:\s]',     # 简写错误码后跟冒号或空格: 52D:
    ]
    
    for pattern in patterns:
        match = re.search(pattern, error_str, re.IGNORECASE)
        if match:
            error_code = match.group(1).upper()
            # 尝试补全为完整格式
            if len(error_code) < 8:
                error_code = error_code.zfill(8)
            
            result = get_ad_error_message(error_code, lang)
            if result:
                return result
            
            # 尝试原始格式
            result = get_ad_error_message(match.group(1).upper(), lang)
            if result:
                return result
    
    return None


def parse_ldap_error(error_result: Any, ldap_type: str = 'ad', lang: str = 'zh') -> Dict[str, str]:
    """
    解析 LDAP 错误结果，返回友好消息
    
    统一处理 AD 和 OpenLDAP 的错误，优先使用错误码映射表，
    匹配不到则返回原始错误信息
    
    Args:
        error_result: ldap3 的错误结果对象或异常
        ldap_type: LDAP 类型，'ad' 或 'openldap'
        lang: 语言，'zh' 或 'en'
    
    Returns:
        包含友好消息的字典:
        - 'message': 友好消息
        - 'category': 错误类别
        - 'original': 原始错误信息
        - 'code': 错误码 (如果有)
    """
    import re
    
    result = {
        'message': '',
        'category': 'unknown',
        'original': '',
        'code': None
    }
    
    # 提取原始错误信息
    if hasattr(error_result, 'message') and error_result.message:
        result['original'] = str(error_result.message)
    elif hasattr(error_result, 'description') and error_result.description:
        result['original'] = str(error_result.description)
    elif isinstance(error_result, dict):
        result['original'] = str(error_result)
    else:
        result['original'] = str(error_result)
    
    # 尝试解析 AD 错误
    if ldap_type.lower() == 'ad':
        # 尝试从字符串中解析 AD 错误码
        ad_result = parse_ad_error_from_string(result['original'], lang)
        if ad_result:
            result['message'] = ad_result['message']
            result['category'] = ad_result['category']
            result['code'] = ad_result['code']
            return result
        
        # 尝试解析 LDAP 结果码
        if hasattr(error_result, 'result'):
            ldap_result = get_ldap_error_message(error_result.result, lang)
            if ldap_result:
                result['message'] = ldap_result['message']
                result['category'] = ldap_result['category']
                result['code'] = ldap_result['code']
                return result
    
    # 尝试解析 OpenLDAP 错误
    elif ldap_type.lower() == 'openldap':
        # 尝试解析 LDAP 结果码
        result_code = None
        if hasattr(error_result, 'result'):
            result_code = error_result.result
        elif isinstance(error_result, dict) and 'result' in error_result:
            result_code = error_result['result']
        
        if result_code is not None:
            ldap_result = get_ldap_error_message(result_code, lang)
            if ldap_result:
                result['message'] = ldap_result['message']
                result['category'] = ldap_result['category']
                result['code'] = ldap_result['code']
                return result
        
        # 尝试解析 PPolicy 错误
        if hasattr(error_result, 'controls'):
            # 检查 PPolicy 响应控制
            ppolicy_control = error_result.controls.get('1.3.6.1.4.1.42.2.27.8.5.1')
            if ppolicy_control and hasattr(ppolicy_control, 'error'):
                ppolicy_result = get_ppolicy_error_message(ppolicy_control.error, lang)
                if ppolicy_result:
                    result['message'] = ppolicy_result['message']
                    result['category'] = ppolicy_result['category']
                    result['code'] = ppolicy_result['code']
                    return result
    
    # 尝试解析标准 LDAP 错误码 (通用)
    if hasattr(error_result, 'result'):
        ldap_result = get_ldap_error_message(error_result.result, lang)
        if ldap_result:
            result['message'] = ldap_result['message']
            result['category'] = ldap_result['category']
            result['code'] = ldap_result['code']
            return result
    
    # 未找到匹配的错误码，返回原始错误
    result['message'] = result['original']
    return result


def get_friendly_error_message(error_result: Any, ldap_type: str = 'ad', lang: str = 'zh') -> str:
    """
    获取用户友好的错误消息
    
    这是 parse_ldap_error 的便捷包装函数，只返回消息字符串
    
    Args:
        error_result: ldap3 的错误结果对象或异常
        ldap_type: LDAP 类型，'ad' 或 'openldap'
        lang: 语言，'zh' 或 'en'
    
    Returns:
        用户友好的错误消息字符串
    """
    result = parse_ldap_error(error_result, ldap_type, lang)
    return result.get('message', '未知错误')


# =============================================================================
# 错误类别到统一错误码的映射
# =============================================================================

ERROR_CATEGORY_TO_LDAP_ERROR_CODE: Dict[str, int] = {
    'authentication': 1001,          # LDAPErrorCode.INVALID_CREDENTIALS
    'account_locked': 1002,          # LDAPErrorCode.ACCOUNT_LOCKED
    'account_disabled': 1003,        # LDAPErrorCode.ACCOUNT_DISABLED
    'password_expired': 1004,        # LDAPErrorCode.PASSWORD_EXPIRED
    'password_must_change': 1005,    # LDAPErrorCode.PASSWORD_MUST_CHANGE
    'account_expired': 1006,         # LDAPErrorCode.ACCOUNT_EXPIRED
    'account_not_found': 1007,       # LDAPErrorCode.ACCOUNT_NOT_FOUND
    'password_policy': 2001,         # LDAPErrorCode.PASSWORD_POLICY_VIOLATION
    'permission_denied': 3005,       # LDAPErrorCode.INSUFFICIENT_PERMISSION
    'connection_error': 3001,        # LDAPErrorCode.CONNECTION_FAILED
    'server_error': 3001,            # LDAPErrorCode.CONNECTION_FAILED
    'not_found': 4004,               # LDAPErrorCode.ENTRY_NOT_FOUND
    'unknown': 5001,                 # LDAPErrorCode.UNKNOWN_ERROR
}


def category_to_error_code(category: str) -> int:
    """
    将错误类别转换为统一的 LDAP 错误码
    
    Args:
        category: 错误类别字符串
    
    Returns:
        统一的 LDAP 错误码 (LDAPErrorCode)
    """
    return ERROR_CATEGORY_TO_LDAP_ERROR_CODE.get(category, 5001)  # 默认返回 UNKNOWN_ERROR


# =============================================================================
# 导出列表
# =============================================================================

__all__ = [
    # 错误码映射表
    'AD_ERROR_MESSAGES',
    'AD_ERROR_SHORT_CODES',
    'LDAP_ERROR_MESSAGES',
    'OPENLDAP_PPOLICY_ERRORS',
    'BEHERA_PPOLICY_ERROR_CODES',
    
    # 工具函数
    'get_ad_error_message',
    'get_ldap_error_message',
    'get_ppolicy_error_message',
    'parse_ad_error_from_string',
    'parse_ldap_error',
    'get_friendly_error_message',
    
    # 类别映射
    'ERROR_CATEGORY_TO_LDAP_ERROR_CODE',
    'category_to_error_code',
]