from django.urls import path
from django.views.generic.base import RedirectView
import resetpwd.views

urlpatterns = {
    path("favicon.ico", RedirectView.as_view(url='static/img/favicon.ico')),
    path('', resetpwd.views.index, name='index'),
    path('auth', resetpwd.views.auth, name='auth'),
    path('resetPassword', resetpwd.views.reset_password, name='resetPassword'),
    path('unlockAccount', resetpwd.views.unlock_account, name='unlockAccount'),
    path('messages', resetpwd.views.messages, name='messages'),
}
