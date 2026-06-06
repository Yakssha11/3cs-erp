from django.urls import path
from . import views

urlpatterns = [
    # egg price
    path('',                        views.config_view,       name='config'),
    path('save/',                   views.config_save,       name='config_save'),

    # buildings
    path('building/save/',          views.building_save,     name='building_save'),
    path('building/delete/<int:pk>/', views.building_delete, name='building_delete'),

    # categories
    path('category/save/',          views.category_save,     name='category_save'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # units
    path('unit/save/',              views.unit_save,         name='unit_save'),
    path('unit/delete/<int:pk>/',   views.unit_delete,       name='unit_delete'),

    # causes
    path('cause/save/',             views.cause_save,        name='cause_save'),
    path('cause/delete/<int:pk>/',  views.cause_delete,      name='cause_delete'),

    # sales targets
    path('target/save/',            views.target_save,       name='target_save'),
    path('target/delete/<int:pk>/', views.target_delete,     name='target_delete'),

    # chicken price
    path('chicken-price/save/',     views.chicken_price_save, name='chicken_price_save'),

    # uom conversions
    path('uom/save/',               views.uom_save,          name='uom_save'),
    path('uom/delete/<int:pk>/',    views.uom_delete,        name='uom_delete'),
]