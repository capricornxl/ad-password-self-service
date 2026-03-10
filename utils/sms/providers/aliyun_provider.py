# -*- coding: utf-8 -*-
"""
阿里云 SMS 提供商

使用阿里云短信服务发送验证码
新版 SDK: alibabacloud_dysmsapi20170525
文档: https://help.aliyun.com/zh/sms/developer-reference/using-python-openapi-example
"""
import json
import os
from typing import Tuple, Optional
from utils.logger_factory import get_logger
from ..base_provider import BaseSMSProvider
from ..errors import SMSException, SMSErrorCode

logger = get_logger(__name__)


class AliyunSMSProvider(BaseSMSProvider):
    """
    阿里云 SMS 提供商
    
    需要配置：
    - sms.aliyun.access_key_id: AccessKey ID
    - sms.aliyun.access_key_secret: AccessKey Secret
    - sms.aliyun.sign_name: 短信签名
    - sms.aliyun.template_code: 模板CODE
    - sms.aliyun.region_id: 地域ID（默认cn-hangzhou）
    """
    
    @property
    def provider_name(self) -> str:
        """提供商显示名称"""
        return "阿里云SMS"
    
    @property
    def provider_type(self) -> str:
        """提供商类型标识"""
        return "aliyun"
    
    def __init__(self):
        """初始化阿里云SMS提供商"""
        super().__init__()
        
        # 从配置读取阿里云参数
        self.access_key_id = self.config.get('sms.aliyun.access_key_id', '')
        self.access_key_secret = self.config.get('sms.aliyun.access_key_secret', '')
        self.sign_name = self.config.get('sms.aliyun.sign_name', '')
        self.template_code = self.config.get('sms.aliyun.template_code', '')
        self.region_id = self.config.get('sms.aliyun.region_id', 'cn-hangzhou')
        
        # 初始化客户端
        self.client = None
        self._init_client()
        
        logger.info(f"阿里云SMS提供商初始化完成: region={self.region_id}, sign={self.sign_name}")
    
    def _init_client(self):
        """初始化阿里云SDK客户端（新版 Tea SDK）"""
        try:
            from alibabacloud_dysmsapi20170525.client import Client
            from alibabacloud_tea_openapi import models as open_api_models
            
            # 创建配置
            config = open_api_models.Config(
                access_key_id=self.access_key_id,
                access_key_secret=self.access_key_secret,
            )
            # 设置 endpoint
            config.endpoint = 'dysmsapi.aliyuncs.com'
            
            # 创建客户端
            self.client = Client(config)
            
            logger.debug("阿里云SDK客户端初始化成功（新版 Tea SDK）")
            
        except ImportError as e:
            logger.error("阿里云SMS SDK未安装，请运行: pip install alibabacloud_dysmsapi20170525")
            raise SMSException(
                SMSErrorCode.SDK_NOT_INSTALLED,
                "阿里云SMS SDK未安装，请运行: pip install alibabacloud_dysmsapi20170525 alibabacloud_tea_openapi",
                "_init_client",
                e
            )
        except Exception as e:
            logger.error(f"阿里云SDK客户端初始化失败: {e}")
            raise SMSException(
                SMSErrorCode.CONFIG_INVALID,
                f"阿里云SMS配置错误: {e}",
                "_init_client",
                e
            )
    
    def send_verification_code(
        self,
        mobile: str,
        code: str,
        template_id: Optional[str] = None,
        template_params: Optional[dict] = None
    ) -> Tuple[bool, str]:
        """
        发送验证码
        
        Args:
            mobile: 手机号
            code: 验证码
            template_id: 模板CODE（可选，默认使用配置的模板）
            template_params: 额外模板参数（可选）
            
        Returns:
            Tuple[成功, 消息]
        """
        try:
            from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
        except ImportError:
            logger.error("阿里云SMS SDK未安装")
            raise SMSException(
                SMSErrorCode.SDK_NOT_INSTALLED,
                "阿里云SMS SDK未安装，请运行: pip install alibabacloud_dysmsapi20170525",
                "send_verification_code"
            )
        
        # 格式化手机号
        formatted_mobile = self.format_mobile(mobile)
        if not formatted_mobile:
            self._log_send_failure(
                mobile=mobile,
                code=code,
                error_code="INVALID_MOBILE",
                error_message="手机号格式不正确"
            )
            raise SMSException(
                SMSErrorCode.MOBILE_INVALID_FORMAT,
                "手机号格式不正确",
                "send_verification_code"
            )
        
        # 使用指定模板或默认模板
        template_code = template_id or self.template_code
        
        # 构建模板参数
        params = {'code': code}
        if template_params:
            params.update(template_params)
        
        try:
            # 创建发送请求
            send_sms_request = dysmsapi_models.SendSmsRequest(
                phone_numbers=formatted_mobile,
                sign_name=self.sign_name,
                template_code=template_code,
                template_param=json.dumps(params)
            )
            
            # 发送请求
            response = self.client.send_sms(send_sms_request)
            
            # 解析响应
            if response.body and response.body.code == 'OK':
                biz_id = response.body.biz_id or ''
                
                self._log_send_success(
                    mobile=formatted_mobile,
                    code=code,
                    provider_msg_id=biz_id,
                    extra_info={
                        'template': template_code,
                        'sign': self.sign_name,
                        'request_id': response.body.request_id
                    }
                )
                
                return True, "验证码发送成功"
            else:
                # 发送失败
                error_code = response.body.code if response.body else 'UNKNOWN'
                error_message = response.body.message if response.body else '未知错误'
                
                self._log_send_failure(
                    mobile=formatted_mobile,
                    code=code,
                    error_code=error_code,
                    error_message=error_message,
                    extra_info={'response': str(response.body) if response.body else None}
                )
                
                # 映射常见错误
                user_message = self._map_error_message(error_code)
                
                raise SMSException(
                    SMSErrorCode.SEND_FAILED,
                    user_message,
                    "send_verification_code",
                    context={'aliyun_error': error_code}
                )
                
        except SMSException:
            raise
        except Exception as e:
            logger.error(f"阿里云SMS发送异常: {e}")
            self._log_send_failure(
                mobile=formatted_mobile,
                code=code,
                error_code="EXCEPTION",
                error_message=str(e)
            )
            raise SMSException(
                SMSErrorCode.SEND_FAILED,
                "短信发送失败，请稍后重试",
                "send_verification_code",
                e
            )
    
    def query_send_status(self, message_id: str) -> Tuple[bool, str, str]:
        """
        查询发送状态
        
        Args:
            message_id: BizId（发送时返回的业务ID）
            
        Returns:
            Tuple[查询成功, 发送状态, 状态描述]
        """
        try:
            from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
        except ImportError:
            logger.error("阿里云SMS SDK未安装")
            return False, "unknown", "SDK未安装"
        
        # 由于需要手机号和发送日期，这里简化处理
        # 实际项目中需要在发送时保存这些信息
        logger.warning(f"阿里云SMS状态查询需要手机号和日期，message_id={message_id}")
        return True, "unknown", "需要更多参数"
    
    def validate_config(self):
        """验证阿里云配置"""
        errors = []
        
        if not self.access_key_id:
            errors.append("缺少 sms.aliyun.access_key_id")
        
        if not self.access_key_secret:
            errors.append("缺少 sms.aliyun.access_key_secret")
        
        if not self.sign_name:
            errors.append("缺少 sms.aliyun.sign_name")
        
        if not self.template_code:
            errors.append("缺少 sms.aliyun.template_code")
        
        if errors:
            error_message = ", ".join(errors)
            logger.error(f"阿里云SMS配置错误: {error_message}")
            raise SMSException(
                SMSErrorCode.CONFIG_MISSING_REQUIRED,
                f"阿里云SMS配置不完整: {error_message}",
                "validate_config"
            )
        
        # 检查SDK是否安装
        try:
            import alibabacloud_dysmsapi20170525
        except ImportError:
            logger.error("阿里云SMS SDK未安装")
            raise SMSException(
                SMSErrorCode.SDK_NOT_INSTALLED,
                "阿里云SMS SDK未安装，请运行: pip install alibabacloud_dysmsapi20170525",
                "validate_config"
            )
        
        logger.debug("阿里云SMS配置验证通过")
    
    def format_mobile(self, mobile: str) -> str:
        """
        格式化手机号（阿里云支持国际号码）
        
        Args:
            mobile: 原始手机号
            
        Returns:
            格式化后的手机号
        """
        # 移除空格和短横线
        mobile = mobile.replace(' ', '').replace('-', '')
        
        # 如果没有国家代码，验证中国大陆手机号
        if not mobile.startswith('+'):
            # 移除86前缀
            if mobile.startswith('86') and len(mobile) == 13:
                mobile = mobile[2:]
            
            # 验证11位手机号
            if len(mobile) == 11 and mobile.isdigit():
                return mobile
            else:
                return ""
        
        # 国际号码直接返回
        return mobile
    
    def get_send_params(self, mobile: str, code: str) -> dict:
        """
        获取发送参数
        
        Args:
            mobile: 手机号
            code: 验证码
            
        Returns:
            参数字典
        """
        return {
            'PhoneNumbers': self.format_mobile(mobile),
            'SignName': self.sign_name,
            'TemplateCode': self.template_code,
            'TemplateParam': json.dumps({'code': code})
        }
    
    def _map_error_message(self, error_code: str) -> str:
        """
        映射阿里云错误码到用户友好消息
        
        文档: https://help.aliyun.com/zh/sms/developer-reference/api-error-codes
        
        Args:
            error_code: 阿里云错误码
            
        Returns:
            用户友好的错误消息
        """
        error_map = {
            # ==================== 账户/权限错误 ====================
            'isv.ACCOUNT_NOT_EXISTS': '账户不存在，请检查AccessKey',
            'isv.ACCOUNT_ABNORMAL': '账户异常，请联系客服',
            'isv.OUT_OF_SERVICE': '业务已停机，请及时充值',
            'isv.AMOUNT_NOT_ENOUGH': '账户余额不足，请及时充值',
            'isv.PRODUCT_UN_SUBSCRIPT': '未开通短信服务，请先开通',
            'isv.PRODUCT_UNSUBSCRIBE': '产品未开通',
            'isp.RAM_PERMISSION_DENY': 'RAM权限不足，请授权',
            'isv.SECURITY_FROZEN_ACCOUNT': '账号已被安全冻结，请联系商务经理',
            
            # ==================== 签名相关错误 ====================
            'isv.SMS_SIGNATURE_ILLEGAL': '该账号下找不到对应签名',
            'isv.SMS_SIGN_ILLEGAL': '签名禁止使用',
            'isv.SIGN_STATE_ILLEGAL': '签名状态不可用',
            'isv.SIGN_NAME_ILLEGAL': '签名名称不符合规范',
            'isv.SIGNATURE_BLACKLIST': '签名内容涉及违规信息',
            'isv.SMS_SIGNATURE_SCENE_ILLEGAL': '签名和模板类型不一致',
            'isv.SIGN_COUNT_OVER_LIMIT': '超过单日签名申请数量上限',
            'isv.SIGN_OVER_LIMIT': '签名字符数量超过限制',
            'isv.SIGN_FILE_LIMIT': '签名认证材料附件大小超过限制',
            'isv.SIGN_SOURCE_ILLEGAL': '签名来源不支持',
            'isv.SMS_SIGN_EMOJI_ILLEGAL': '签名不能包含emoji表情',
            'isv.ERROR_SIGN_NOT_DELETE': '审核中的签名暂时无法删除',
            'isv.ERROR_SIGN_NOT_MODIFY': '已通过的签名不支持修改',
            'isv.EXTEND_CODE_ERROR': '扩展码使用错误',
            'isv.ONE_CODE_MULTIPLE_SIGN': '一码多签，扩展码对应签名不一致',
            'isv.CODE_EXCEED_LIMIT': '扩展码个数已超过上限',
            'isv.CODE_ERROR': '传入扩展码不可用',
            
            # ==================== 模板相关错误 ====================
            'isv.SMS_TEMPLATE_ILLEGAL': '模板未审核或内容不匹配',
            'isv.TEMPLATE_MISSING_PARAMETERS': '模板变量中存在未赋值变量',
            'isv.TEMPLATE_PARAMS_ILLEGAL': '模板参数与变量属性类型不匹配',
            'template_parameter_count_illegal': '验证码模板仅支持一个验证码变量',
            'isv.TEMPLATE_COUNT_OVER_LIMIT': '超过单日模板申请数量上限',
            'isv.TEMPLATE_OVER_LIMIT': '模板字符数量超过限制',
            'isv.ERROR_TEMPLATE_NOT_DELETE': '审核中的模板暂时无法删除',
            'isv.ERROR_TEMPLATE_NOT_MODIFY': '已通过的模板不支持修改',
            'isv.SMS_TEST_SIGN_TEMPLATE_LIMIT': '测试签名和模板必须结合使用',
            'isv.SMS_TEST_TEMPLATE_PARAMS_ILLEGAL': '测试模板变量仅支持4~6位纯数字',
            
            # ==================== 手机号相关错误 ====================
            'isv.MOBILE_NUMBER_ILLEGAL': '手机号格式不正确',
            'isv.MOBILE_COUNT_OVER_LIMIT': '手机号数量超过限制',
            'isv.DOMESTIC_NUMBER_NOT_SUPPORTED': '国际模板不支持发送国内号码',
            'isv.SMS_TEST_NUMBER_LIMIT': '只能向已绑定的测试手机号发送',
            'MOBILE_NOT_ON_SERVICE': '手机号停机、空号或不在服务区',
            'MOBILE_SEND_LIMIT': '该手机号发送频率超限',
            'MOBILE_ACCOUNT_ABNORMAL': '手机号账户异常或欠费',
            'MOBILE_IN_BLACK': '手机号在黑名单中',
            'MOBLLE_TERMINAL_ERROR': '手机终端问题，请检查设备',
            'INVALID_NUMBER': '号码状态异常',
            
            # ==================== 内容相关错误 ====================
            'isv.SMS_CONTENT_ILLEGAL': '短信内容包含禁止发送内容',
            'isv.PARAM_LENGTH_LIMIT': '参数超过长度限制',
            'isv.PARAM_NOT_SUPPORT_URL': '变量不支持传入URL',
            'isv.INVALID_JSON_PARAM': '参数格式错误，请使用JSON格式',
            'isv.INVALID_PARAMETERS': '参数格式不正确',
            'PARAMS_ILLEGAL': '参数错误，请检查签名、模板或手机号',
            'isv.UNSUPPORTED_CONTENT': '短信内容包含不支持的字符',
            'isv.SMS_CONTENT_MISMATCH_TEMPLATE_TYPE': '短信内容和模板属性不匹配',
            'CONTENT_KEYWORD': '内容包含敏感关键字',
            'CONTENT_ERROR': '推广短信必须包含退订信息',
            'isv.BLACK_KEY_CONTROL_LIMIT': '手机号在免打扰名单中',
            'isv.CUSTOMER_REFUSED': '用户已退订推广短信',
            
            # ==================== 流控/限额错误 ====================
            'isv.BUSINESS_LIMIT_CONTROL': '触发流控限制，请稍后重试',
            'isv.DAY_LIMIT_CONTROL': '今日发送次数已达上限',
            'isv.MONTH_LIMIT_CONTROL': '本月发送次数已达上限',
            'isv.SMS_OVER_LIMIT': '超过单日申请数量上限',
            
            # ==================== 服务/系统错误 ====================
            'isp.SYSTEM_ERROR': '系统错误，请重新调用',
            'isp.GATEWAY_ERROR': '网关错误，请重试',
            'IS_CLOSE': '短信通道暂时关闭，请稍后重试',
            'NO_ROUTE': '当前内容无可用通道发送',
            'SP_UNKNOWN_ERROR': '运营商未知错误',
            'REQUEST_SUCCESS': '请求已接收，等待运营商回执',
            
            # ==================== 认证/签名错误 ====================
            'SignatureDoesNotMatch': 'AccessKey签名错误',
            'InvalidAccessKeyId.NotFound': 'AccessKey ID不存在',
            'InvalidTimeStamp.Expired': '请求时间戳已过期',
            'SignatureNonceUsed': '签名随机数已被使用',
            'InvalidVersion': 'API版本号错误',
            'InvalidAction.NotFound': '接口地址或名称错误',
            
            # ==================== 其他错误 ====================
            'isv.DENY_IP_RANGE': 'IP地址所在地区被禁用',
            'PORT_NOT_REGISTERED': '签名未完成实名制报备',
            'SP_NOT_BY_INTER_SMS': '收件人未开通国际短信',
            'USER_REJECT': '用户已退订此业务',
        }
        
        return error_map.get(error_code, f'短信发送失败: {error_code}')