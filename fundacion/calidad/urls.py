from django.urls import path

from calidad.views import EvaluacionAdd, EvaluacionAjaxList, EvaluacionEdit, LlamadaAjaxList, CalificarServicio, \
    VerServicio
from . import views

app_name = 'calidad'

urlpatterns = [

    path('evaluacion/add/', EvaluacionAdd.as_view(), name='add_evaluacion'),
    path('evaluacion/list/', views.list_evaluacion, name='list_evaluacion'),
    path('evaluacion/ajax/list/', EvaluacionAjaxList.as_view(), name='list_ajax_evaluacion'),
    path('evaluacion/edit/<int:pk>', EvaluacionEdit.as_view(), name='edit_evaluacion'),
    path('evaluacion/list/delete/<int:pk>', views.delete_evaluacion, name='delete_evaluacion'),

    path('llamada/list/', views.list_llamada, name='list_llamada'),
    path('llamada/ajax/list/', LlamadaAjaxList.as_view(), name='list_ajax_llamada'),

    path('calificar_servicio/<int:pk>', CalificarServicio.as_view(), name='calificar_servicio'),
    path('ver_servicio/<int:pk>', VerServicio.as_view(), name='ver_servicio'),

    path('evaluacion/list/', views.list_evaluacion, name='list_evaluacion'),
    path('evaluacion/ajax/list/', EvaluacionAjaxList.as_view(), name='list_ajax_evaluacion'),

    ]