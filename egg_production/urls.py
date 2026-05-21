from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.egg_production_list,   name='egg_production_list'),
    path('save/',            views.egg_production_save,   name='egg_production_save'),
    path('delete/<int:pk>/', views.egg_production_delete, name='egg_production_delete'),
    path('edit/<int:pk>/',   views.egg_production_update, name='egg_production_update'),
    path('export/',          views.export_eggs, name='export_eggs'),
]