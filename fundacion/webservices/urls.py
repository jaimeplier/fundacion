from django.urls import path

from webservices.catalogos import ListSexo
from webservices.views import ResumenLlamada

app_name = 'webservices'

urlpatterns = [
    path('resumenLlamada/', ResumenLlamada.as_view(), name='resumen_puntos_mes'),

    # Catalogos

    path('list_sexos/', ListSexo.as_view(), name='list_sexo'),

]
