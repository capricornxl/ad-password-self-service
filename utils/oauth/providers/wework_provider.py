# -*- coding: utf-8 -*-
from typing import Tuple, Optional, Dict, Any
from utils.config import get_config
from utils.oauth.base_provider import BaseOAuthProvider
from utils.storage.memorystorage import get_token_storage
from utils.storage.cache import WeWorkCache
from utils.wework_api.abstract_api import ApiException, AbstractApi
from utils.logger_factory import get_logger

logger = get_logger(__name__)


class WeWorkProvider(BaseOAuthProvider, AbstractApi):
    """企业微信OAuth提供商"""
    
    # API类型定义
    CORP_API_TYPE = {
        'GET_USER_TICKET_OAUTH2': ['/cgi-bin/auth/getuserinfo?access_token=ACCESS_TOKEN', 'GET'],
        'GET_USER_INFO_OAUTH2': ['/cgi-bin/auth/getuserdetail?access_token=ACCESS_TOKEN', 'POST'],
        'GET_ACCESS_TOKEN': ['/cgi-bin/gettoken', 'GET'],
        'USER_CREATE': ['/cgi-bin/user/create?access_token=ACCESS_TOKEN', 'POST'],
        'USER_GET': ['/cgi-bin/user/get?access_token=ACCESS_TOKEN', 'GET'],
        'USER_UPDATE': ['/cgi-bin/user/update?access_token=ACCESS_TOKEN', 'POST'],
        'USER_DELETE': ['/cgi-bin/user/delete?access_token=ACCESS_TOKEN', 'GET'],
        'USER_BATCH_DELETE': ['/cgi-bin/user/batchdelete?access_token=ACCESS_TOKEN', 'POST'],
        'USER_SIMPLE_LIST': ['/cgi-bin/user/simplelist?access_token=ACCESS_TOKEN', 'GET'],
        'USER_LIST': ['/cgi-bin/user/list?access_token=ACCESS_TOKEN', 'GET'],
        'USERID_TO_OPENID': ['/cgi-bin/user/convert_to_openid?access_token=ACCESS_TOKEN', 'POST'],
        'OPENID_TO_USERID': ['/cgi-bin/user/convert_to_userid?access_token=ACCESS_TOKEN', 'POST'],
        'USER_AUTH_SUCCESS': ['/cgi-bin/user/authsucc?access_token=ACCESS_TOKEN', 'GET'],
        'DEPARTMENT_CREATE': ['/cgi-bin/department/create?access_token=ACCESS_TOKEN', 'POST'],
        'DEPARTMENT_UPDATE': ['/cgi-bin/department/update?access_token=ACCESS_TOKEN', 'POST'],
        'DEPARTMENT_DELETE': ['/cgi-bin/department/delete?access_token=ACCESS_TOKEN', 'GET'],
        'DEPARTMENT_LIST': ['/cgi-bin/department/list?access_token=ACCESS_TOKEN', 'GET'],
        'TAG_CREATE': ['/cgi-bin/tag/create?access_token=ACCESS_TOKEN', 'POST'],
        'TAG_UPDATE': ['/cgi-bin/tag/update?access_token=ACCESS_TOKEN', 'POST'],
        'TAG_DELETE': ['/cgi-bin/tag/delete?access_token=ACCESS_TOKEN', 'GET'],
        'TAG_GET_USER': ['/cgi-bin/tag/get?access_token=ACCESS_TOKEN', 'GET'],
        'TAG_ADD_USER': ['/cgi-bin/tag/addtagusers?access_token=ACCESS_TOKEN', 'POST'],
        'TAG_DELETE_USER': ['/cgi-bin/tag/deltagusers?access_token=ACCESS_TOKEN', 'POST'],
        'TAG_GET_LIST': ['/cgi-bin/tag/list?access_token=ACCESS_TOKEN', 'GET'],
        'BATCH_JOB_GET_RESULT': ['/cgi-bin/batch/getresult?access_token=ACCESS_TOKEN', 'GET'],
        'BATCH_INVITE': ['/cgi-bin/batch/invite?access_token=ACCESS_TOKEN', 'POST'],
        'AGENT_GET': ['/cgi-bin/agent/get?access_token=ACCESS_TOKEN', 'GET'],
        'AGENT_SET': ['/cgi-bin/agent/set?access_token=ACCESS_TOKEN', 'POST'],
        'AGENT_GET_LIST': ['/cgi-bin/agent/list?access_token=ACCESS_TOKEN', 'GET'],
        'MENU_CREATE': ['/cgi-bin/menu/create?access_token=ACCESS_TOKEN', 'POST'],
        'MENU_GET': ['/cgi-bin/menu/get?access_token=ACCESS_TOKEN', 'GET'],
        'MENU_DELETE': ['/cgi-bin/menu/delete?access_token=ACCESS_TOKEN', 'GET'],
        'MESSAGE_SEND': ['/cgi-bin/message/send?access_token=ACCESS_TOKEN', 'POST'],
        'MESSAGE_REVOKE': ['/cgi-bin/message/revoke?access_token=ACCESS_TOKEN', 'POST'],
        'MEDIA_GET': ['/cgi-bin/media/get?access_token=ACCESS_TOKEN', 'GET'],
        'GET_USER_INFO_BY_CODE': ['/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN', 'GET'],
        'GET_USER_DETAIL': ['/cgi-bin/user/getuserdetail?access_token=ACCESS_TOKEN', 'POST'],
        'GET_TICKET': ['/cgi-bin/ticket/get?access_token=ACCESS_TOKEN', 'GET'],
        'GET_JSAPI_TICKET': ['/cgi-bin/get_jsapi_ticket?access_token=ACCESS_TOKEN', 'GET'],
        'GET_CHECKIN_OPTION': ['/cgi-bin/checkin/getcheckinoption?access_token=ACCESS_TOKEN', 'POST'],
        'GET_CHECKIN_DATA': ['/cgi-bin/checkin/getcheckindata?access_token=ACCESS_TOKEN', 'POST'],
        'GET_APPROVAL_DATA': ['/cgi-bin/corp/getapprovaldata?access_token=ACCESS_TOKEN', 'POST'],
        'GET_INVOICE_INFO': ['/cgi-bin/card/invoice/reimburse/getinvoiceinfo?access_token=ACCESS_TOKEN', 'POST'],
        'UPDATE_INVOICE_STATUS':
            ['/cgi-bin/card/invoice/reimburse/updateinvoicestatus?access_token=ACCESS_TOKEN', 'POST'],
        'BATCH_UPDATE_INVOICE_STATUS':
            ['/cgi-bin/card/invoice/reimburse/updatestatusbatch?access_token=ACCESS_TOKEN', 'POST'],
        'BATCH_GET_INVOICE_INFO':
            ['/cgi-bin/card/invoice/reimburse/getinvoiceinfobatch?access_token=ACCESS_TOKEN', 'POST'],

        'APP_CHAT_CREATE': ['/cgi-bin/appchat/create?access_token=ACCESS_TOKEN', 'POST'],
        'APP_CHAT_GET': ['/cgi-bin/appchat/get?access_token=ACCESS_TOKEN', 'GET'],
        'APP_CHAT_UPDATE': ['/cgi-bin/appchat/update?access_token=ACCESS_TOKEN', 'POST'],
        'APP_CHAT_SEND': ['/cgi-bin/appchat/send?access_token=ACCESS_TOKEN', 'POST'],

        'MINIPROGRAM_CODE_TO_SESSION_KEY': ['/cgi-bin/miniprogram/jscode2session?access_token=ACCESS_TOKEN', 'GET'],
    }

    def __init__(self):
        """初始化企业微信提供商"""
        BaseOAuthProvider.__init__(self)
        AbstractApi.__init__(self)
        
        config = get_config()
        wework_config = config.get_dict('oauth_providers.wework')
        
        self._corp_id = wework_config.get('corp_id')
        self._agent_id = wework_config.get('agent_id')
        self._agent_secret = wework_config.get('agent_secret')
        
        # 使用全局token存储单例，确保多个实例共享token
        self._storage = get_token_storage()
        self.cache = WeWorkCache(self._storage, "wework:corp_id:%s" % self._corp_id)
    
    @property
    def provider_name(self) -> str:
        """提供商名称"""
        return "企业微信"
    
    @property
    def provider_type(self) -> str:
        """提供商类型"""
        return "wework"
    
    @property
    def corp_id(self) -> str:
        """企业ID"""
        return self._corp_id
    
    @property
    def app_id(self) -> str:
        """应用ID"""
        return self._corp_id
    
    @property
    def agent_id(self) -> str:
        """应用代理ID"""
        return self._agent_id
    
    def access_token(self):
        """获取access_token，优先从缓存获取"""
        access_token = self.cache.access_token.get()
        if access_token is None:
            ret = self.get_access_token()
            access_token = ret['access_token']
            expires_in = ret.get('expires_in', 7200)
            self.cache.access_token.set(value=access_token, ttl=expires_in)
        return access_token
    
    def get_access_token(self):
        """获取access_token"""
        return self.http_call(
            self.CORP_API_TYPE['GET_ACCESS_TOKEN'],
            {
                'corpid': self._corp_id,
                'corpsecret': self._agent_secret,
            })
    
    def get_user_id_by_code(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        通过授权码获取用户ID（增强版）
        
        Args:
            code: 授权码（有效期约 3-5 分钟）
            
        Returns:
            (成功状态, 用户ID 或 错误信息)
        """
        try:
            logger.debug(f"[企业微信] 通过免登码获取用户信息, code={code[:10]}...")
            result = self.http_call(
                self.CORP_API_TYPE['GET_USER_TICKET_OAUTH2'],
                {'code': code}
            )
            
            # 兼容多种字段格式（UserId/userid/user_id）
            user_id = result.get('UserId') or result.get('userid') or result.get('user_id')
            
            if user_id:
                logger.info(f"[企业微信] 成功获取 user_id: {user_id}")
                return True, user_id
            else:
                logger.warning(f"[企业微信] 响应中缺少 userid 字段: {result}")
                return False, "获取用户ID失败: 响应数据不完整"
                
        except ApiException as e:
            # 处理常见错误码
            error_code = getattr(e, 'errCode', 'unknown')
            error_msg = getattr(e, 'errMsg', str(e))
            
            if error_code == 40029:
                logger.error(f"[企业微信] 授权码无效或已过期: {error_code}-{error_msg}")
                return False, "授权码已过期，请重新扫码授权"
            elif error_code == 40014:
                logger.error(f"[企业微信] access_token 无效: {error_code}-{error_msg}")
                # 清除缓存的 token，下次会重新获取
                self.cache.access_token.delete()
                return False, "系统凭证失效，请重试"
            else:
                logger.error(f"[企业微信] 获取用户ID API异常: {error_code}-{error_msg}")
                return False, f"API 错误: {error_code}-{error_msg}"
                
        except Exception as e:
            logger.exception(f"[企业微信] 获取用户ID异常: {str(e)}")
            return False, f"获取用户ID异常: {str(e)}"
    
    def get_user_detail_by_user_id(self, user_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        通过用户ID获取用户详情（增强版）
        
        Args:
            user_id: 用户ID
            
        Returns:
            (成功状态, 用户信息字典 或 错误信息)
        """
        try:
            logger.debug(f"[企业微信] 通过 user_id 获取用户详情, user_id={user_id}")
            user_info = self.http_call(
                self.CORP_API_TYPE['USER_GET'],
                {'userid': user_id}
            )
            
            # 提取关键字段（兼容不同版本的 API 返回）
            user_name = user_info.get('name') or user_info.get('Name') or user_id
            user_email = user_info.get('email') or user_info.get('biz_mail') or user_info.get('Email')
            user_mobile = user_info.get('mobile') or user_info.get('Mobile')
            
            logger.info(f"[企业微信] 成功获取用户详情: name={user_name}, email={user_email}, mobile={user_mobile}")
            return True, user_info
            
        except ApiException as e:
            error_code = getattr(e, 'errCode', 'unknown')
            error_msg = getattr(e, 'errMsg', str(e))
            
            if error_code == 60011:
                logger.error(f"[企业微信] 用户不存在: {user_id}")
                return False, f"用户不存在: {user_id}"
            else:
                logger.error(f"[企业微信] 获取用户详情 API 异常: {error_code}-{error_msg}")
                return False, f"API 错误: {error_code}-{error_msg}"
                
        except Exception as e:
            logger.exception(f"[企业微信] 获取用户详情异常: {str(e)}")
            return False, f"获取用户详情异常: {str(e)}"
    
    def get_user_detail(self, code: str, home_url: str) -> Tuple[bool, Any, Optional[Dict[str, Any]]]:
        """
        通过授权码获取用户详情（OAuth2流程）
        
        Args:
            code: 授权码
            home_url: 主页URL
            
        Returns:
            (成功状态, 用户ID/错误上下文, 用户信息/错误信息)
        """
        logger.info(f"[企业微信] 开始OAuth流程, home_url={home_url}")
        
        try:
            # 步骤1: 通过免登码获取 user_ticket
            logger.debug(f"[企业微信] 步骤1: 通过免登码获取用户信息")
            result = self.http_call(
                self.CORP_API_TYPE['GET_USER_TICKET_OAUTH2'],
                {'code': code}
            )
            
            # 兼容多种字段格式
            user_id = result.get('UserId') or result.get('userid') or result.get('user_id')
            user_ticket = result.get('user_ticket') or result.get('UserTicket')
            
            if not user_id:
                logger.error(f"[企业微信] 响应中缺少 userid: {result}")
                config = get_config()
                context = {
                    'global_title': config.get('app.title', 'Self-Service'),
                    'msg': f'获取用户ID失败，请确认您已加入企业',
                    'button_click': f"window.location.href='/auth'",
                    'button_display': "重新授权"
                }
                return False, context, str(result)
            
            # 如果没有 user_ticket，说明用户未加入企业或权限不足
            if not user_ticket:
                logger.warning(f"[企业微信] 未获取到 user_ticket，用户 [{user_id}] 可能未加入企业")
                config = get_config()
                context = {
                    'global_title': config.get('app.title', 'Self-Service'),
                    'msg': f'无法获取用户详细信息，用户 [{user_id}] 可能未加入企业或权限不足',
                    'button_click': f"window.location.href='{home_url}'",
                    'button_display': "返回主页"
                }
                return False, context, user_id
            
            # 步骤2: 通过 user_ticket 获取用户详情
            logger.debug(f"[企业微信] 步骤2: 通过 user_ticket 获取用户详细信息")
            user_info = self.http_call(
                self.CORP_API_TYPE['GET_USER_INFO_OAUTH2'],
                {'user_ticket': user_ticket}
            )
            
            # 记录用户信息字段（用于调试）
            user_name = user_info.get('name') or user_info.get('Name')
            user_email = user_info.get('email') or user_info.get('biz_mail')
            logger.info(f"[企业微信] OAuth流程成功完成: user_id={user_id}, name={user_name}, email={user_email}")
            return True, user_id, user_info
            
        except ApiException as e:
            error_code = getattr(e, 'errCode', 'unknown')
            error_msg = getattr(e, 'errMsg', str(e))
            
            logger.error(f"[企业微信] OAuth流程 API 异常: {error_code}-{error_msg}")
            
            # 根据错误码提供更友好的提示
            if error_code == 40029:
                user_msg = "授权码已过期，请重新扫码授权"
            elif error_code == 40014:
                user_msg = "系统凭证失效，请稍后重试"
                self.cache.access_token.delete()  # 清除失效的 token
            elif error_code == 60011:
                user_msg = "用户不存在或未加入企业"
            else:
                user_msg = f"认证失败: {error_msg} (错误码: {error_code})"
            
            config = get_config()
            context = {
                'global_title': config.get('app.title', 'Self-Service'),
                'msg': user_msg,
                'button_click': f"window.location.href='/auth'",
                'button_display': "重新授权"
            }
            return False, context, f"{error_code}-{error_msg}"
            
        except Exception as e:
            logger.exception(f"[企业微信] OAuth流程未知异常: {str(e)}")
            config = get_config()
            context = {
                'global_title': config.get('app.title', 'Self-Service'),
                'msg': f'系统异常: {str(e)}',
                'button_click': f"window.location.href='{home_url}'",
                'button_display': "返回主页"
            }
            return False, context, str(e)
