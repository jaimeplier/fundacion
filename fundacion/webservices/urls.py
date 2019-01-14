from django.urls import path

from webservices.catalogos import ListSexo, ListReligion, ListGradoEstudios, ListOcupacion
from webservices.views import ResumenLlamada

app_name = 'webservices'

urlpatterns = [
    path('resumenLlamada/', ResumenLlamada.as_view(), name='resumen_puntos_mes'),

    # Catalogos

    path('list_sexos/', ListSexo.as_view(), name='list_sexos'),
    path('list_religiones/', ListReligion.as_view(), name='list_religiones'),
    path('list_grado_estudios/', ListGradoEstudios.as_view(), name='list_grado_estudios'),
    path('list_ocupaciones/', ListOcupacion.as_view(), name='list_ocupaciones'),

]
