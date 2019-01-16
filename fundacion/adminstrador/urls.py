from django.urls import path

from adminstrador.views import AcudeInstitucionAdd, AcudeInstitucionAjaxList, AcudeInstitucionEdit, EstadoAdd, \
    EstadoAjaxList, EstadoEdit, PaisAdd, PaisAjaxList, PaisEdit, EstadoCivilAdd, EstadoCivilAjaxList, EstadoCivilEdit, \
    EstatusAdd, EstatusAjaxList, EstatusEdit, LenguaIndigenaAdd, LenguaIndigenaAjaxList, LenguaIndigenaEdit, \
    MedioContactoAdd, MedioContactoAjaxList, MedioContactoEdit, ModalidadViolenciaAdd, ModalidadViolenciaAjaxList, \
    ModalidadViolenciaEdit, MunicipioAdd, MunicipioAjaxList, MunicipioEdit, NivelEstudioAdd, NivelEstudioAjaxList, \
    NivelEstudioEdit, NivelViolenciaAdd, NivelViolenciaAjaxList, NivelViolenciaEdit, OcupacionAdd, OcupacionAjaxList, \
    OcupacionEdit, ReligionAdd, ReligionAjaxList, ReligionEdit, TipoCasoAdd, TipoCasoAjaxList, TipoCasoEdit, \
    TipoViolenciaAdd, TipoViolenciaAjaxList, TipoViolenciaEdit, ViolentometroAdd, ViolentometroAjaxList, \
    ViolentometroEdit, ViveConAdd, ViveConAjaxList, ViveConEdit, ConsejeroAdd, ConsejeroAjaxList, \
    ConsejeroEdit, DirectorioAdd, DirectorioAjaxList, DirectorioEdit, SupervisorAdd, SupervisorAjaxList, \
    SupervisorEdit, ContactoInstitucionAdd, ContactoInstitucionAjaxList, ContactoInstitucionEdit, CalidadAdd, \
    CalidadAjaxList, CalidadEdit, LlamadaAjaxList, SexoAdd, SexoAjaxList, SexoEdit, AyudaAdd, AyudaAjaxList, AyudaEdit, \
    MotivoLLamadaAdd, MotivoLLamadaAjaxList, MotivoLLamadaEdit, EstatusLLamadaAdd, EstatusLLamadaAjaxList, \
    EstatusLLamadaEdit
from . import views

app_name = 'administrador'

