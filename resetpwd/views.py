import logging

from django.http import *
from django.shortcuts import render
from pwdselfservice.local_settings import SCAN_CODE_TYPE, DING_MO_APP_ID, WEWORK_CORP_ID, WEWORK_AGENT_ID, HOME_URL, CRYPTO_KEY, TMPID_COOKIE_AGE

from utils.ad_ops import AdOps
from utils.crypto import Crypto
from utils.format_username import format2username, get_user_is_active
from .form import CheckForm

msg_template = 'messages.html'
logger = logging.getLogger('django')


class PARAMS(object):
    if SCAN_CODE_TYPE == 'DING':
        app_id = DING_MO_APP_ID
        agent_id = None
        SCAN_APP = '钉钉'
        from utils.dingding_ops import DingDingOps
        ops = DingDingOps()
    elif SCAN_CODE_TYPE == 'WEWORK':
        app_id = WEWORK_CORP_ID
        agent_id = WEWORK_AGENT_ID
        SCAN_APP = '微信'
        from utils.wework_ops import WeWorkOps
        ops = WeWorkOps()


scan_params = PARAMS()
_ops = scan_params.ops
ad_ops = AdOps()


def index(request):
    """
    用户自行修改密码/首页
    :param request:
    :return:
    """
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    app_id = scan_params.app_id
    agent_id = scan_params.agent_id
    if request.method == 'GET' and SCAN_CODE_TYPE == 'DING':
        return render(request, 'ding_index.html', locals())
    elif request.method == 'GET' and SCAN_CODE_TYPE == 'WEWORK':
        return render(request, 'we_index.html', locals())
    else:
        logger.error('[异常]  请求方法：%s，请求路径：%s' % (request.method, request.path))

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
        username = format2username(username)
        # 检测账号状态
        auth_status, auth_result = ad_ops.ad_auth_user(username=username, password=old_password)
        if not auth_status:
            context = {
                'msg': str(auth_result),
                'button_click': "window.history.back()",
                'button_display': "返回"
            }
            return render(request, msg_template, context)

        # 514 66050是AD中账号被禁用的特定代码，这个可以在微软官网查到。
        # 可能不是太准确，如果使用者能确定还有其它状态码，可以自行在此处添加
        account_code = ad_ops.ad_get_user_status_by_account(username)
        if account_code == 514 or account_code == 66050:
            context = {
                'msg': "此账号状态为己禁用，请联系HR确认账号是否正确。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

        reset_status, reset_result = ad_ops.ad_reset_user_pwd_by_account(username=username, new_password=new_password)
        if reset_status:
            context = {
                'msg': "密码己修改成功，新密码稍后生效，请妥善保管。您可直接关闭此页面！",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        else:
            context = {
                'msg': "密码未修改成功，原因：{}".format(reset_result),
                'button_click': "window.history.back()",
                'button_display': "返回"
            }
            return render(request, msg_template, context)
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

    try:
        _status, user_id = _ops.get_user_id_by_code(code)
        # 判断 user_id 在本企业钉钉/微信中是否存在
        if not _status:
            context = {
                'msg': '获取钉钉userid失败，错误信息：{}'.format(user_id),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        detail_status, user_info = _ops.get_user_detail_by_user_id(user_id)
        if not detail_status:
            context = {
                'msg': '获取钉钉用户信息失败，错误信息：{}'.format(user_info),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        # 账号是否是激活的
        if get_user_is_active(user_info):
            crypto = Crypto(CRYPTO_KEY)
            # 对user_id进行加密，因为user_id基本上固定不变的，为了防止user_id泄露而导致重复使用，进行加密后再传回。
            _id_cryto = crypto.encrypt(user_id)
            # 配置cookie，通过cookie把加密后的用户user_id传到重置密码页面，并重定向到重置密码页面。
            set_cookie = HttpResponseRedirect('resetPassword')
            set_cookie.set_cookie('tmpid', _id_cryto, expires=TMPID_COOKIE_AGE)
            return set_cookie
        else:
            context = {
                'msg': '[%s]在钉钉中未激活或可能己离职' % format2username(user_info.get('name')),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
    except KeyError:
        context = {
            'msg': "错误，临时授权码己失效，请从主页重新扫码验证。",
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        logger.error('[异常] ：%s' % str(KeyError))
        return render(request, msg_template, context)

    except Exception as callback_e:
        context = {
            'msg': "错误[%s]，请与管理员联系." % str(callback_e),
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        logger.error('[异常] ：%s' % str(callback_e))
        return render(request, msg_template, context)


def reset_pwd_by_ding_callback(request):
    """
    钉钉扫码并验证信息通过之后，在重置密码页面将用户账号进行绑定
    :param request:
    :return:
    """
    global tmpid_crypto
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    # 从cookie中提取union_id，并解密，然后对当前union_id的用户进行重置密码
    if request.method == 'GET':
        try:
            tmpid_crypto = request.COOKIES.get('tmpid')
        except Exception as e:
            tmpid_crypto = None
            logger.error('[异常] ：%s' % str(e))
        if not tmpid_crypto:
            logger.error('[异常]  请求方法：%s，请求路径：%s，未能拿到TmpID或会话己超时。' % (request.method, request.path))
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        # 解密
        crypto = Crypto(CRYPTO_KEY)
        user_id = crypto.decrypt(tmpid_crypto)
        # 通过user_id拿到用户的邮箱，并格式化为username
        userid_status, user_result = _ops.get_user_detail_by_user_id(user_id)
        if not userid_status:
            context = {
                'msg': '获取{}用户信息失败，错误信息：{}'.format(user_result, scan_params.SCAN_APP),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        username = format2username(user_result['email'])
        # 如果邮箱能提取到，则格式化之后，提取出账号提交到前端绑定
        if username:
            context = {
                'username': username,
            }
            return render(request, 'resetPassword.html', context)
        # 否则就是用户未配置邮箱，返回相关提示
        else:
            context = {
                'msg': "{}，您好，企业{}中未能找到您账号的邮箱配置，请联系HR完善信息。" .format(user_result.get('name'), scan_params.SCAN_APP),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

    # 重置密码页面，输入新密码后点击提交
    elif request.method == 'POST':
        _new_password = request.POST.get('new_password').strip()
        try:
            tmpid_crypto = request.COOKIES.get('tmpid')
        except Exception as e:
            tmpid_crypto = None
            logger.error('[异常] ：%s' % str(e))
        if not tmpid_crypto:
            logger.error('[异常]  请求方法：%s，请求路径：%s，未能拿到CODE或CODE己超时。' % (request.method, request.path))
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        crypto = Crypto(CRYPTO_KEY)
        user_id = crypto.decrypt(tmpid_crypto)
        userid_status, user_result = _ops.get_user_detail_by_user_id(user_id)
        if not userid_status:
            context = {
                'msg': '获取企业{}用户信息失败，错误信息：{}'.format(scan_params.SCAN_APP, user_result),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        username = format2username(user_result['email'])
        if ad_ops.ad_ensure_user_by_account(username) is False:
            context = {
                'msg': "账号[%s]在AD中不存在，请确认当前钉钉扫码账号绑定的邮箱是否和您正在使用的邮箱一致？或者该账号己被禁用！\n猜测：您的账号或邮箱是否是带有数字或其它字母区分？" % username,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

        # 514 66050是AD中账号被禁用的特定代码，这个可以在微软官网查到。
        # 可能不是太准确，如果使用者能确定还有其它状态码，可以自行在此处添加
        account_code = ad_ops.ad_get_user_status_by_account(username)
        if account_code == 514 or account_code == 66050:
            context = {
                'msg': "此账号状态为己禁用，请联系HR确认账号是否正确。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

        reset_status, result = ad_ops.ad_reset_user_pwd_by_account(username=username, new_password=_new_password)
        if reset_status:
            # 重置密码并执行一次解锁，防止重置后账号还是锁定状态。
            unlock_status, result = ad_ops.ad_unlock_user_by_account(username)
            if unlock_status:
                context = {
                    'msg': "密码己重置成功，请妥善保管。你可以点击返回主页或直接关闭此页面！",
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
        else:
            context = {
                'msg': "密码未重置成功，错误信息：{}".format(result),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
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
        _union_id_crypto = request.COOKIES.get('tmpid')
        if not _union_id_crypto:
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        crypto = Crypto(CRYPTO_KEY)
        user_id = crypto.decrypt(_union_id_crypto)
        userid_status, user_info = _ops.get_user_detail_by_user_id(user_id)
        if not userid_status:
            context = {
                'msg': '获取{}用户信息失败，错误信息：{}'.format(scan_params.SCAN_APP, user_info),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        username = format2username(user_info['email'])
        context = {
            'username': username,
        }
        return render(request, 'resetPassword.html', context)

    elif request.method == 'POST':
        _union_id_crypto = request.COOKIES.get('tmpid')
        if not _union_id_crypto:
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        crypto = Crypto(CRYPTO_KEY)
        user_id = crypto.decrypt(_union_id_crypto)
        userid_status, user_info = _ops.get_user_detail_by_user_id(user_id)
        if not userid_status:
            context = {
                'msg': '获取{}用户信息失败，错误信息：{}'.format(scan_params.SCAN_APP, user_info),
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        username = format2username(user_info['email'])
        if ad_ops.ad_ensure_user_by_account(username=username) is False:
            context = {
                'msg': "账号[%s]在AD中未能正确检索到，请确认当前钉钉扫码账号绑定的邮箱是否和您正在使用的邮箱一致？或者该账号己被禁用！\n猜测：您的账号或邮箱是否是带有数字或其它字母区分？" %
                       username,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        else:
            unlock_status, result = ad_ops.ad_unlock_user_by_account(username)
            if unlock_status:
                context = {
                    'msg': "账号己解锁成功。你可以点击返回主页或直接关闭此页面！",
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
            else:
                context = {
                    'msg': "账号未能解锁，错误信息：{}".format(result),
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
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
