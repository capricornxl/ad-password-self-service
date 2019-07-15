from django.shortcuts import render, reverse, HttpResponsePermanentRedirect, redirect
from django.http import *
from django.contrib import messages
from dingtalk import *
from .models import *
from .crypto import Crypto
from .ad import ad_get_user_locked_status_by_mail, ad_unlock_user_by_mail, ad_reset_user_pwd_by_mail, \
    ad_get_user_status_by_mail, ad_ensure_user_by_mail, ad_modify_user_pwd_by_mail
from .dingding import ding_get_userinfo_detail, ding_get_userid_by_unionid, ding_get_userinfo_by_code, \
    ding_get_persistent_code, ding_get_access_token
from pwdselfservice.local_settings import *
from .form import *


class CustomPasswortValidator(object):

    def __init__(self, min_length=1, max_length=30):
        self.min_length = min_length

    def validate(self, password):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d digit.') % {'min_length': self.min_length})
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d letter.') % {'min_length': self.min_length})
        if not any(char in special_characters for char in password):
            raise ValidationError(_('Password must contain at least %(min_length)d special character.') % {'min_length': self.min_length})

    def get_help_text(self):
        return ""
