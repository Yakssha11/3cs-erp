from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.finance_list,   name='finance_list'),
    path('save/',            views.finance_save,   name='finance_save'),
    path('delete/<int:pk>/', views.finance_delete, name='finance_delete'),
    path('edit/<int:pk>/', views.finance_update, name='finance_update'),
    path('export/', views.export_finance, name='export_finance'),
]