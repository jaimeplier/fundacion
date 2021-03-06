from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as vtoken

from webservices.Calidad import EvaluarServicio, ComentarioServicio
from webservices.Consejeros import PrimerRegistro, SeguimientoRegistro, ListConsejerosVictima, ListHistorialLLamada, \
    UltimaLLamada, BusquedaUsuario, ListConsejeros
from webservices.catalogos import ListSexo, ListReligion, ListGradoEstudios, ListOcupacion, ListViveCon, \
    ListTipoLlamada, ListTipoViolencia, ListViolentometro, ListAcudeInstitucion, ListMotivoLlamada, \
    ListTipificaciones, ListTipificacionesCategorias, ListModalidadViolencia, \
    ListVictimas, ListAgresor, ListRedesApoyo, ListMedioContacto, ListNivelRiesgo, \
    ListRecomendacionesRiesgo, ListFaseCambio, ListComoSeEntero, ListAliado, ListLineaNegocio, \
    ListTipificacionesSubcategorias, ListTutor, ListDatosCP, ListEstadoCivil, ListSucursales, ListExamenMental, \
    ListEstado, ListMunicipio, GetSucursal
from webservices.views import ResumenLlamada, ListUsuarios, ListEstatusActividadUsuario, UpdateEstatusActividadUsuario, \
    AgregaArchivoMensaje, AgregaArchivoRecado, ListArchivoMensaje, ListArchivoRecado, CambiarEstatusInstitucion, \
    ResumenLlamadaMes, ReporteUsuarioViewSet, CountPendientes, CountAvisos, CountRecados
from . import views

app_name = 'webservices'

router = routers.DefaultRouter()
router.register(r'mensajes', views.MensajesViewSet)
router.register(r'recados', views.RecadosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', vtoken.obtain_auth_token),
    path('list_usuarios/', ListUsuarios.as_view(), name='list_usuarios'),
    path('list_estatus_actividad_usuarios/', ListEstatusActividadUsuario.as_view(), name='list_estatus_actividad_usuarios'),
    path('update_estatus_actividad_usuarios/', UpdateEstatusActividadUsuario.as_view(), name='update_estatus_actividad_usuarios'),
    path('add_archivo_mensaje/', AgregaArchivoMensaje.as_view(), name='add_archivo_mensaje'),
    path('add_archivo_recado/', AgregaArchivoRecado.as_view(), name='add_archivo_recado'),
    path('list_archivos_mensaje/', ListArchivoMensaje.as_view(), name='list_archivos_mensaje'),
    path('list_archivo_recado/', ListArchivoRecado.as_view(), name='list_archivo_recado'),
    path('cambiar_estatus_institucion/', CambiarEstatusInstitucion.as_view(), name='cambiar_estatus_institucion'),

    path('list_count_pendientes/', CountPendientes.as_view(), name='list_count_pendientes'),
    path('list_count_avisos/', CountAvisos.as_view(), name='list_count_avisos'),
    path('list_count_recados/', CountRecados.as_view(), name='list_count_recados'),
    # Consejeros:
    path('registro_primera_vez/', PrimerRegistro.as_view(), name='registro_primera_vez'),
    path('registro_seguimiento/', SeguimientoRegistro.as_view(), name='registro_seguimiento'),
    path('list_consejeros_victima/', ListConsejerosVictima.as_view(), name='list_consejeros_victima'),
    path('list_historial_llamada/', ListHistorialLLamada.as_view(), name='list_historial_llamada'),
    path('ultima_llamada/', UltimaLLamada.as_view(), name='ultima_llamada'),
    path('busqueda_usuario/', BusquedaUsuario.as_view(), name='busqueda_usuario'),
    path('list_consejeros/', ListConsejeros.as_view(), name='list_consejeros'),

    # Calidad:
    path('evaluar_servicio/', EvaluarServicio.as_view(), name='evaluar_servicio'),
    path('comentarios_servicio/', ComentarioServicio.as_view(), name='comentarios_servicio'),

    # Supervisores:
    path('resumenLlamada/', ResumenLlamada.as_view(), name='resumen_puntos_mes'),
    path('resumen_llamada_mes/', ResumenLlamadaMes.as_view(), name='resumen_puntos_mes'),
    path('reporte_usuarios/', ReporteUsuarioViewSet.as_view(), name='reporte_usuarios'),

    # Catalogos:
    path('list_sexos/', ListSexo.as_view(), name='list_sexos'),
    path('list_religiones/', ListReligion.as_view(), name='list_religiones'),
    path('list_grado_estudios/', ListGradoEstudios.as_view(), name='list_grado_estudios'),
    path('list_ocupaciones/', ListOcupacion.as_view(), name='list_ocupaciones'),
    path('list_vive_con/', ListViveCon.as_view(), name='list_vive_con'),
    path('list_tipos_de_llamada/', ListTipoLlamada.as_view(), name='list_tipos_de_llamada'),
    path('list_motivo_de_llamada/', ListMotivoLlamada.as_view(), name='list_motivo_de_llamada'),
    path('list_tipificaciones/', ListTipificaciones.as_view(), name='list_tipificaciones'),
    path('list_tipificaciones_categorias/', ListTipificacionesCategorias.as_view(), name='list_tipificaciones_categorias'),
    path('list_tipificaciones_subcategorias/', ListTipificacionesSubcategorias.as_view(), name='list_tipificaciones_subcategorias'),
    path('list_modalidad_violencia/', ListModalidadViolencia.as_view(), name='list_modalidad_violencia'),
    path('list_tipos_violencia/', ListTipoViolencia.as_view(), name='list_tipos_violencia'),
    path('list_violentometro/', ListViolentometro.as_view(), name='list_violentometro'),
    path('list_victimas/', ListVictimas.as_view(), name='list_victimas'),
    path('list_agresor/', ListAgresor.as_view(), name='list_agresor'),
    path('list_redes_apoyo/', ListRedesApoyo.as_view(), name='list_redes_apoyo'),
    path('list_medio_contacto/', ListMedioContacto.as_view(), name='list_medio_contacto'),
    path('list_instituciones/', ListAcudeInstitucion.as_view(), name='list_instituciones'),
    path('list_sucursales/', ListSucursales.as_view(), name='list_sucursales'),
    path('get_sucursal/', GetSucursal.as_view(), name='get_sucursal'),
    path('list_nivel_riesgo/', ListNivelRiesgo.as_view(), name='list_nivel_riesgo'),
    path('list_recomendaciones_riesgo/', ListRecomendacionesRiesgo.as_view(), name='list_recomendaciones_riesgo'),
    path('list_fase_cambio/', ListFaseCambio.as_view(), name='list_fase_cambio'),
    path('list_como_se_entero/', ListComoSeEntero.as_view(), name='list_como_se_entero'),
    path('list_aliado/', ListAliado.as_view(), name='list_aliado'),
    path('list_line_negocio/', ListLineaNegocio.as_view(), name='list_line_negocio'),
    path('list_tutor/', ListTutor.as_view(), name='list_tutor'),
    path('list_cp/', ListDatosCP.as_view(), name='list_cp'),
    path('list_estado_civil/', ListEstadoCivil.as_view(), name='list_estado_civil'),
    path('list_examen_mental/', ListExamenMental.as_view(), name='list_examen_mental'),
    path('list_estado/', ListEstado.as_view(), name='list_estado'),
    path('list_municipio/', ListMunicipio.as_view(), name='list_municipio'),

]
