from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.laying_finance_list,   name='laying_finance_list'),
    path('save/',            views.laying_finance_save,   name='laying_finance_save'),
    path('delete/<int:pk>/', views.laying_finance_delete, name='laying_finance_delete'),
    path('edit/<int:pk>/',   views.laying_finance_update, name='laying_finance_update'),
    path('export/',          views.export_laying_finance, name='export_laying_finance'),
]