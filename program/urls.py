from django.urls import path
from . import views

urlpatterns = [
    path('growing/',                    views.program_growing,  name='program_growing'),
    path('laying/',                     views.program_laying,   name='program_laying'),
    path('save/',                       views.program_save,     name='program_save'),
    path('delete/<int:pk>/',            views.program_delete,   name='program_delete'),
    path('<int:program_pk>/step/save/', views.step_save,        name='step_save'),
    path('step/delete/<int:pk>/',       views.step_delete,      name='step_delete'),
    path('step/update/<int:pk>/',       views.step_update,      name='step_update'),
    path('view/growing/',               views.view_growing,     name='view_growing'),
    path('view/laying/',                views.view_laying,      name='view_laying'),
    path('export/<int:pk>/',            views.export_program,   name='export_program'),
    path('import/<int:pk>/',            views.import_program,   name='import_program'),
    path('batch/save/',                 views.batch_save,       name='batch_save'),
    path('batch/delete/<int:pk>/',      views.batch_delete,     name='batch_delete'),
]