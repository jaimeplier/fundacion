from django.urls import path

from webapp.views import PendienteAdd, PendienteAjaxList, PendienteEdit
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.index, name='index'),

    path('avisos/', views.avisos, name='avisos'),
    path('recados/', views.recados, name='recados'),

    path('ver_avisos/', views.ver_avisos, name='ver_avisos'),
    path('ver_recados/', views.ver_recados, name='ver_recados'),

    path('pendiente/add/', PendienteAdd.as_view(), name='add_pendiente'),
    path('pendiente/list/', views.list_pendiente, name='list_pendiente'),
    path('pendiente/ajax/list/', PendienteAjaxList.as_view(), name='list_ajax_pendiente'),
    path('pendiente/edit/<int:pk>', PendienteEdit.as_view(), name='edit_pendiente'),
    path('pendiente/list/delete/<int:pk>', views.delete_pendiente, name='delete_pendiente'),


]
