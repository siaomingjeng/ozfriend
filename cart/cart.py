from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, req):
        """Initialize the cart"""
        self.session = req.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                    'quantity': 0, 'price_rmb': float(product.price_rmb),
                    'weight': product.weight,  # default Int
                    'category': product.category.first().slug,  # default str
                    'product_url': product.get_absolute_url(),  # default str
                    'ico_url': product.ico.url,  # default str
                    'chinese': product.chinese,  # default str
                    'id': product_id}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def get_quantity(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            return 0
        else:
            return int(self.cart[product_id]['quantity'])

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        for id, item in self.cart.items():
            item['total_price_rmb'] = item['price_rmb']*item['quantity']
            item['total_weight'] = item['weight']*item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def len(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price_rmb_with_delivery(self):
        return self.get_total_price_rmb()+self.get_delivery_fee_aud()

    def get_total_price_rmb(self, misc=False):
        if not misc:
            return round(sum(Decimal(item['price_rmb'])*item['quantity']
                         for item in self.cart.values()), 2)
        else:
            misc = []
            for item in self.cart.values():
                if 'milk-powder' != item['category']:
                    misc.append(Decimal(item['price_rmb'])*item['quantity'])
            return sum(misc)

    def get_total_expense_aud(self):
        return sum(item['quantity']*item['product'].expense_aud
                   for item in self.cart.values())

    def get_total_weight(self, for_delivery=False):
        milk = []
        misc = []
        for item in self.cart.values():
            if 'milk-powder' == item['category']:
                milk.append(item['weight']*item['quantity'])
            else:
                misc.append(item['weight']*item['quantity'])
        res = {'milk': sum(milk), 'misc': sum(misc)}
        if for_delivery:
            if res['milk'] > 0 and res['milk'] < 1000:
                res['milk'] = 1000
            if res['misc'] > 0 and res['misc'] < 1000:
                res['misc'] = 1000
        return res

    def get_delivery_expense_aud(self):
        weight = self.get_total_weight(for_delivery=True)
        return 0 if not weight else (weight['milk']*3.2+weight['misc']*5)/1000

    def get_delivery_fee_aud(self, thres=399):
        if self.get_total_price_rmb(misc=True) > thres:
            return 0
        else:
            weight = self.get_total_weight(for_delivery=True)
            return Decimal(weight['misc']*35.0/1000)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
