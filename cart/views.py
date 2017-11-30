from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from django.http import HttpResponse
from .cart import Cart
from .forms import CartAddProductForm
from django.http import Http404


@require_POST
def cart_add(req, product_id):
    cart = Cart(req)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(req.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if req.is_ajax():
            if cart.get_quantity(product) >= 8:
                return HttpResponse("fail")
            else:
                cart.add(product=product, quantity=cd['quantity'],
                         update_quantity=cd['update'])
                return HttpResponse("success")
        elif not cd['update'] or cart.get_quantity(product) < 8:
            cart.add(product=product, quantity=cd['quantity'],
                     update_quantity=cd['update'])
        else:
            raise Http404("You can only buy less than 8 the \
                          same products in one order")
    return redirect('cart:cart_detail')


def cart_remove(req, product_id):
    cart = Cart(req)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(req):
    cart = Cart(req)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'], 'update': True})
    return render(req, 'cart/detail.html', {'cart': cart})
