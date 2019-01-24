from django.urls import path

from webservices.Consejeros import PrimerRegistro, SeguimientoRegistro, ListConsejerosVictima, ListHistorialLLamada
from webservices.catalogos import ListSexo, ListReligion, ListGradoEstudios, ListOcupacion, ListViveCon, \
    ListTipoLlamada, ListTipoCaso, ListTipoViolencia, ListViolentometro, ListAcudeInstitucion, ListMotivoLlamada, \
    ListTipificaciones, ListTipificacionesCategorias, ListModalidadViolencia, ListFaseViolencia, ListSemaforo, \
    ListVictimas, ListAgresor, ListRedesApoyo, ListEstatusLLamada, ListMedioContacto
from webservices.views import ResumenLlamada

app_name = 'webservices'

urlpatterns = [
    # Consejeros:
    path('registro_primera_vez/', PrimerRegistro.as_view(), name='registro_primera_vez'),
    path('registro_seguimiento/', SeguimientoRegistro.as_view(), name='registro_seguimiento'),
    path('list_consejeros_victima/', ListConsejerosVictima.as_view(), name='list_consejeros_victima'),
    path('list_historial_llamada/', ListHistorialLLamada.as_view(), name='list_historial_llamada'),

    # Supervisores:
    path('resumenLlamada/', ResumenLlamada.as_view(), name='resumen_puntos_mes'),

    # Catalogos:
    path('list_sexos/', ListSexo.as_view(), name='list_sexos'),
    path('list_religiones/', ListReligion.as_view(), name='list_religiones'),
    path('list_grado_estudios/', ListGradoEstudios.as_view(), name='list_grado_estudios'),
    path('list_ocupaciones/', ListOcupacion.as_view(), name='list_ocupaciones'),
    path('list_redes_apoyo/', ListViveCon.as_view(), name='list_redes_apoyo'),
    path('list_tipos_de_llamada/', ListTipoLlamada.as_view(), name='list_tipos_de_llamada'),
    path('list_motivo_de_llamada/', ListMotivoLlamada.as_view(), name='list_motivo_de_llamada'),
    path('list_tipificaciones/', ListTipificaciones.as_view(), name='list_tipificaciones'),
    path('list_tipificaciones_categorias/', ListTipificacionesCategorias.as_view(), name='list_tipificaciones_categorias'),
    #path('list_tipificaciones/', ListTipoCaso.as_view(), name='list_tipificaciones'),
    path('list_modalidad_violencia/', ListModalidadViolencia.as_view(), name='list_modalidad_violencia'),
    path('list_tipos_violencia/', ListTipoViolencia.as_view(), name='list_tipos_violencia'),
    path('list_fases_violencia/', ListFaseViolencia.as_view(), name='list_fases_violencia'),
    path('list_semaforo/', ListSemaforo.as_view(), name='list_semaforo'),
    path('list_violentometro/', ListViolentometro.as_view(), name='list_violentometro'),
    path('list_victimas/', ListVictimas.as_view(), name='list_victimas'),
    path('list_agresor/', ListAgresor.as_view(), name='list_agresor'),
    path('list_redes_apoyo/', ListRedesApoyo.as_view(), name='list_redes_apoyo'),
    path('list_medio_contacto/', ListMedioContacto.as_view(), name='list_medio_contacto'),
    path('list_instituciones/', ListAcudeInstitucion.as_view(), name='list_instituciones'),
    path('list_estatus_llamada/', ListEstatusLLamada.as_view(), name='list_estatus_llamada'),



]
