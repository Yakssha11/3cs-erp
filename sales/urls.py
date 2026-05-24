from django.urls import path
from . import views

urlpatterns = [
    path('growing/',                    views.growing_sales_list,    name='growing_sales'),
    path('growing/save/',               views.growing_sale_save,     name='growing_sale_save'),
    path('growing/delete/<int:pk>/',    views.growing_sale_delete,   name='growing_sale_delete'),
    path('growing/export/',             views.export_growing_sales,  name='export_growing_sales'),
    path('laying/',                     views.laying_sales_list,     name='laying_sales'),
    path('laying/save/',                views.laying_sale_save,      name='laying_sale_save'),
    path('laying/delete/<int:pk>/',     views.laying_sale_delete,    name='laying_sale_delete'),
    path('laying/export/',              views.export_laying_sales,   name='export_laying_sales'),
    path('analytics/',                  views.sales_analytics,       name='sales_analytics'),
    path('test-dr/',                    views.test_dr_pdf, name='test_dr_pdf'),
    path('analytics/data/',             views.sales_analytics_data, name='sales_analytics_data'),
]