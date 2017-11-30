from django.contrib import admin
from .models import FX


class FxAdmin(admin.ModelAdmin):
    list_display = ['id', 'rmb', 'aud', 'date']
    list_filter = ['date']

admin.site.register(FX, FxAdmin)
