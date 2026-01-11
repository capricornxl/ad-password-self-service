# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic.base import RedirectView
from apps.password_manager.views import (
    reset_password,
    index,
    unlock_account,
    messages,
    auth,
    send_sms_code,
    verify_sms_code,
    healthz
)
from apps.password_manager.api import (
    api_change_password,
    api_reset_password,
    api_unlock_account,
    api_password_rules,
    api_auth_status
)

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url='static/img/favicon.ico')),
    # 健康检查接口（用于容器心跳检测）
    path('healthz', healthz, name='healthz'),
    path('', index, name='index'),
    path('auth', auth, name='auth'),
    path('resetPassword', reset_password, name='resetPassword'),
    path('unlockAccount', unlock_account, name='unlockAccount'),
    path('messages', messages, name='messages'),
    # SMS API端点
    path('api/sms/send', send_sms_code, name='send_sms_code'),
    path('api/sms/verify', verify_sms_code, name='send_sms_verify'),
    # 密码管理 API 端点
    path('api/password/change', api_change_password, name='api_change_password'),
    path('api/password/reset', api_reset_password, name='api_reset_password'),
    path('api/account/unlock', api_unlock_account, name='api_unlock_account'),
    path('api/config/password-rules', api_password_rules, name='api_password_rules'),
    # 认证状态检查 API 端点
    path('api/auth/status', api_auth_status, name='api_auth_status'),
]