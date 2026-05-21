from django.urls import path
from . import views

urlpatterns = [
    path('',       views.consumption_list, name='consumption_list'),
    path('save/',  views.consumption_save, name='consumption_save'),
    path('delete/<int:pk>/', views.consumption_delete, name='consumption_delete'),
    path('items/', views.get_items,        name='get_items'),
    path('edit/<int:pk>/', views.consumption_update, name='consumption_update'),
    path('export/', views.export_consumption, name='export_consumption'),
]