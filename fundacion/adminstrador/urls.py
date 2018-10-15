from django.urls import path

from adminstrador.views import AcudeInstitucionAdd, AcudeInstitucionAjaxList, AcudeInstitucionEdit, EstadoAdd, \
    EstadoAjaxList, EstadoEdit, PaisAdd, PaisAjaxList, PaisEdit, EstadoCivilAdd, EstadoCivilAjaxList, EstadoCivilEdit, \
    EstatusAdd, EstatusAjaxList, EstatusEdit, LenguaIndigenaAdd, LenguaIndigenaAjaxList, LenguaIndigenaEdit, \
    MedioContactoAdd, MedioContactoAjaxList, MedioContactoEdit, ModalidadViolenciaAdd, ModalidadViolenciaAjaxList, \
    ModalidadViolenciaEdit
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
]
