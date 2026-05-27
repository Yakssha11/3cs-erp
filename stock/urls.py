from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.stock_list,   name='stock_list'),
    path('save/',            views.stock_save,   name='stock_save'),
    path('delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    path('edit/<int:pk>/',   views.stock_update, name='stock_update'),
    path('export/',          views.export_stock, name='export_stock'),
]