from django.urls import path
from . import views

urlpatterns = [
    path('',                           views.laying_flock_list,       name='laying_flock_list'),
    path('save/',                      views.laying_flock_save,       name='laying_flock_save'),
    path('delete/<int:pk>/',           views.laying_flock_delete,     name='laying_flock_delete'),
    path('edit/<int:pk>/',             views.laying_flock_update,     name='laying_flock_update'),
    path('transfer/<int:pk>/',         views.laying_flock_transfer,   name='laying_flock_transfer'),
    path('mortality/save/',            views.laying_mortality_save,   name='laying_mortality_save'),
    path('mortality/delete/<int:pk>/', views.laying_mortality_delete, name='laying_mortality_delete'),
    path('mortality/edit/<int:pk>/',   views.laying_mortality_update, name='laying_mortality_update'),
    path('info/<int:pk>/',             views.laying_flock_info,       name='laying_flock_info'),
    path('quick-mortality/',           views.quick_laying_mortality,  name='quick_laying_mortality'),
]