from django.urls import path

from directorio.views import AcudeInstitucionAdd, AcudeInstitucionAjaxList, AcudeInstitucionEdit, \
    ContactoInstitucionAdd, ContactoInstitucionAjaxList, ContactoInstitucionEdit
from . import views

app_name = 'directorio'

urlpatterns = [

    path('acude_institucion/add/', AcudeInstitucionAdd.as_view(), name='add_acude_institucion'),
    path('acude_institucion/list/', views.list_acude_institucion, name='list_acude_institucion'),
    path('acude_institucion/ajax/list/', AcudeInstitucionAjaxList.as_view(), name='list_ajax_acude_institucion'),
    path('acude_institucion/edit/<int:pk>', AcudeInstitucionEdit.as_view(), name='edit_acude_institucion'),
    path('acude_institucion/list/delete/<int:pk>', views.delete_acude_institucion, name='delete_acude_institucion'),

    path('contacto_institucion/add/<int:institucion>', ContactoInstitucionAdd.as_view(), name='add_contacto_institucion'),
    path('contacto_institucion/list/<int:institucion>', views.list_contacto_institucion, name='list_contacto_institucion'),
    path('contacto_institucion/ajax/list/<int:institucion>', ContactoInstitucionAjaxList.as_view(), name='list_ajax_contacto_institucion'),
    path('contacto_institucion/edit/<int:pk>/<int:institucion>', ContactoInstitucionEdit.as_view(), name='edit_contacto_institucion'),
    path('contacto_institucion/list/delete/<int:pk>', views.delete_contacto_institucion, name='delete_contacto_institucion'),
]
