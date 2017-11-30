from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'create/$', views.order_create, name='order_create'),
    url(r'^inner/$', views.order_inner, name='order_inner'),
    url(r'^validate/$', views.order_validate_img, name='order_validate_img'),
]
