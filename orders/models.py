from django.db import models
from shop.models import Product
from django.template.loader import render_to_string


class Courier(models.Model):
    chinese = models.CharField(max_length=20, db_index=True, unique=True,
                               verbose_name="快递公司")
    name = models.CharField(max_length=40, db_index=True, unique=True,
                            verbose_name="英文名称")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    url = models.URLField(max_length=300, verbose_name="官方网站")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    cost_misc_kg = models.DecimalField(max_digits=6, decimal_places=2,
                                       verbose_name="杂货/kg")
    cost_milk_kg = models.DecimalField(max_digits=6, decimal_places=2,
                                       verbose_name="奶粉/kg")
    cost_box = models.DecimalField(max_digits=6, decimal_places=2,
                                   verbose_name="箱子/个")

    def __str__(self):
        return self.chinese


class Order(models.Model):
    courier = models.ForeignKey(Courier, related_name='couriers', default=1,
                                verbose_name="快递公司")
    receiver = models.CharField(max_length=20, verbose_name="收货人")
    payer = models.CharField(max_length=20, blank=True, verbose_name="下单人")
    phone = models.CharField(max_length=15, verbose_name="收货人电话")
    address = models.CharField(max_length=100, verbose_name="收货地址")
    total_expense_aud = models.DecimalField(max_digits=10, decimal_places=2,
                                            default=0,
                                            verbose_name="总成本(AUD)")
    total_expense_rmb = models.DecimalField(max_digits=10, decimal_places=2,
                                            default=0,
                                            verbose_name="总成本(RMB)")
    total_price_rmb = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0,
                                          verbose_name="总售价(RMB)")
    total_price_aud = models.DecimalField(max_digits=10, decimal_places=2,
                                          default=0,
                                          verbose_name="总售价(AUD)")
    fx_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                  verbose_name="汇率(1AUD=)")
    track = models.CharField(max_length=20, blank=True, verbose_name="快递单号")
    track_result = models.CharField(max_length=100, blank=True,
                                    verbose_name="快递状态")
    message = models.TextField(max_length=100, blank=True,
                               verbose_name="客户留言")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    delivered_date = models.DateField(null=True, blank=True)
    original = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_price_rmb(self):
        return sum(item.get_item_total_price_rmb()
                   for item in self.items.all())

    def get_total_price_aud(self):
        return sum(item.get_item_total_price_aud()
                   for item in self.items.all())

    def get_total_expense_rmb(self):
        return sum(item.get_item_total_expense_rmb()
                   for item in self.items.all())

    def get_total_expense_aud(self):
        return sum(item.get_item_total_expense_aud()
                   for item in self.items.all())

    # overwrite save(self, *args, **kwargs) isn't good with admin inline save,
    # when Orderitems are not saved yet, no way to calculate.
    # def save(self, *args, **kwargs):
    #    self.total_price_rmb = self.get_total_price_rmb()
    #    self.total_price_aud = self.get_total_price_aud()
    #    self.total_expense_rmb = self.get_total_expense_rmb()
    #    self.total_expense_aud = self.get_total_expense_aud()
    #    super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items',
                                verbose_name="产品")
    # default to product.price
    price_rmb = models.DecimalField(max_digits=8, decimal_places=2,
                                    default=0, verbose_name="售价RMB")
    # default to product.price
    price_aud = models.DecimalField(max_digits=8, decimal_places=2, blank=True,
                                    default=0, verbose_name="售价AUD")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    # default=0, default to product.cost
    expense_aud = models.DecimalField(max_digits=8, decimal_places=2,
                                      default=0, verbose_name="成本AUD")
    # Australian Debit Card or Chinese Credit Card
    CARD_CHOICES = (('CN', "中国"), ('OZ', "澳洲"),)
    expense_aud_card = models.CharField(max_length=2, choices=CARD_CHOICES,
                                        default="CN", verbose_name="AUD来源")
    # default = 0, default to product.cost
    expense_rmb = models.DecimalField(max_digits=8, decimal_places=2,
                                      blank=True, default=0,
                                      verbose_name="成本RMB")

    # set default value of expense to the cost of ForeignKey product.
    # (But price uses the value returned from webpage.)
    # def save(self, *args, **kwargs):
    #    if not self.expense_aud:
    #        self.expense_aud = self.product.expense_aud
    #    if not self.expense_rmb:
    #        self.expense_rmb = self.product.expense_rmb
    #    if not self.price_rmb:
    #        self.price_rmb = self.product.price_rmb
    #    if not self.price_aud:
    #        self.price_aud = self.product.price_aud
    #    super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)

    def get_item_total_price_rmb(self):
        return self.price_rmb * self.quantity

    def get_item_total_price_aud(self):
        return self.price_aud * self.quantity

    def get_item_total_expense_rmb(self):
        return self.expense_rmb * self.quantity

    def get_item_total_expense_aud(self):
        return self.expense_aud * self.quantity


class Photo(models.Model):
    order = models.ForeignKey(Order, related_name='photos')
    # Courier Order,Dispatch Photo
    NATURE_CHOICES = (('CO', "快递单"), ('DP', "发货照"),)
    nature = models.CharField(max_length=2, choices=NATURE_CHOICES,
                              default="DP", verbose_name="图片性质")
    image = models.ImageField(upload_to="DISPATCH/%Y%m", blank=True)

    def thumbnail(self):
        return render_to_string('orders/thumb.html',
                                {'image_url': self.image.url})
