from django.urls import path

from . import views

app_name = 'supervisor'

urlpatterns = [

    path('reportes/', views.reportes, name='reportes'),
    path('resumen/', views.resumen, name='resumen'),
]
