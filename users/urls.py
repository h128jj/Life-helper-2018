from django.conf.urls import url
from .views import register, login, logout, user_info, activate, activate_again, login_expire


urlpatterns = [
    url(r'^register$', register),
    url(r'^login', login),
    url(r'^logout', logout),
    url(r'^user_info', user_info),
    url(r'^activate', activate),
    url(r'^again', activate_again),
    url(r'^check', login_expire),
]
