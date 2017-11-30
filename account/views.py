from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from orders.validate import get_validate_img, validated
from orders.models import Order, OrderItem
import json


@login_required
def ajax_orderitem(req):
    '''Decode xmean of reports/templatetags/ozfriend_tags.py'''
    def xdecode(val):
        return int(val[:-1])
    if req.is_ajax():
        if req.method == 'POST':
            orderid = xdecode(req.POST['orderid'])
            orderpayer = req.user.first_name
            order = get_object_or_404(Order, id=orderid, payer=orderpayer)
            resp = []
            if order:
                for o in OrderItem.objects.filter(order=order):
                    if o.product.id not in [1, 2]:
                        resp.append(o.product.chinese+' X '+str(o.quantity))
            return HttpResponse(json.dumps(resp),
                                content_type='application/json')


@login_required
def dashboard(req):
    order_list = Order.objects.filter(payer=req.user.first_name)
    return render(req, 'account/dashboard.html',
                  {'sessioin': 'dashboard', 'order_list': order_list})


def account_validate_img(req):
    image = get_validate_img(req)
    res = HttpResponse(content_type='image/png')
    image.save(res, 'png')
    return res


def user_login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if not validated(req):
            form.errors['reason'] = 'Invalid validation'
            return render(req, 'account/login.html', {'form': form})
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(req, user)
                    return redirect('account:dashboard')
                else:
                    form.errors['reason'] = 'Inactive account!'
                    return render(req, 'account/login.html', {'form': form})
            else:
                form.errors['reason'] = 'Invalid username or password!'
                return render(req, 'account/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(req, 'account/login.html', {'form': form})


@login_required
def user_logout(req):
    logout(req)
    return render(req, 'account/logout.html')
