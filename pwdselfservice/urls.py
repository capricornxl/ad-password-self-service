from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf import urls
import resetpwd.views
from django.conf.urls.static import static

urlpatterns = {
    # path('admin/', admin.site.urls)
    path("favicon.ico", RedirectView.as_view(url='static/img/favicon.ico')),
    path('', resetpwd.views.resetpwd_index, name='index'),
    path('resetcheck', resetpwd.views.resetpwd_check_userinfo, name='resetcheck'),
    path('resetpwd', resetpwd.views.resetpwd_reset, name='resetpwd'),
    path('resetunlock', resetpwd.views.resetpwd_unlock, name='resetunlock'),
    path('resetmsg', resetpwd.views.reset_msg, name='resetmsg'),
}
