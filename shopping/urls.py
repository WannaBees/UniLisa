from django.conf.urls import url

from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import login
from django.views.generic import RedirectView

from UniLisa_Shop import settings
from . import views

urlpatterns = [
    # /shop/
    url(r'^$', views.index, name='index'),

   # url(r'^(?P<item_id>[0-9]+)/addToCart$', RedirectView.as_view(url='/shop/(item_id)', permanent=False), name='detail'),

    url(r'^(?P<item_id>[0-9]+)/addToCart$', views.detail, name='detail'),

    # /shop/71/
    url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),


    #url(r'^(?P<item_id>[0-9]+)/?action=addtocart', RedirectView.as_view(url='/shop', permanent=False), name='index'),


    # /cart/
    url(r'^cart/$', views.cart, name='cart'),


    # /login/
    url(r'^login/$', views.login, name='login'),

    # /register
    url(r'^register/$', views.register, name='register'),

    # /order
    url(r'^order/$', views.order, name='order'),

    # /orderconfirmation
    url(r'^orderconfirmation/$', views.orderconfirmation, name='orderconfirmation'),

   # url(r'^signup/$', views.signup, name='signup')

]



