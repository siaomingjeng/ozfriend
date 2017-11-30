from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    chinese = models.CharField(max_length=200, db_index=True, unique=True)
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    chinese = models.CharField(max_length=200, db_index=True, unique=True)
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    reference = models.URLField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    price_rmb = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                    verbose_name="Selling Price RMB")
    price_aud = models.DecimalField(max_digits=6, decimal_places=2, default=0,
                                    verbose_name="Selling Price AUD")
    expense_aud = models.DecimalField(max_digits=6, decimal_places=2,
                                      default=0,
                                      verbose_name="Buying Cost AUD")
    expense_rmb = models.DecimalField(max_digits=6, decimal_places=2,
                                      default=0,
                                      verbose_name="Buying Cost RMB")
    weight = models.PositiveIntegerField(blank=True, default=0,
                                         verbose_name="Weight (g)")
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def image_path(instance, filename):
        if instance.slug:
            brand = instance.slug.split('-')[0]
        else:
            brand = "default"
        filename = "IMAGE_"+instance.slug+"."+filename.split('.')[-1]
        return '{0}/{1}'.format(brand, filename)

    def ico_path(instance, filename):
        if instance.slug:
            brand = instance.slug.split('-')[0]
        else:
            brand = "default"
        filename = "ICO_"+instance.slug+"."+filename.split('.')[-1]
        return '{0}/{1}'.format(brand, filename)

    ico = models.ImageField(upload_to=ico_path)
    image = models.ImageField(upload_to=image_path, blank=True)

    class Meta:
        ordering = ('chinese',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.chinese

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
