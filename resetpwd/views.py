import json
import logging
import os
from django.shortcuts import render
from utils.ad_ops import AdOps
from ldap3.core.exceptions import LDAPException
from utils.format_username import format2username, get_user_is_active
from .form import CheckForm
from .utils import code_2_user_info, crypto_id_2_user_info, ops_account, crypto_id_2_user_id, crypto_user_id_2_cookie
from django.conf import settings
APP_ENV = os.getenv('APP_ENV')
if APP_ENV == 'dev':
    from conf.local_settings_dev import SCAN_CODE_TYPE, DING_MO_APP_ID, WEWORK_CORP_ID, WEWORK_AGENT_ID, HOME_URL, DING_CORP_ID
else:
    from conf.local_settings import SCAN_CODE_TYPE, DING_MO_APP_ID, WEWORK_CORP_ID, WEWORK_AGENT_ID, HOME_URL, DING_CORP_ID

msg_template = 'messages.v1.html'
logger = logging.getLogger('django')


class PARAMS(object):
    if SCAN_CODE_TYPE == 'DING':
        corp_id = DING_CORP_ID
        app_id = DING_MO_APP_ID
        agent_id = None
        SCAN_APP = '钉钉'
        from utils.dingding_ops import DingDingOps
        ops = DingDingOps()
    elif SCAN_CODE_TYPE == 'WEWORK':
        corp_id = None
        app_id = WEWORK_CORP_ID
        agent_id = WEWORK_AGENT_ID
        SCAN_APP = '微信'
        from utils.wework_ops import WeWorkOps
        ops = WeWorkOps()
    else:
        corp_id = None
        app_id = WEWORK_CORP_ID
        agent_id = WEWORK_AGENT_ID
        SCAN_APP = '微信'
        from utils.wework_ops import WeWorkOps
        ops = WeWorkOps()


scan_params = PARAMS()
_ops = scan_params.ops


