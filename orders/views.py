from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.models import Product
from orders.models import Courier, Order
from .wechat3 import send_wechat
import json
from .validate import get_validate_img, validated
from django.http import HttpResponse


@staff_member_required
def order_inner(req):
    if req.is_ajax():
        if req.method == 'POST':
            print(req)
            receiver = req.POST['receiver']
            order = Order.objects.filter(receiver=receiver).first()
            if order:
                resp = {'address': order.address, 'phone': order.phone,
                        'status': True}
            else:
                resp = {'status': False}
            return HttpResponse(json.dumps(resp),
                                content_type='application/json')


def order_validate_img(req):
    image = get_validate_img(req)
    res = HttpResponse(content_type='image/png')
    image.save(res, 'png')
    return res


def order_create(req):
    cart = Cart(req)
    if req.method == 'POST':
        form = OrderCreateForm(req.POST)
        if not validated(req):
            return render(req, 'orders/create.html',
                          {'cart': cart, 'form': form})
        if form.is_valid():
            if 0 == len(cart):
                return render(req, 'orders/already.html')
            order = form.save()
            wechat_msg = "Order: {0}\nReceiver:{1}, Ph:{2}, Add:{3}\n".format(
                    order.id, order.receiver, order.phone, order.address)
            if req.user.is_authenticated() and hasattr(req.user, 'first_name'):
                order.payer = req.user.first_name
                order.save()
                wechat_msg += 'Payer:{}**\n'.format(order.payer)
            for item in cart:
                item['product'] = Product.objects.get(id=item['id'])
                OrderItem.objects.create(
                        order=order, product=item['product'],
                        price_rmb=item['price_rmb'],
                        quantity=item['quantity'],
                        expense_aud=item['product'].expense_aud)
                wechat_msg += '\n{0}({1}) ${2} X {3}'.format(
                        item['product'].name, item['product'].chinese,
                        item['product'].expense_aud, item['quantity'])
            # Delivery Fee
            OrderItem.objects.create(
                    order=order, product=Product.objects.get(id=2),
                    price_rmb=cart.get_delivery_fee_aud(),
                    expense_aud=cart.get_delivery_expense_aud(),
                    expense_aud_card='OZ')
            wechat_msg += '\n Delivery fee around:${}'.format(
                    cart.get_delivery_expense_aud())
            # Discount
            OrderItem.objects.create(order=order,
                                     product=Product.objects.get(id=1))
            order.total_price_rmb = cart.get_total_price_rmb_with_delivery()
            order.total_expense_aud = cart.get_total_expense_aud()
            # order.courier=Courier.objects.get(id=1)
            order.save()
            # clear the cart
            cart.clear()
            # send wechat message
            status_wechat = send_wechat(wechat_msg)
            # log to be added!
            return render(req, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
        return render(req, 'orders/create.html', {'cart': cart, 'form': form})
