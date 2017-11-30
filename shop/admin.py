from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['chinese', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['chinese']
    list_display = ['id', 'chinese', 'name', 'price_rmb', 'stock',
                    'available']
    list_filter = ['available', 'category', 'updated', 'weight']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