def index(request):
    """
    用户自行修改密码/首页
    :param request:
    :return:
    """
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    corp_id = scan_params.corp_id
    app_id = scan_params.app_id
    agent_id = scan_params.agent_id
    scan_app = scan_params.SCAN_APP
    unsecpwd = settings.UN_SEC_PASSWORD
    if request.method == 'GET' and SCAN_CODE_TYPE == 'DING':
        return render(request, 'ding_index.html', locals())
    elif request.method == 'GET' and SCAN_CODE_TYPE == 'WEWORK':
        return render(request, 'we_index.v1.html', locals())
    elif request.method == 'GET' and SCAN_CODE_TYPE == 'FEISHU':
        return render(request, 'index.v1.html', locals())
    else:
        logger.error('[异常]  请求方法：%s，请求路径%s' % (request.method, request.path))
    #
    # if request.method == 'GET':
    #     return render(request, 'index.v1.html', locals())

    if request.method == 'POST':
        # 对前端提交的数据进行二次验证，防止恶意提交简单密码或篡改账号。
        check_form = CheckForm(request.POST)
        if check_form.is_valid():
            form_obj = check_form.cleaned_data
            username = form_obj.get("username")
            old_password = form_obj.get("old_password")
            new_password = form_obj.get("new_password")
        else:
            _msg = check_form.as_p().errors
            logger.error('[异常]  请求方法：%s，请求路径：%s，错误信息：%s' % (request.method, request.path, _msg))
            context = {
                'msg': _msg,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        # 格式化用户名
        _, username = format2username(username)
        if _ is False:
            context = {
                'msg': username,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        # 检测账号状态
        auth_status, auth_result = AdOps().ad_auth_user(username=username, password=old_password)
        if not auth_status:
            context = {
                'msg': str(auth_result),
                'button_click': "window.history.back()",
                'button_display': "返回"
            }
            return render(request, msg_template, context)
        return ops_account(AdOps(), request, msg_template, home_url, username, new_password)
    else:
        context = {
            'msg': "请从主页进行修改密码操作或扫码验证用户信息。",
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        return render(request, msg_template, context)


def callback_check(request):
    """
    钉钉扫码回调数据之后，将用户账号在AD中进行验证，如果通过，则返回钉钉中取出用户的union_id
    :param request:
    :return:
    """
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    code = request.GET.get('code')
    if code:
        logger.info('[成功]  请求方法：%s，请求路径：%s，CODE：%s' % (request.method, request.path, code))
    else:
        logger.error('[异常]  请求方法：%s，请求路径：%s，未能拿到CODE。' % (request.method, request.path))
        context = {
            'msg': "错误，临时授权码己失效，请从主页重新扫码验证。",
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        return render(request, msg_template, context)
    try:
        _status, user_id, user_info = code_2_user_info(_ops, request, msg_template, home_url, code)
        print(user_info)
        if not _status:
            return render(request, msg_template, user_id)
        # 账号是否是激活的
        if get_user_is_active(user_info):
            return crypto_user_id_2_cookie(user_id)
        # 否则账号不存在或未激活
        else:
            context = {
                'msg': '当前扫码的用户在钉钉中未激活或可能己离职，用户信息如下：%s' % user_info,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
    except Exception as callback_e:
        context = {
            'msg': "错误[%s]，请与管理员联系." % str(callback_e),
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        logger.error('[异常] ：%s' % str(callback_e))
        return render(request, msg_template, context)


def reset_pwd_by_callback(request):
    """
    钉钉扫码并验证信息通过之后，在重置密码页面将用户账号进行绑定
    :param request:
    :return:
    """
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    # 从cookie中提取union_id，并解密，然后对当前union_id的用户进行重置密码
    if request.method == 'GET':
        _status, user_info = crypto_id_2_user_info(_ops, request, msg_template, home_url, scan_params.SCAN_APP)
        if not _status:
            return render(request, msg_template, user_info)
        # 通过user_id拿到用户信息，并格式化为username
        # 格式化用户名
        _, username = format2username(user_info.get('email'))
        if _ is False:
            context = {
                'msg': username,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        # 如果邮箱能提取到，则格式化之后，提取出账号提交到前端绑定
        if username:
            context = {
                'username': username,
            }
            return render(request, 'resetPassword.v1.html', context)
        else:
            context = {
                'msg': "{}，您好，企业{}中未能找到您账号的邮箱配置，请联系HR完善信息。".format(user_info.get('name'), scan_params.SCAN_APP),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

    # 重置密码页面，输入新密码后点击提交
    elif request.method == 'POST':
        try:
            _new_password = request.POST.get('new_password').strip()
            _status, user_info = crypto_id_2_user_info(_ops, request, msg_template, home_url, scan_params.SCAN_APP)
            if not _status:
                return render(request, msg_template, user_info)
            # 格式化用户名
            _, username = format2username(user_info.get('email'))
            if _ is False:
                context = {
                    'msg': username,
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
            return ops_account(ad_ops=AdOps(), request=request, msg_template=msg_template, home_url=home_url, username=username, new_password=_new_password)
        except Exception as reset_e:
            context = {
                'msg': "错误[%s]，请与管理员联系." % str(reset_e),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            logger.error('[异常] ：%s' % str(reset_e))
            return render(request, msg_template, context)
    else:
        context = {
            'msg': "请从主页开始进行操作。",
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        return render(request, msg_template, context)


def unlock_account(request):
    """
    解锁账号
    :param request:
    :return:
    """
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    if request.method == 'GET':
        _status, user_info = crypto_id_2_user_info(_ops, request, msg_template, home_url, scan_params.SCAN_APP)
        if not _status:
            return render(request, msg_template, user_info)
        # 格式化用户名
        _, username = format2username(user_info.get('email'))
        if _ is False:
            context = {
                'msg': username,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        context = {
            'username': username,
        }
        return render(request, 'resetPassword.v1.html', context)

    elif request.method == 'POST':
        _status, user_info = crypto_id_2_user_info(_ops, request, msg_template, home_url, scan_params.SCAN_APP)
        if not _status:
            return render(request, msg_template, user_info)
        # 格式化用户名
        _, username = format2username(user_info.get('email'))
        if _ is False:
            context = {
                'msg': username,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        return ops_account(AdOps(), request, msg_template, home_url, username, None)
    else:
        context = {
            'msg': "请从主页开始进行操作。",
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        return render(request, msg_template, context)


def messages(request):
    _msg = request.GET.get('msg')
    button_click = request.GET.get('button_click')
    button_display = request.GET.get('button_display')
    context = {
        'msg': _msg,
        'button_click': button_click,
        'button_display': button_display
    }
    return render(request, msg_template, context)
