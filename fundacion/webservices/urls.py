from django.urls import path

from webservices.views import ResumenLlamada

app_name = 'webservices'

urlpatterns = [
    path('resumenLlamada/', ResumenLlamada.as_view(), name='resumen_puntos_mes'),
    ]