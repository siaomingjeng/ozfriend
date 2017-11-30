from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.report_list, name='report_list'),
    url(r'^annual$', views.annual_report, name='annual_report'),
    url(r'^monthly$', views.monthly_report, name='monthly_report'),
    url(r'^payer$', views.payer_report, name='payer_report'),
    url(r'^capital$', views.capital_report, name='capital_report'),
]
