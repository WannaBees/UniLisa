from django.conf.urls import url


from . import views

urlpatterns = [
    # /shop/
    url(r'^$', views.index, name='index'),


    url(r'^(?P<item_id>[0-9]+)/addToCart$', views.detail, name='detail'),

    # /shop/71/
    url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),

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

]



