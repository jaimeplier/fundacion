from django.urls import path

from webservices.catalogos import ListSexo, ListReligion, ListGradoEstudios, ListOcupacion, ListViveCon, \
    ListTipoLlamada, ListTipoCaso, ListTipoViolencia, ListViolentometro
from webservices.views import ResumenLlamada

app_name = 'webservices'

urlpatterns = [
    path('resumenLlamada/', ResumenLlamada.as_view(), name='resumen_puntos_mes'),

    # Catalogos:

    path('list_sexos/', ListSexo.as_view(), name='list_sexos'),
    path('list_religiones/', ListReligion.as_view(), name='list_religiones'),
    path('list_grado_estudios/', ListGradoEstudios.as_view(), name='list_grado_estudios'),
    path('list_ocupaciones/', ListOcupacion.as_view(), name='list_ocupaciones'),
    path('list_redes_apoyo/', ListViveCon.as_view(), name='list_redes_apoyo'),
    path('list_tipos_de_llamada/', ListTipoLlamada.as_view(), name='list_tipos_de_llamada'),
    path('list_tipificaciones/', ListTipoCaso.as_view(), name='list_tipificaciones'),
    # Modalidad
    path('list_tipos_violencia/', ListTipoViolencia.as_view(), name='list_tipos_violencia'),
    # Fase de violencia
    # Semaforo
    path('list_violentometro/', ListViolentometro.as_view(), name='list_violentometro'),


]
