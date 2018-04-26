from django.conf.urls import url
from .views import show_message, read_message, message_number


urlpatterns = [
    url(r'^show$', show_message),
    url(r'^show?page=(?P<page_no>)$', show_message),
    url(r'^read/(?P<msg_id>\d+)', read_message),
    url(r'^query$', message_number),

]