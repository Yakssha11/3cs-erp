from django.urls import path
from . import views

urlpatterns = [
    path('',        views.chicken_production_list,   name='chicken_production_list'),
    path('save/',   views.chicken_production_save,   name='chicken_production_save'),
    path('delete/<int:pk>/', views.chicken_production_delete, name='chicken_production_delete'),
    path('export/', views.export_chicken_production, name='export_chicken_production'),
]