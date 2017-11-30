from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^validate/$', views.account_validate_img,
        name='account_validate_img'),
    url(r'^orderitem/$', views.ajax_orderitem, name='ajax_orderitem'),
    url(r'^$', views.dashboard, name='dashboard'),
]
