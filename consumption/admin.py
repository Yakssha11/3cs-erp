from django.contrib import admin
from .models import Consumption

@admin.register(Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display  = ('date_consumed', 'growing_house', 'category',
                     'item_name', 'quantity', 'unit', 'recorded_by')
    search_fields = ('item_name', 'growing_house', 'recorded_by')
    list_filter   = ('growing_house', 'category')