# -*- coding: utf-8 -*-
"""
腾讯云 SMS 提供商

使用腾讯云短信服务发送验证码
文档: https://cloud.tencent.com/document/product/382
"""
import json
from typing import Tuple, Optional
from utils.logger_factory import get_logger
from ..base_provider import BaseSMSProvider
from ..errors import SMSException, SMSErrorCode

logger = get_logger(__name__)


class TencentSMSProvider(BaseSMSProvider):
    """
    腾讯云 SMS 提供商
    
    需要配置：
    - sms.tencent.secret_id: SecretId
    - sms.tencent.secret_key: SecretKey
    - sms.tencent.sdk_app_id: 短信应用ID
    - sms.tencent.sign_name: 短信签名内容
    - sms.tencent.template_id: 模板ID
    - sms.tencent.region: 地域（默认ap-guangzhou）
    """
    
    @property
    def provider_name(self) -> str:
        """提供商显示名称"""
        return "腾讯云SMS"
    
    @property
    def provider_type(self) -> str:
        """提供商类型标识"""
        return "tencent"
    
    def __init__(self):
        """初始化腾讯云SMS提供商"""
        super().__init__()
        
        # 从配置读取腾讯云参数
        self.secret_id = self.config.get('sms.tencent.secret_id', '')
        self.secret_key = self.config.get('sms.tencent.secret_key', '')
        self.sdk_app_id = self.config.get('sms.tencent.sdk_app_id', '')
        self.sign_name = self.config.get('sms.tencent.sign_name', '')
        self.template_id = self.config.get('sms.tencent.template_id', '')
        self.region = self.config.get('sms.tencent.region', 'ap-guangzhou')
        
        # 初始化客户端
        self.client = None
        self._init_client()
        
        logger.info(f"腾讯云SMS提供商初始化完成: region={self.region}, sign={self.sign_name}")
    
    def _init_client(self):
        """初始化腾讯云SDK客户端"""
        try:
            from tencentcloud.common import credential
            from tencentcloud.sms.v20210111 import sms_client, models
            
            # 创建认证对象
            cred = credential.Credential(self.secret_id, self.secret_key)
            
            # 创建客户端
            self.client = sms_client.SmsClient(cred, self.region)
            self.models = models
            
            logger.debug("腾讯云SDK客户端初始化成功")
            
        except ImportError as e:
            logger.error("腾讯云SMS SDK未安装，请运行: pip install tencentcloud-sdk-python")
            raise SMSException(
                SMSErrorCode.CONFIG_INVALID,
                "腾讯云SMS SDK未安装",
                "_init_client",
                e
            )
        except Exception as e:
            logger.error(f"腾讯云SDK客户端初始化失败: {e}")
            raise SMSException(
                SMSErrorCode.CONFIG_INVALID,
                "腾讯云SMS配置错误",
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
            template_id: 模板ID（可选，默认使用配置的模板）
            template_params: 额外模板参数（可选）
            
        Returns:
            Tuple[成功, 消息]
        """
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
        template_id_to_use = template_id or self.template_id
        
        # 构建模板参数列表（腾讯云要求数组格式）
        template_param_list = [code]
        if template_params:
            # 如果有额外参数，添加到列表
            for value in template_params.values():
                template_param_list.append(str(value))
        
        try:
            # 创建请求
            req = self.models.SendSmsRequest()
            
            # 设置参数
            req.SmsSdkAppId = self.sdk_app_id
            req.SignName = self.sign_name
            req.TemplateId = template_id_to_use
            req.TemplateParamSet = template_param_list
            
            # 腾讯云需要+86前缀
            phone_number_set = [f"+86{formatted_mobile}"]
            req.PhoneNumberSet = phone_number_set
            
            # 发送请求
            response = self.client.SendSms(req)
            
            # 检查结果
            if response.SendStatusSet:
                send_status = response.SendStatusSet[0]
                
                if send_status.Code == "Ok":
                    serial_no = send_status.SerialNo or ""
                    
                    self._log_send_success(
                        mobile=formatted_mobile,
                        code=code,
                        provider_msg_id=serial_no,
                        extra_info={
                            'template': template_id_to_use,
                            'sign': self.sign_name,
                            'request_id': response.RequestId
                        }
                    )
                    
                    return True, "验证码发送成功"
                else:
                    # 发送失败
                    error_code = send_status.Code
                    error_message = send_status.Message
                    
                    self._log_send_failure(
                        mobile=formatted_mobile,
                        code=code,
                        error_code=error_code,
                        error_message=error_message,
                        extra_info={'request_id': response.RequestId}
                    )
                    
                    # 映射常见错误
                    user_message = self._map_error_message(error_code)
                    
                    raise SMSException(
                        SMSErrorCode.SEND_FAILED,
                        user_message,
                        "send_verification_code",
                        context={'tencent_error': error_code}
                    )
            else:
                logger.error("腾讯云SMS返回空结果")
                raise SMSException(
                    SMSErrorCode.SEND_FAILED,
                    "短信发送失败，返回空结果",
                    "send_verification_code"
                )
                
        except SMSException:
            raise
        except Exception as e:
            logger.error(f"腾讯云SMS发送异常: {e}")
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
            message_id: SerialNo（发送时返回的流水号）
            
        Returns:
            Tuple[查询成功, 发送状态, 状态描述]
        """
        try:
            req = self.models.PullSmsSendStatusRequest()
            req.SmsSdkAppId = self.sdk_app_id
            req.Limit = 10
            
            response = self.client.PullSmsSendStatus(req)
            
            # 查找匹配的消息
            if response.PullSmsSendStatusSet:
                for status in response.PullSmsSendStatusSet:
                    if status.SerialNo == message_id:
                        report_status = status.ReportStatus
                        
                        # 映射状态
                        if report_status == "SUCCESS":
                            return True, "delivered", "已送达"
                        elif report_status == "FAIL":
                            return True, "failed", f"发送失败: {status.Description}"
                        else:
                            return True, "unknown", f"未知状态: {report_status}"
            
            return True, "unknown", "未找到消息"
            
        except Exception as e:
            logger.error(f"腾讯云SMS状态查询失败: {e}")
            return False, "unknown", str(e)
    
    def validate_config(self):
        """验证腾讯云配置"""
        errors = []
        
        if not self.secret_id:
            errors.append("缺少 sms.tencent.secret_id")
        
        if not self.secret_key:
            errors.append("缺少 sms.tencent.secret_key")
        
        if not self.sdk_app_id:
            errors.append("缺少 sms.tencent.sdk_app_id")
        
        if not self.sign_name:
            errors.append("缺少 sms.tencent.sign_name")
        
        if not self.template_id:
            errors.append("缺少 sms.tencent.template_id")
        
        if errors:
            error_message = ", ".join(errors)
            logger.error(f"腾讯云SMS配置错误: {error_message}")
            raise SMSException(
                SMSErrorCode.CONFIG_MISSING_REQUIRED,
                f"腾讯云SMS配置不完整: {error_message}",
                "validate_config"
            )
        
        # 检查SDK是否安装
        try:
            from tencentcloud.sms.v20210111 import sms_client
        except ImportError:
            logger.error("腾讯云SMS SDK未安装")
            raise SMSException(
                SMSErrorCode.CONFIG_INVALID,
                "腾讯云SMS SDK未安装，请运行: pip install tencentcloud-sdk-python",
                "validate_config"
            )
        
        logger.debug("腾讯云SMS配置验证通过")
    
    def format_mobile(self, mobile: str) -> str:
        """
        格式化手机号（腾讯云需要不带+86的11位号码）
        
        Args:
            mobile: 原始手机号
            
        Returns:
            格式化后的手机号
        """
        # 移除空格和短横线
        mobile = mobile.replace(' ', '').replace('-', '')
        
        # 移除+86前缀
        if mobile.startswith('+86'):
            mobile = mobile[3:]
        elif mobile.startswith('86') and len(mobile) == 13:
            mobile = mobile[2:]
        
        # 验证11位手机号
        if len(mobile) == 11 and mobile.isdigit():
            return mobile
        else:
            return ""
    
    def get_send_params(self, mobile: str, code: str) -> dict:
        """
        获取发送参数
        
        Args:
            mobile: 手机号
            code: 验证码
            
        Returns:
            参数字典
        """
        formatted_mobile = self.format_mobile(mobile)
        return {
            'SmsSdkAppId': self.sdk_app_id,
            'SignName': self.sign_name,
            'TemplateId': self.template_id,
            'TemplateParamSet': [code],
            'PhoneNumberSet': [f"+86{formatted_mobile}"]
        }
    
    def _map_error_message(self, error_code: str) -> str:
        """
        映射腾讯云错误码到用户友好消息
        
        文档: https://cloud.tencent.com/document/api/382/52075
        
        Args:
            error_code: 腾讯云错误码
            
        Returns:
            用户友好的错误消息
        """
        error_map = {
            # ==================== 公共错误码 ====================
            # 认证相关
            'AuthFailure.InvalidAuthorization': '请求认证信息无效',
            'AuthFailure.InvalidSecretId': '密钥非法',
            'AuthFailure.SecretIdNotFound': '密钥不存在或已禁用',
            'AuthFailure.SignatureExpire': '签名已过期，请检查服务器时间',
            'AuthFailure.SignatureFailure': '签名错误',
            'AuthFailure.TokenFailure': 'Token错误',
            'AuthFailure.UnauthorizedOperation': '请求未授权',
            
            # 服务相关
            'ActionOffline': '接口已下线',
            'InternalError': '服务内部错误',
            'InvalidAction': '接口不存在',
            'InvalidParameter': '参数错误',
            'InvalidParameterValue': '参数取值错误',
            'MissingParameter': '缺少必要参数',
            'RequestLimitExceeded': '请求频率超限，请稍后重试',
            'RequestLimitExceeded.IPLimitExceeded': 'IP请求频率超限',
            'RequestLimitExceeded.UinLimitExceeded': '账号请求频率超限',
            'ServiceUnavailable': '服务暂时不可用',
            
            # ==================== 业务错误码 ====================
            # FailedOperation - 操作失败类
            'FailedOperation': '操作失败',
            'FailedOperation.ContainSensitiveWord': '短信内容包含敏感词，请联系管理员',
            'FailedOperation.FailResolvePacket': '请求包解析失败',
            'FailedOperation.InsufficientBalanceInSmsPackage': '短信套餐包余额不足',
            'FailedOperation.JsonParseFail': 'JSON解析失败',
            'FailedOperation.MarketingSendTimeConstraint': '营销短信只能在8点-22点发送',
            'FailedOperation.MissingSignature': '未申请签名',
            'FailedOperation.MissingSignatureList': '签名未审核通过',
            'FailedOperation.MissingTemplateList': '模板未审核通过',
            'FailedOperation.NotEnterpriseCertification': '需完成企业认证',
            'FailedOperation.OtherError': '其他错误，请联系管理员',
            'FailedOperation.ParametersOtherError': '参数错误，请联系管理员',
            'FailedOperation.PhoneNumberInBlacklist': '手机号在免打扰名单中',
            'FailedOperation.PhoneNumberParseFail': '手机号解析失败，请检查格式',
            'FailedOperation.SignatureIncorrectOrUnapproved': '签名未审批或格式错误',
            'FailedOperation.TemplateIncorrectOrUnapproved': '模板未审批或内容不匹配',
            'FailedOperation.TemplateParamSetNotMatchApprovedTemplate': '模板参数不匹配',
            'FailedOperation.TemplateUnapprovedOrNotExist': '模板未审批或不存在',
            
            # InternalError - 内部错误类
            'InternalError.JsonParseFail': '参数解析失败',
            'InternalError.OtherError': '服务内部错误',
            'InternalError.RequestTimeException': '请求时间异常，请检查服务器时间',
            'InternalError.Timeout': '请求超时，请稍后重试',
            'InternalError.SendAndRecvFail': '网络超时，请稍后重试',
            
            # InvalidParameter/InvalidParameterValue - 参数错误类
            'InvalidParameter.AppidAndBizId': '账号与应用ID不匹配',
            'InvalidParameter.DirtyWordFound': '存在敏感词',
            'InvalidParameter.InvalidParameters': '参数有误',
            'InvalidParameterValue.IncorrectPhoneNumber': '手机号格式错误',
            'InvalidParameterValue.ContentLengthLimit': '短信内容过长',
            'InvalidParameterValue.InvalidTemplateFormat': '模板格式错误',
            'InvalidParameterValue.TemplateParameterFormatError': '验证码格式错误，只能为0-6位纯数字',
            'InvalidParameterValue.TemplateParameterLengthLimit': '模板变量字符数超限',
            'InvalidParameterValue.TemplateWithDirtyWords': '模板内容存在敏感词',
            'InvalidParameterValue.SdkAppIdNotExist': 'SdkAppId不存在',
            
            # LimitExceeded - 限制类
            'LimitExceeded.AppDailyLimit': '应用日发送量已达上限',
            'LimitExceeded.AppMainlandChinaDailyLimit': '国内短信日发送量已达上限',
            'LimitExceeded.DailyLimit': '短信日发送量已达上限',
            'LimitExceeded.DeliveryFrequencyLimit': '触发发送频率限制',
            'LimitExceeded.PhoneNumberCountLimit': '单次提交手机号超过200个',
            'LimitExceeded.PhoneNumberDailyLimit': '该手机号今日接收次数已达上限',
            'LimitExceeded.PhoneNumberOneHourLimit': '该手机号1小时内接收次数已达上限',
            'LimitExceeded.PhoneNumberThirtySecondLimit': '该手机号30秒内接收次数已达上限',
            'LimitExceeded.PhoneNumberSameContentDailyLimit': '该手机号接收相同内容次数已达上限',
            
            # UnauthorizedOperation - 未授权类
            'UnauthorizedOperation.IndividualUserMarketingSmsPermissionDeny': '个人用户无营销短信权限',
            'UnauthorizedOperation.RequestIpNotInWhitelist': '请求IP不在白名单中',
            'UnauthorizedOperation.RequestPermissionDeny': '无请求权限',
            'UnauthorizedOperation.SdkAppIdIsDisabled': '应用已被禁用',
            'UnauthorizedOperation.ServiceSuspendDueToArrears': '服务已欠费停用',
            'UnauthorizedOperation.SmsSdkAppIdVerifyFail': 'SdkAppId校验失败',
            
            # UnsupportedOperation - 不支持操作类
            'UnsupportedOperation.ChineseMainlandTemplateToGlobalPhone': '国内短信模板不支持国际手机号',
            'UnsupportedOperation.GlobalTemplateToChineseMainlandPhone': '国际短信模板不支持国内手机号',
            'UnsupportedOperation.ContainDomesticAndInternationalPhoneNumber': '不能同时发送国内外手机号',
            'UnsupportedOperation.UnsupportedRegion': '不支持该地区短信发送',
        }
        
        return error_map.get(error_code, f'短信发送失败: {error_code}')
