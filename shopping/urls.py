from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import login

from UniLisa_Shop import settings
from . import views

urlpatterns = [
    # /shop/
    url(r'^$', views.index, name='index'),

    # /shop/71/
    url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),

    # /account/ for the account creation/login
    url(r'^login/$', views.login, name='login')
]
