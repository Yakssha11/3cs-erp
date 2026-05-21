from django.contrib import admin
from .models import Finance

@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display  = ('expense_date', 'nature', 'building',
                     'amount', 'person')
    search_fields = ('nature', 'building', 'person')
    list_filter   = ('nature', 'building')