from django.contrib import admin
from .models import Flock, Mortality

@admin.register(Flock)
class FlockAdmin(admin.ModelAdmin):
    list_display  = ('batch_name', 'growing_house', 'start_count',
                     'current_count', 'date_placed', 'status')
    search_fields = ('batch_name', 'growing_house')
    list_filter   = ('growing_house', 'status')

@admin.register(Mortality)
class MortalityAdmin(admin.ModelAdmin):
    list_display  = ('flock', 'growing_house', 'death_date',
                     'count', 'cause', 'recorded_by')
    search_fields = ('growing_house', 'cause', 'recorded_by')
    list_filter   = ('growing_house', 'cause')