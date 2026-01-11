# -*- coding: utf-8 -*-
"""
华为云 SMS 提供商

使用华为云短信服务发送验证码
文档: https://support.huaweicloud.com/devg-msgsms/sms_04_0001.html
"""
import base64
import hashlib
import hmac
import json
import time
from typing import Tuple, Optional
from datetime import datetime
import requests
from utils.logger_factory import get_logger
from ..base_provider import BaseSMSProvider
from ..errors import SMSException, SMSErrorCode

logger = get_logger(__name__)


class HuaweiSMSProvider(BaseSMSProvider):
    """
    华为云 SMS 提供商
    
    需要配置：
    - sms.huawei.app_key: APP Key
    - sms.huawei.app_secret: APP Secret
    - sms.huawei.sender: 短信通道号
    - sms.huawei.template_id: 模板ID
    - sms.huawei.signature: 短信签名（可选，某些场景需要）
    - sms.huawei.api_url: API地址（默认https://smsapi.cn-north-4.myhuaweicloud.com:443）
    """
    
    @property
    def provider_name(self) -> str:
        """提供商显示名称"""
        return "华为云SMS"
    
    @property
    def provider_type(self) -> str:
        """提供商类型标识"""
        return "huawei"
    
    def __init__(self):
        """初始化华为云SMS提供商"""
        super().__init__()
        
        # 从配置读取华为云参数
        self.app_key = self.config.get('sms.huawei.app_key', '')
        self.app_secret = self.config.get('sms.huawei.app_secret', '')
        self.sender = self.config.get('sms.huawei.sender', '')
        self.template_id = self.config.get('sms.huawei.template_id', '')
        self.signature = self.config.get('sms.huawei.signature', '')
        self.api_url = self.config.get(
            'sms.huawei.api_url',
            'https://smsapi.cn-north-4.myhuaweicloud.com:443'
        )
        
        logger.info(f"华为云SMS提供商初始化完成: sender={self.sender}")
    
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
        
        # 构建模板参数列表（华为云要求JSON数组格式）
        template_param_list = [code]
        if template_params:
            for value in template_params.values():
                template_param_list.append(str(value))
        
        # 华为云需要+86前缀
        phone_number = f"+86{formatted_mobile}"
        
        # 构建请求体
        body = {
            "from": self.sender,
            "to": [phone_number],
            "templateId": template_id_to_use,
            "templateParas": json.dumps(template_param_list),
        }
        
        # 如果配置了签名，添加到请求体
        if self.signature:
            body["signature"] = self.signature
        
        # 构建请求头
        headers = self._build_headers(body)
        
        # 发送请求
        url = f"{self.api_url}/sms/batchSendSms/v1"
        
        try:
            response = requests.post(url, json=body, headers=headers, timeout=10)
            response_data = response.json()
            
            # 检查结果
            result = response_data.get('result', [])
            if result and len(result) > 0:
                status = result[0]
                status_code = status.get('status', '')
                
                if status_code == '000000':
                    # 发送成功
                    msg_id = status.get('smsMsgId', '')
                    
                    self._log_send_success(
                        mobile=formatted_mobile,
                        code=code,
                        provider_msg_id=msg_id,
                        extra_info={
                            'template': template_id_to_use,
                            'sender': self.sender,
                        }
                    )
                    
                    return True, "验证码发送成功"
                else:
                    # 发送失败
                    error_message = status.get('statusMsg', status_code)
                    
                    self._log_send_failure(
                        mobile=formatted_mobile,
                        code=code,
                        error_code=status_code,
                        error_message=error_message
                    )
                    
                    # 映射常见错误
                    user_message = self._map_error_message(status_code)
                    
                    raise SMSException(
                        SMSErrorCode.SEND_FAILED,
                        user_message,
                        "send_verification_code",
                        context={'huawei_error': status_code}
                    )
            else:
                logger.error(f"华为云SMS返回空结果: {response_data}")
                raise SMSException(
                    SMSErrorCode.SEND_FAILED,
                    "短信发送失败，返回空结果",
                    "send_verification_code"
                )
                
        except requests.exceptions.RequestException as e:
            logger.error(f"华为云SMS请求异常: {e}")
            self._log_send_failure(
                mobile=formatted_mobile,
                code=code,
                error_code="REQUEST_ERROR",
                error_message=str(e)
            )
            raise SMSException(
                SMSErrorCode.SEND_FAILED,
                "短信发送失败，网络错误",
                "send_verification_code",
                e
            )
        except SMSException:
            raise
        except Exception as e:
            logger.error(f"华为云SMS发送异常: {e}")
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
            message_id: smsMsgId（发送时返回的消息ID）
            
        Returns:
            Tuple[查询成功, 发送状态, 状态描述]
        """
        # 华为云短信状态查询需要额外的接口，这里简化处理
        logger.warning(f"华为云SMS状态查询功能未完全实现，message_id={message_id}")
        return True, "unknown", "华为云状态查询需要额外配置"
    
    def validate_config(self):
        """验证华为云配置"""
        errors = []
        
        if not self.app_key:
            errors.append("缺少 sms.huawei.app_key")
        
        if not self.app_secret:
            errors.append("缺少 sms.huawei.app_secret")
        
        if not self.sender:
            errors.append("缺少 sms.huawei.sender")
        
        if not self.template_id:
            errors.append("缺少 sms.huawei.template_id")
        
        if errors:
            error_message = ", ".join(errors)
            logger.error(f"华为云SMS配置错误: {error_message}")
            raise SMSException(
                SMSErrorCode.CONFIG_MISSING_REQUIRED,
                f"华为云SMS配置不完整: {error_message}",
                "validate_config"
            )
        
        logger.debug("华为云SMS配置验证通过")
    
    def format_mobile(self, mobile: str) -> str:
        """
        格式化手机号（华为云需要不带+86的11位号码）
        
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
            'from': self.sender,
            'to': [f"+86{formatted_mobile}"],
            'templateId': self.template_id,
            'templateParas': json.dumps([code])
        }
    
    def _build_headers(self, body: dict) -> dict:
        """
        构建华为云API请求头（包含WSSE认证）
        
        华为云认证算法：
        1. 生成UTC时间戳: YYYY-MM-DDTHH:MM:SSZ
        2. 生成Nonce: 随机字符串（这里使用时间戳毫秒）
        3. 计算PasswordDigest: Base64(SHA256(Nonce + Created + AppSecret))
        4. 构建X-WSSE头
        
        Args:
            body: 请求体
            
        Returns:
            请求头字典
        """
        # 生成UTC时间戳
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # 生成Nonce（使用时间戳毫秒）
        nonce = str(int(time.time() * 1000))
        
        # 计算密码摘要: Base64(SHA256(Nonce + Created + AppSecret))
        digest_str = nonce + now + self.app_secret
        digest = hashlib.sha256(digest_str.encode('utf-8')).digest()
        password_digest = base64.b64encode(digest).decode('utf-8')
        
        # 构建WSSE头
        wsse_header = (
            f'UsernameToken Username="{self.app_key}", '
            f'PasswordDigest="{password_digest}", '
            f'Nonce="{nonce}", '
            f'Created="{now}"'
        )
        
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'WSSE realm="SDP",profile="UsernameToken",type="Appkey"',
            'X-WSSE': wsse_header
        }
        
        return headers
    
    def _map_error_message(self, error_code: str) -> str:
        """
        映射华为云错误码到用户友好消息
        
        华为云常见错误码：
        - 000000: 成功
        - E000001~E000014: 各种业务错误
        - E200xxx: 系统错误
        
        Args:
            error_code: 华为云错误码
            
        Returns:
            用户友好的错误消息
        """
        error_map = {
            '000000': '发送成功',
            'E000001': '参数格式错误',
            'E000002': '短信内容超长',
            'E000003': '手机号格式不正确',
            'E000004': '用户名或密码错误',
            'E000005': '余额不足',
            'E000006': '通道号不存在',
            'E000007': '模板ID不存在',
            'E000008': '签名不正确',
            'E000009': '超过发送频率限制',
            'E000010': '手机号在黑名单中',
            'E000011': '短信内容包含敏感词',
            'E000012': '模板参数不匹配',
            'E000013': '短信签名未审核',
            'E000014': '模板未审核',
            'E200033': '参数异常',
            'E200034': '请求超时',
            'E200035': '系统异常',
        }
        
        return error_map.get(error_code, f'短信发送失败: {error_code}')
