from django.urls import path

from supervisor.views import LlamadaAjaxList, ProductividadAjaxList
from . import views

app_name = 'supervisor'

urlpatterns = [

    path('reportes/', views.reportes, name='reportes'),
    path('reporte_servicios/ajax/list/', LlamadaAjaxList.as_view(), name='list_ajax_llamada'),
    path('reporte_productividad/ajax/list/', ProductividadAjaxList.as_view(), name='list_ajax_productividad'),
    path('resumen/', views.resumen, name='resumen'),
]
