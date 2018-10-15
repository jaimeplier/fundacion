from django.urls import path

from adminstrador.views import AcudeInstitucionAdd, AcudeInstitucionAjaxList, AcudeInstitucionEdit, EstadoAdd, \
    EstadoAjaxList, EstadoEdit, PaisAdd, PaisAjaxList, PaisEdit, EstadoCivilAdd, EstadoCivilAjaxList, EstadoCivilEdit, \
    EstatusAdd, EstatusAjaxList, EstatusEdit, LenguaIndigenaAdd, LenguaIndigenaAjaxList, LenguaIndigenaEdit, \
    MedioContactoAdd, MedioContactoAjaxList, MedioContactoEdit, ModalidadViolenciaAdd, ModalidadViolenciaAjaxList, \
    ModalidadViolenciaEdit, MunicipioAdd, MunicipioAjaxList, MunicipioEdit, NivelEstudioAdd, NivelEstudioAjaxList, \
    NivelEstudioEdit, NivelViolenciaAdd, NivelViolenciaAjaxList, NivelViolenciaEdit, OcupacionAdd, OcupacionAjaxList, \
    OcupacionEdit, ReligionAdd, ReligionAjaxList, ReligionEdit, TipoCasoAdd, TipoCasoAjaxList, TipoCasoEdit
from . import views

app_name = 'administrador'

urlpatterns = [
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
]
