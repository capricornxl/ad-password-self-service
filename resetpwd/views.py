from django.shortcuts import render
from django.http import *
from resetpwd.utils.crypto import Crypto
from resetpwd.utils.ad import ad_get_user_locked_status_by_mail, ad_unlock_user_by_mail, ad_reset_user_pwd_by_mail, \
    ad_get_user_status_by_mail, ad_ensure_user_by_mail, ad_modify_user_pwd_by_mail
from resetpwd.utils.dingding import ding_get_userinfo_detail, ding_get_userid_by_unionid, \
    ding_get_persistent_code, ding_get_access_token
from pwdselfservice.local_settings import *
from .form import CheckForm
import logging

msg_template = 'msg.html'
logger = logging.getLogger('django')


def resetpwd_index(request):
    """
    用户修改密码
    :param request:
    :return:
    """
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    app_id = DING_SELF_APP_ID
    if request.method == 'GET':
        return render(request, 'index.html', locals())
    else:
        logger.error('[异常]  请求方法：%s，请求路径：%s' % (request.method, request.path))

    if request.method == 'POST':
        # 对前端提交的数据进行二次验证，防止恶意提交简单密码或串改账号。
        check_form = CheckForm(request.POST)
        if check_form.is_valid():
            form_obj = check_form.cleaned_data
            user_email = form_obj.get("user_email")
            old_password = form_obj.get("old_password")
            new_password = form_obj.get("new_password")
        else:
            msg = check_form.as_p().errors
            logger.error('[异常]  请求方法：%s，请求路径：%s，错误信息：%s' % (request.method, request.path, msg))
            context = {
                'msg': msg,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

        if user_email and old_password and new_password:
            try:
                # 判断账号是否被锁定
                if ad_get_user_locked_status_by_mail(user_mail_addr=user_email) is not 0:
                    context = {
                        'msg': "此账号己被锁定，请先解锁账号。",
                        'button_click': "window.history.back()",
                        'button_display': "返回"
                    }
                    return render(request, msg_template, context)

                # 514 66050是AD中账号被禁用的特定代码，这个可以在微软官网查到。
                if ad_get_user_status_by_mail(user_mail_addr=user_email) == 514 or ad_get_user_status_by_mail(
                        user_mail_addr=user_email) == 66050:
                    context = {
                        'msg': "此账号状态为己禁用，请联系HR确认账号是否正确。",
                        'button_click': "window.location.href='%s'" % home_url,
                        'button_display': "返回主页"
                    }
                    return render(request, msg_template, context)

                try:
                    result = ad_modify_user_pwd_by_mail(user_mail_addr=user_email, old_password=old_password,
                                                        new_password=new_password)
                    if result:
                        context = {
                            'msg': "密码己修改成功，请妥善保管密码。你可直接关闭此页面！",
                            'button_click': "window.location.href='%s'" % home_url,
                            'button_display': "返回主页"
                        }
                        return render(request, msg_template, context)

                    else:
                        context = {
                            'msg': "密码未修改成功，请确认旧密码是否正确。",
                            'button_click': "window.history.back()",
                            'button_display': "返回"
                        }
                        return render(request, msg_template, context)

                except IndexError:
                    context = {
                        'msg': "请确认邮箱账号[%s]是否正确？未能在Active Directory中检索到相关信息。" % user_email,
                        'button_click': "window.location.href='%s'" % home_url,
                        'button_display': "返回主页"
                    }
                    return render(request, msg_template, context)

                except Exception as e:
                    context = {
                        'msg': "出现未预期的错误[%s]，请与管理员联系~" % str(e),
                        'button_click': "window.location.href='%s'" % home_url,
                        'button_display': "返回主页"
                    }
                    return render(request, msg_template, context)

            except IndexError:
                context = {
                    'msg': "请确认邮箱账号[%s]是否正确？未能在Active Directory中检索到相关信息。" % user_email,
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)

            except Exception as e:
                context = {
                    'msg': "出现未预期的错误[%s]，请与管理员联系~" % str(e),
                    'button_click': "window.history.back()",
                    'button_display': "返回"
                }
                return render(request, msg_template, context)

        else:
            context = {
                'msg': "用户名、旧密码、新密码参数不正确，请重新确认后输入。",
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


def resetpwd_check_userinfo(request):
    """
    钉钉扫码回调数据对用户在AD中进行验证
    扫码之后从钉钉中取出用户的unionid
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
        unionid = ding_get_persistent_code(code, ding_get_access_token())
        # 判断 unionid 在本企业钉钉中是否存在
        if not unionid:
            logger.error('[异常]  请求方法：%s，请求路径：%s，未能拿到unionid。' % (request.method, request.path))
            context = {
                'msg': '未能在钉钉企业通讯录中检索到相关信息，请确认当前登录钉钉的账号已在企业中注册！',
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

        ding_user_info = ding_get_userinfo_detail(ding_get_userid_by_unionid(unionid))
        try:
            # 钉钉中此账号是否可用
            if ding_user_info['active']:
                crypto = Crypto(CRYPTO_KEY)
                # 对unionid进行加密，因为unionid基本上固定不变的，为了防止unionid泄露而导致重复使用，进行加密后再传回。
                unionid_cryto = crypto.encrypt(unionid)
                # 配置cookie，通过cookie把加密后的用户unionid传到重置密码页面，并重定向到重置密码页面。
                set_cookie = HttpResponseRedirect('resetpwd')
                set_cookie.set_cookie('tmpid', unionid_cryto, expires=TMPID_COOKIE_AGE)
                return set_cookie
            else:
                context = {
                    'msg': '邮箱是[%s]的用户在钉钉中未激活或可能己离职' % ding_user_info['email'],
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
        except IndexError:
            context = {
                'msg': "用户不存在或己离职",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        except Exception as e:
            logger.error('[异常] ：%s' % str(e))

    except KeyError:
        context = {
            'msg': "错误，钉钉临时Code己失效，请从主页重新扫码。",
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        logger.error('[异常] ：%s' % str(KeyError))
        return render(request, msg_template, context)

    except Exception as e:
        context = {
            'msg': "错误[%s]，请与管理员联系." % str(e),
            'button_click': "window.location.href='%s'" % home_url,
            'button_display': "返回主页"
        }
        logger.error('[异常] ：%s' % str(e))
        return render(request, msg_template, context)


def resetpwd_reset(request):
    """
    钉钉扫码并验证信息之后，在重置密码页面将用户邮箱进行绑定
    :param request:
    :return:
    """
    global unionid_crypto
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    # 从cookie中提取unionid，并解密，然后对当前unionid的用户进行重置密码
    if request.method == 'GET':
        try:
            unionid_crypto = request.COOKIES.get('tmpid')
        except Exception as e:
            logger.error('[异常] ：%s' % str(e))
        if not unionid_crypto:
            logger.error('[异常]  请求方法：%s，请求路径：%s，未能拿到CODE或CODE己超时。' % (request.method, request.path))
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        # 解密
        crypto = Crypto(CRYPTO_KEY)
        unionid = crypto.decrypt(unionid_crypto)
        # 通过unionid在钉钉中拿到用户的邮箱
        user_email = ding_get_userinfo_detail(ding_get_userid_by_unionid(unionid))['email']
        # 如果邮箱在钉钉中能提取，则提交到前端绑定
        if user_email:
            context = {
                'user_email': user_email,
            }
            return render(request, 'resetpwd.html', context)
        # 否则就是钉钉中此用户未配置邮箱，返回相关提示
        else:
            context = {
                'msg': "%s 您好，企业钉钉中未能找到您账号的邮箱配置，请联系HR完善信息。" % ding_get_userinfo_detail(ding_get_userid_by_unionid(
                    unionid))['name'],
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

    # 重置密码页面，输入新密码后点击提交
    elif request.method == 'POST':
        new_password = request.POST.get('new_password').strip()
        unionid_crypto = request.COOKIES.get('tmpid')
        # 对cookie中的unionid进行超时验证，如果页面超时就不再做处理。
        if not unionid_crypto:
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        crypto = Crypto(CRYPTO_KEY)
        unionid = crypto.decrypt(unionid_crypto)
        user_email = ding_get_userinfo_detail(ding_get_userid_by_unionid(unionid))['email']
        if ad_ensure_user_by_mail(user_mail_addr=user_email) is False:
            context = {
                'msg': "账号[%s]在AD中不存在，请确认当前钉钉扫码账号绑定的邮箱是否和您正在使用的邮箱一致？或者该邮箱账号己被禁用！\n猜测：您的邮箱是否是带有数字或其它字母区分？" % user_email,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        if ad_get_user_status_by_mail(user_mail_addr=user_email) == 514 or ad_get_user_status_by_mail(
                user_mail_addr=user_email) == 66050:
            context = {
                'msg': "此账号状态为己禁用，请联系HR确认账号是否正确。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)

        try:
            result = ad_reset_user_pwd_by_mail(user_mail_addr=user_email, new_password=new_password)
            if result:
                # 重置密码并执行一次解锁，防止重置后账号还是锁定状态。
                ad_unlock_user_by_mail(user_email)
                context = {
                    'msg': "密码己重置成功，请妥善保管。你可以点击返回主页或直接关闭此页面！",
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
            else:
                context = {
                    'msg': "密码未重置成功，确认密码是否满足AD的复杂性要求。",
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
        except IndexError:
            context = {
                'msg': "请确认邮箱账号[%s]是否正确？未能在AD中检索到相关信息。" % user_email,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        except Exception as e:
            context = {
                'msg': "出现未预期的错误[%s]，请与管理员联系~" % str(e),
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


def resetpwd_unlock(request):
    """
    解锁账号
    :param request:
    :return:
    """
    home_url = '%s://%s' % (request.scheme, HOME_URL)
    if request.method == 'GET':
        unionid_crypto = request.COOKIES.get('tmpid')
        if not unionid_crypto:
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        crypto = Crypto(CRYPTO_KEY)
        unionid = crypto.decrypt(unionid_crypto)
        user_email = ding_get_userinfo_detail(ding_get_userid_by_unionid(unionid))['email']
        context = {
            'user_email': user_email,
        }
        return render(request, 'resetpwd.html', context)

    elif request.method == 'POST':
        unionid_crypto = request.COOKIES.get('tmpid')
        if not unionid_crypto:
            context = {
                'msg': "会话己超时，请重新扫码验证用户信息。",
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        crypto = Crypto(CRYPTO_KEY)
        unionid = crypto.decrypt(unionid_crypto)
        user_email = ding_get_userinfo_detail(ding_get_userid_by_unionid(unionid))['email']
        if ad_ensure_user_by_mail(user_mail_addr=user_email) is False:
            context = {
                'msg': "账号[%s]在AD中未能正确检索到，请确认当前钉钉扫码账号绑定的邮箱是否和您正在使用的邮箱一致？或者该邮箱账号己被禁用！\n猜测：您的邮箱是否是带有数字或其它字母区分？" %
                       user_email,
                'button_click': "window.location.href='%s'" % home_url,
                'button_display': "返回主页"
            }
            return render(request, msg_template, context)
        else:
            try:
                result = ad_unlock_user_by_mail(user_email)
                if result:
                    context = {
                        'msg': "账号己解锁成功。你可以点击返回主页或直接关闭此页面！",
                        'button_click': "window.location.href='%s'" % home_url,
                        'button_display': "返回主页"
                    }
                    return render(request, msg_template, context)
                else:
                    context = {
                        'msg': "账号未能解锁，请联系管理员确认该账号在AD的是否己禁用。",
                        'button_click': "window.location.href='%s'" % home_url,
                        'button_display': "返回主页"
                    }
                    return render(request, msg_template, context)
            except IndexError:
                context = {
                    'msg': "请确认邮箱账号[%s]是否正确？未能在AD中检索到相关信息。" % user_email,
                    'button_click': "window.location.href='%s'" % home_url,
                    'button_display': "返回主页"
                }
                return render(request, msg_template, context)
            except Exception as e:
                context = {
                    'msg': "出现未预期的错误[%s]，请与管理员联系~" % str(e),
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


def reset_msg(request):
    msg = request.GET.get('msg')
    button_click = request.GET.get('button_click')
    button_display = request.GET.get('button_display')
    context = {
        'msg': msg,
        'button_click': button_click,
        'button_display': button_display
    }
    return render(request, msg_template, context)
