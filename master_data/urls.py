from django.urls import path
from . import views

urlpatterns = [
    path('',                           views.master_data_view,    name='master_data'),
    path('records/',                   views.master_data_records, name='master_data_records'),

    # customers
    path('customer/save/',             views.customer_save,       name='customer_save'),
    path('customer/delete/<int:pk>/',  views.customer_delete,     name='customer_delete'),

    # suppliers
    path('supplier/save/',             views.supplier_save,       name='supplier_save'),
    path('supplier/delete/<int:pk>/',  views.supplier_delete,     name='supplier_delete'),

    # materials
    path('material/save/',             views.material_save,       name='material_save'),
    path('material/delete/<int:pk>/',  views.material_delete,     name='material_delete'),
    path('material/update/<int:pk>/',  views.material_update,     name='material_update'),
    path('material/list/',             views.get_materials,       name='get_materials_list'),
]