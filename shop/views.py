from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import HttpResponse
import json
from .forms import QuickSearch


@staff_member_required
def product_inner(req, search_text=""):
    if req.is_ajax():
        if req.method == 'GET':
            q = req.GET['q']
            if q:
                recs = Product.objects.filter(chinese__contains=q)[:10]
                rejson = []
                for rec in recs:
                    rejson.append(rec.chinese)
                return HttpResponse(json.dumps(rejson),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps([]),
                                    content_type='application/json')
        elif req.method == 'POST':
            search_text = req.POST['search_text']
            product = get_object_or_404(Product, chinese=search_text)
            resp = {'id': product.id, 'expense_aud': str(product.expense_aud),
                    'expense_rmb': str(product.expense_rmb),
                    'price_rmb': str(product.price_rmb),
                    'price_aud': str(product.price_aud)}
            return HttpResponse(json.dumps(resp),
                                content_type='application/json')


def product_list(req, category_slug=None, search_text=""):
    if req.is_ajax():
        q = req.GET['q']
        if q:
            recs = Product.objects.filter(chinese__contains=q)[:10]
            rejson = []
            for rec in recs:
                rejson.append(rec.chinese)
            return HttpResponse(json.dumps(rejson),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps([]),
                                content_type='application/json')

    if req.method == 'POST':
        form = QuickSearch(req.POST)
        if form.is_valid():
            cd = form.cleaned_data
            search_text = cd["chinese"]

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True,
                                      chinese__contains=search_text)

    cart_product_form = CartAddProductForm()
    quick_search_form = QuickSearch()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    LIMIT = 32  # Number of items showing on each page!
    page = req.GET.get('page')   # Get the page number!
    paginator = Paginator(products, LIMIT)
    try:
        pageprods = paginator.page(page)
    except PageNotAnInteger:
        pageprods = paginator.page(1)
    except EmptyPage:
        pageprods = paginator.page(paginator.num_pages)

    return render(req, 'shop/list.html', {
            'category': category, 'categories': categories,
            'pageprods': pageprods, 'cart_product_form': cart_product_form,
            'quick_search_form': quick_search_form})


def product_detail(req, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    categories = product.category.all()
    cart_product_form = CartAddProductForm()
    return render(req, 'shop/detail.html', {
            'product': product,
            'categories': categories,
            'cart_product_form': cart_product_form})
