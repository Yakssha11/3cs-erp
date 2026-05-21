from django.urls import path
from . import views

urlpatterns = [
    path('',      views.config_view,  name='config'),
    path('save/', views.config_save,  name='config_save'),
]