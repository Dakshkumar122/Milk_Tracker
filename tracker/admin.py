from django.contrib import admin
from .models import MilkEntry


class MilkEntryAdmin(admin.ModelAdmin):
    list_display = ['date', 'quantity', 'price_per_litre']
    list_filter = ['date']

admin.site.register(MilkEntry, MilkEntryAdmin)