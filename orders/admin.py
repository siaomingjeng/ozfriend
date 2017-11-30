from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from .models import Order, OrderItem, Courier, Photo
from .split import split_save
from django.contrib import messages


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    fields = ('product', 'price_aud', 'price_rmb', 'quantity', 'expense_aud',
              'expense_aud_card', 'expense_rmb')


class PhotoInline(admin.TabularInline):
    model = Photo
    raw_id_fields = ['order']
    extra = 0
    readonly_fields = ('thumbnail',)
    fields = ('id', 'nature', 'image', 'thumbnail', )


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['payer']
    list_display = ['id', 'payer', 'receiver', 'paid', 'delivered',
                    'track_result', 'created']
    readonly_fields = ('original',)
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline, PhotoInline]
    fields = (('payer', 'paid', 'original'), ('receiver', 'phone'),
              'address', 'message',
              ('courier', 'delivered', 'delivered_date'),
              ('track', 'track_result'),
              ('total_price_rmb', 'total_expense_aud',
               'total_price_aud', 'total_expense_rmb'))

    def change_view(self, request, obj, form_url='', extra_context=None):
        if '_delete2new' in request.POST:
            res = split_save(request, obj)
            if res['status'] == 'success':
                messages.success(request, res['msg'])
                return HttpResponseRedirect(request.path)
            else:
                messages.error(request, res['msg'])
                return HttpResponseRedirect(request.path)
        else:
            return super().change_view(request, obj, form_url, extra_context)

admin.site.register(Order, OrderAdmin)


class CourierAdmin(admin.ModelAdmin):
    list_display = ['chinese', 'name', 'url']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Courier, CourierAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price_rmb', 'quantity',
                    'expense_aud', 'expense_aud_card']
admin.site.register(OrderItem, OrderItemAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'nature', 'image', 'thumbnail']
admin.site.register(Photo, PhotoAdmin)
