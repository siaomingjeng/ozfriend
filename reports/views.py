from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from .reports import Report, YMD
from .forms import ReportDateForm, ReportPayerForm
# use @never_cache # useless here
from django.views.decorators.cache import never_cache
import datetime


CONTEXT = {'site_header': 'OZFriend Management System',
           'site_title': 'OZFriend', }


@staff_member_required
def report_list(req):
    context = {}
    context['site_header'] = CONTEXT['site_header']
    context['site_title'] = CONTEXT['site_title']
    context['marry_count'] = "我们结婚{0}年{1}个月零{2}天啦~~~~ \
        一共度过了{3}天快乐的时光！".format(*YMD())
    context['app_list'] = [{'name': 'Report'}]
    context['title'] = 'Reports administration'
    return render(req, "reports/report_index.html", context)


@staff_member_required
@never_cache
def annual_report(req):
    context = {}
    context['site_header'] = CONTEXT['site_header']
    context['site_title'] = CONTEXT['site_title']
    context['report_type'] = 'Annual'
    context['title'] = 'Annual Report'
    context['report_url'] = 'annual_report'
    context['has_permission'] = True
    context['site_url'] = reverse('shop:product_list')
    if req.method == 'POST':
        form = ReportDateForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            date_from = cd["date_from"]
            date_to = cd["date_to"]
            context['report'] = Report().get_this_year(date_from, date_to)
            context['report_date_form'] = form
            return render(req, "reports/report_detail.html", context)
        else:
            context['report'] = Report().get_this_year()
            context['report_date_form'] = form
            context['report_date_form'].fields['date_to'].initial = \
                datetime.datetime.now().date()
            context['report_date_form'].fields['date_from'].initial = \
                datetime.datetime.now().date() - datetime.timedelta(30)
            return render(req, "reports/report_detail.html", context)
    else:
        context['report'] = Report().get_this_year()
        context['report_date_form'] = ReportDateForm()
        context['report_date_form'].fields['date_to'].initial = \
            datetime.datetime.now().date()
        context['report_date_form'].fields['date_from'].initial = \
            datetime.datetime.now().date() - datetime.timedelta(30)
        return render(req, "reports/report_detail.html", context)


@staff_member_required
def monthly_report(req):
    context = {}
    context['site_header'] = CONTEXT['site_header']
    context['site_title'] = CONTEXT['site_title']
    context['has_permission'] = True
    context['site_url'] = reverse('shop:product_list')
    context['report_type'] = 'Monthly'
    context['report_url'] = 'monthly_report'
    context['title'] = 'Monthly Report'
    if req.method == 'POST':
        form = ReportDateForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            date_from = cd["date_from"]
            date_to = cd["date_to"]
            context['report'] = Report().get_this_month(date_from, date_to)
            context['report_date_form'] = form
            return render(req, "reports/report_detail.html", context)
        else:
            context['report'] = Report().get_this_month()
            context['report_date_form'] = form
            context['report_date_form'].fields['date_to'].initial = \
                datetime.datetime.now().date()
            context['report_date_form'].fields['date_from'].initial = \
                datetime.datetime.now().date() - datetime.timedelta(30)
            return render(req, "reports/report_detail.html", context)
    else:
        context['report'] = Report().get_this_month()
        context['report_date_form'] = ReportDateForm()
        context['report_date_form'].fields['date_to'].initial = \
            datetime.datetime.now().date()
        context['report_date_form'].fields['date_from'].initial = \
            datetime.datetime.now().date() - datetime.timedelta(30)
        return render(req, "reports/report_detail.html", context)


@staff_member_required
def payer_report(req):
    context = {}
    context['site_header'] = CONTEXT['site_header']
    context['site_title'] = CONTEXT['site_title']
    context['has_permission'] = True
    context['site_url'] = reverse('shop:product_list')
    context['report_type'] = 'Payer'
    context['report_url'] = 'payer_report'
    context['title'] = 'Payer Report'
    if req.method == 'POST':
        form = ReportPayerForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            datetime_from = cd["date_from"]
            datetime_to = cd["date_to"]
            over = cd["over"]
            context['report'] = Report().get_payers_year(datetime_from,
                                                         datetime_to, over)
            context['report_date_form'] = form
            return render(req, "reports/report_detail.html", context)
        else:
            context['report'] = Report().get_payers_year()
            context['report_date_form'] = form
            context['report_date_form'].fields['date_to'].initial = \
                datetime.datetime.now().date()
            context['report_date_form'].fields['date_from'].initial = \
                datetime.datetime.now().date() - datetime.timedelta(30)
            return render(req, "reports/report_detail.html", context)
    else:
        context['report'] = Report().get_payers_year()
        context['report_date_form'] = ReportPayerForm()
        context['report_date_form'].fields['date_to'].initial = \
            datetime.datetime.now().date()
        context['report_date_form'].fields['date_from'].initial = \
            datetime.datetime.now().date() - datetime.timedelta(30)
        return render(req, "reports/report_detail.html", context)


@staff_member_required
def capital_report(req):
    context = {}
    context['site_header'] = CONTEXT['site_header']
    context['site_title'] = CONTEXT['site_title']
    context['has_permission'] = True
    context['site_url'] = reverse('shop:product_list')
    context['report_url'] = 'capital_report'
    context['title'] = 'Capital Report'
    if req.method == 'POST':
        form = ReportDateForm(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            datetime_from = cd["date_from"]
            datetime_to = cd["date_to"]
            context['report'] = Report().get_capital_year(datetime_from,
                                                          datetime_to)
            context['report_date_form'] = form
            return render(req, "reports/report_detail.html", context)
        else:
            context['report_date_form'] = form
            context['report'] = Report().get_capital_year()
            context['report_date_form'].fields['date_to'].initial = \
                datetime.datetime.now().date()
            context['report_date_form'].fields['date_from'].initial = \
                datetime.datetime.now().date() - datetime.timedelta(30)
            return render(req, "reports/report_detail.html", context)
    else:
        context['report'] = Report().get_capital_year()
        context['report_date_form'] = ReportDateForm()
        context['report_date_form'].fields['date_to'].initial = \
            datetime.datetime.now().date()
        context['report_date_form'].fields['date_from'].initial = \
            datetime.datetime.now().date() - datetime.timedelta(30)
        return render(req, "reports/report_detail.html", context)
