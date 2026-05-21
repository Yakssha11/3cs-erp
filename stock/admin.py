from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display  = ('item_id', 'name', 'price', 'quantity', 'category', 'date')
    search_fields = ('item_id', 'name', 'category')
    list_filter   = ('category',)