urlpatterns = [

    path('reportes/', views.reportes, name='reportes'),
    path('reporte_llamada/ajax/list/', LlamadaAjaxList.as_view(), name='list_ajax_llamada'),

    path('resumen/', views.resumen, name='resumen'),
    path('catalogos/', views.catalogos, name='catalogos'),
    # Psicologos, Medicos, Abogados
    path('consejero/add/', ConsejeroAdd.as_view(), name='add_consejero'),
    path('consejero/list/', views.list_consejero, name='list_consejero'),
    path('consejero/ajax/list/', ConsejeroAjaxList.as_view(), name='list_ajax_consejero'),
    path('consejero/edit/<int:pk>', ConsejeroEdit.as_view(), name='edit_consejero'),
    path('consejero/list/delete/<int:pk>', views.delete_consejero, name='delete_consejero'),
    #Directorio
    path('directorio/add/', DirectorioAdd.as_view(), name='add_directorio'),
    path('directorio/list/', views.list_directorio, name='list_directorio'),
    path('directorio/ajax/list/', DirectorioAjaxList.as_view(), name='list_ajax_directorio'),
    path('directorio/edit/<int:pk>', DirectorioEdit.as_view(), name='edit_directorio'),
    path('directorio/list/delete/<int:pk>', views.delete_directorio, name='delete_directorio'),
    #Reportes
    path('supervisor/add/', SupervisorAdd.as_view(), name='add_supervisor'),
    path('supervisor/list/', views.list_supervisor, name='list_supervisor'),
    path('supervisor/ajax/list/', SupervisorAjaxList.as_view(), name='list_ajax_supervisor'),
    path('supervisor/edit/<int:pk>', SupervisorEdit.as_view(), name='edit_supervisor'),
    path('supervisor/list/delete/<int:pk>', views.delete_supervisor, name='delete_supervisor'),
    #Calidad
    path('calidad/add/', CalidadAdd.as_view(), name='add_calidad'),
    path('calidad/list/', views.list_calidad, name='list_calidad'),
    path('calidad/ajax/list/', CalidadAjaxList.as_view(), name='list_ajax_calidad'),
    path('calidad/edit/<int:pk>', CalidadEdit.as_view(), name='edit_calidad'),
    path('calidad/list/delete/<int:pk>', views.delete_calidad, name='delete_calidad'),

    # Catalogos
    path('acude_institucion/add/', AcudeInstitucionAdd.as_view(), name='add_acude_institucion'),
    path('acude_institucion/list/', views.list_acude_institucion, name='list_acude_institucion'),
    path('acude_institucion/ajax/list/', AcudeInstitucionAjaxList.as_view(), name='list_ajax_acude_institucion'),
    path('acude_institucion/edit/<int:pk>', AcudeInstitucionEdit.as_view(), name='edit_acude_institucion'),
    path('acude_institucion/list/delete/<int:pk>', views.delete_acude_institucion, name='delete_acude_institucion'),

    path('estado/add/', EstadoAdd.as_view(), name='add_estado'),
    path('estado/list/', views.list_estado, name='list_estado'),
    path('estado/ajax/list/', EstadoAjaxList.as_view(), name='list_ajax_estado'),
    path('estado/edit/<int:pk>', EstadoEdit.as_view(), name='edit_estado'),
    path('estado/list/delete/<int:pk>', views.delete_estado, name='delete_estado'),

    path('pais/add/', PaisAdd.as_view(), name='add_pais'),
    path('pais/list/', views.list_pais, name='list_pais'),
    path('pais/ajax/list/', PaisAjaxList.as_view(), name='list_ajax_pais'),
    path('pais/edit/<int:pk>', PaisEdit.as_view(), name='edit_pais'),
    path('pais/list/delete/<int:pk>', views.delete_pais, name='delete_pais'),

    path('estado_civil/add/', EstadoCivilAdd.as_view(), name='add_estado_civil'),
    path('estado_civil/list/', views.list_estado_civil, name='list_estado_civil'),
    path('estado_civil/ajax/list/', EstadoCivilAjaxList.as_view(), name='list_ajax_estado_civil'),
    path('estado_civil/edit/<int:pk>', EstadoCivilEdit.as_view(), name='edit_estado_civil'),
    path('estado_civil/list/delete/<int:pk>', views.delete_estado_civil, name='delete_estado_civil'),

    path('estatus/add/', EstatusAdd.as_view(), name='add_estatus'),
    path('estatus/list/', views.list_estatus, name='list_estatus'),
    path('estatus/ajax/list/', EstatusAjaxList.as_view(), name='list_ajax_estatus'),
    path('estatus/edit/<int:pk>', EstatusEdit.as_view(), name='edit_estatus'),
    path('estatus/list/delete/<int:pk>', views.delete_estatus, name='delete_estatus'),

    path('lengua_indigena/add/', LenguaIndigenaAdd.as_view(), name='add_lengua_indigena'),
    path('lengua_indigena/list/', views.list_lengua_indigena, name='list_lengua_indigena'),
    path('lengua_indigena/ajax/list/', LenguaIndigenaAjaxList.as_view(), name='list_ajax_lengua_indigena'),
    path('lengua_indigena/edit/<int:pk>', LenguaIndigenaEdit.as_view(), name='edit_lengua_indigena'),
    path('lengua_indigena/list/delete/<int:pk>', views.delete_lengua_indigena, name='delete_lengua_indigena'),

    path('medio_contacto/add/', MedioContactoAdd.as_view(), name='add_medio_contacto'),
    path('medio_contacto/list/', views.list_medio_contacto, name='list_medio_contacto'),
    path('medio_contacto/ajax/list/', MedioContactoAjaxList.as_view(), name='list_ajax_medio_contacto'),
    path('medio_contacto/edit/<int:pk>', MedioContactoEdit.as_view(), name='edit_medio_contacto'),
    path('medio_contacto/list/delete/<int:pk>', views.delete_medio_contacto, name='delete_medio_contacto'),

    path('modalidad_violencia/add/', ModalidadViolenciaAdd.as_view(), name='add_modalidad_violencia'),
    path('modalidad_violencia/list/', views.list_modalidad_violencia, name='list_modalidad_violencia'),
    path('modalidad_violencia/ajax/list/', ModalidadViolenciaAjaxList.as_view(), name='list_ajax_modalidad_violencia'),
    path('modalidad_violencia/edit/<int:pk>', ModalidadViolenciaEdit.as_view(), name='edit_modalidad_violencia'),
    path('modalidad_violencia/list/delete/<int:pk>', views.delete_modalidad_violencia, name='delete_modalidad_violencia'),

    path('municipio/add/', MunicipioAdd.as_view(), name='add_municipio'),
    path('municipio/list/', views.list_municipio, name='list_municipio'),
    path('municipio/ajax/list/', MunicipioAjaxList.as_view(), name='list_ajax_municipio'),
    path('municipio/edit/<int:pk>', MunicipioEdit.as_view(), name='edit_municipio'),
    path('municipio/list/delete/<int:pk>', views.delete_municipio, name='delete_municipio'),

    path('nivel_estudio/add/', NivelEstudioAdd.as_view(), name='add_nivel_estudio'),
    path('nivel_estudio/list/', views.list_nivel_estudio, name='list_nivel_estudio'),
    path('nivel_estudio/ajax/list/', NivelEstudioAjaxList.as_view(), name='list_ajax_nivel_estudio'),
    path('nivel_estudio/edit/<int:pk>', NivelEstudioEdit.as_view(), name='edit_nivel_estudio'),
    path('nivel_estudio/list/delete/<int:pk>', views.delete_nivel_estudio, name='delete_nivel_estudio'),

    path('nivel_violencia/add/', NivelViolenciaAdd.as_view(), name='add_nivel_violencia'),
    path('nivel_violencia/list/', views.list_nivel_violencia, name='list_nivel_violencia'),
    path('nivel_violencia/ajax/list/', NivelViolenciaAjaxList.as_view(), name='list_ajax_nivel_violencia'),
    path('nivel_violencia/edit/<int:pk>', NivelViolenciaEdit.as_view(), name='edit_nivel_violencia'),
    path('nivel_violencia/list/delete/<int:pk>', views.delete_nivel_violencia, name='delete_nivel_violencia'),

    path('ocupacion/add/', OcupacionAdd.as_view(), name='add_ocupacion'),
    path('ocupacion/list/', views.list_ocupacion, name='list_ocupacion'),
    path('ocupacion/ajax/list/', OcupacionAjaxList.as_view(), name='list_ajax_ocupacion'),
    path('ocupacion/edit/<int:pk>', OcupacionEdit.as_view(), name='edit_ocupacion'),
    path('ocupacion/list/delete/<int:pk>', views.delete_ocupacion, name='delete_ocupacion'),

    path('religion/add/', ReligionAdd.as_view(), name='add_religion'),
    path('religion/list/', views.list_religion, name='list_religion'),
    path('religion/ajax/list/', ReligionAjaxList.as_view(), name='list_ajax_religion'),
    path('religion/edit/<int:pk>', ReligionEdit.as_view(), name='edit_religion'),
    path('religion/list/delete/<int:pk>', views.delete_religion, name='delete_religion'),

    path('tipo_caso/add/', TipoCasoAdd.as_view(), name='add_tipo_caso'),
    path('tipo_caso/list/', views.list_tipo_caso, name='list_tipo_caso'),
    path('tipo_caso/ajax/list/', TipoCasoAjaxList.as_view(), name='list_ajax_tipo_caso'),
    path('tipo_caso/edit/<int:pk>', TipoCasoEdit.as_view(), name='edit_tipo_caso'),
    path('tipo_caso/list/delete/<int:pk>', views.delete_tipo_caso, name='delete_tipo_caso'),

    path('tipo_violencia/add/', TipoViolenciaAdd.as_view(), name='add_tipo_violencia'),
    path('tipo_violencia/list/', views.list_tipo_violencia, name='list_tipo_violencia'),
    path('tipo_violencia/ajax/list/', TipoViolenciaAjaxList.as_view(), name='list_ajax_tipo_violencia'),
    path('tipo_violencia/edit/<int:pk>', TipoViolenciaEdit.as_view(), name='edit_tipo_violencia'),
    path('tipo_violencia/list/delete/<int:pk>', views.delete_tipo_violencia, name='delete_tipo_violencia'),

    path('violentometro/add/', ViolentometroAdd.as_view(), name='add_violentometro'),
    path('violentometro/list/', views.list_violentometro, name='list_violentometro'),
    path('violentometro/ajax/list/', ViolentometroAjaxList.as_view(), name='list_ajax_violentometro'),
    path('violentometro/edit/<int:pk>', ViolentometroEdit.as_view(), name='edit_violentometro'),
    path('violentometro/list/delete/<int:pk>', views.delete_violentometro, name='delete_violentometro'),

    path('vive_con/add/', ViveConAdd.as_view(), name='add_vive_con'),
    path('vive_con/list/', views.list_vive_con, name='list_vive_con'),
    path('vive_con/ajax/list/', ViveConAjaxList.as_view(), name='list_ajax_vive_con'),
    path('vive_con/edit/<int:pk>', ViveConEdit.as_view(), name='edit_vive_con'),
    path('vive_con/list/delete/<int:pk>', views.delete_vive_con, name='delete_vive_con'),

    path('contacto_institucion/add/<int:institucion>', ContactoInstitucionAdd.as_view(), name='add_contacto_institucion'),
    path('contacto_institucion/list/<int:institucion>', views.list_contacto_institucion, name='list_contacto_institucion'),
    path('contacto_institucion/ajax/list/<int:institucion>', ContactoInstitucionAjaxList.as_view(), name='list_ajax_contacto_institucion'),
    path('contacto_institucion/edit/<int:pk>/<int:institucion>', ContactoInstitucionEdit.as_view(), name='edit_contacto_institucion'),
    path('contacto_institucion/list/delete/<int:pk>', views.delete_contacto_institucion, name='delete_contacto_institucion'),

    path('sexo/add/', SexoAdd.as_view(), name='add_sexo'),
    path('sexo/list/', views.list_sexo, name='list_sexo'),
    path('sexo/ajax/list/', SexoAjaxList.as_view(), name='list_ajax_sexo'),
    path('sexo/edit/<int:pk>', SexoEdit.as_view(), name='edit_sexo'),
    path('sexo/list/delete/<int:pk>', views.delete_sexo, name='delete_sexo'),

    path('ayuda/add/', AyudaAdd.as_view(), name='add_ayuda'),
    path('ayuda/list/', views.list_ayuda, name='list_ayuda'),
    path('ayuda/ajax/list/', AyudaAjaxList.as_view(), name='list_ajax_ayuda'),
    path('ayuda/edit/<int:pk>', AyudaEdit.as_view(), name='edit_ayuda'),
    path('ayuda/list/delete/<int:pk>', views.delete_ayuda, name='delete_ayuda'),

    path('motivo_llamada/add/', MotivoLLamadaAdd.as_view(), name='add_motivo_llamada'),
    path('motivo_llamada/list/', views.list_motivo_llamada, name='list_motivo_llamada'),
    path('motivo_llamada/ajax/list/', MotivoLLamadaAjaxList.as_view(), name='list_ajax_motivo_llamada'),
    path('motivo_llamada/edit/<int:pk>', MotivoLLamadaEdit.as_view(), name='edit_motivo_llamada'),
    path('motivo_llamada/list/delete/<int:pk>', views.delete_motivo_llamada, name='delete_motivo_llamada'),

    path('estatus_llamada/add/', EstatusLLamadaAdd.as_view(), name='add_estatus_llamada'),
    path('estatus_llamada/list/', views.list_estatus_llamada, name='list_estatus_llamada'),
    path('estatus_llamada/ajax/list/', EstatusLLamadaAjaxList.as_view(), name='list_ajax_estatus_llamada'),
    path('estatus_llamada/edit/<int:pk>', EstatusLLamadaEdit.as_view(), name='edit_estatus_llamada'),
    path('estatus_llamada/list/delete/<int:pk>', views.delete_estatus_llamada, name='delete_estatus_llamada'),
]
