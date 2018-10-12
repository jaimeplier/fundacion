from django.urls import path

from adminstrador.views import AcudeInstitucionAdd, AcudeInstitucionAjaxList, AcudeInstitucionEdit, EstadoAdd, \
    EstadoAjaxList, EstadoEdit
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
]
