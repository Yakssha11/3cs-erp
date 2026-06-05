from django.urls import path
from . import views

urlpatterns = [
    path('',                     views.flock_list,      name='flock_list'),
    path('save/',                views.flock_save,      name='flock_save'),
    path('delete/<int:pk>/',     views.flock_delete,    name='flock_delete'),
    path('transfer/<int:pk>/',   views.flock_transfer,  name='flock_transfer'),
    path('mortality/save/',      views.mortality_save,  name='mortality_save'),
    path('mortality/delete/<int:pk>/', views.mortality_delete, name='mortality_delete'),
    path('edit/<int:pk>/',       views.flock_update,    name='flock_update'),
    path('mortality/edit/<int:pk>/', views.mortality_update, name='mortality_update'),
    path('export/',              views.export_flock,    name='export_flock'),
    path('info/<int:pk>/',       views.flock_info,      name='flock_info'),
    path('quick-mortality/',     views.quick_mortality, name='quick_mortality'),
]