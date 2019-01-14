from django.urls import path

from . import views

app_name = 'consejero'

urlpatterns = [

    path('busqueda_usuario/', views.busqueda_usuario, name='busqueda_usuario'),
    path('registro_primera_vez/', views.registro_primera_vez, name='registro_primera_vez'),
    path('registro_seguimiento/', views.registro_seguimiento, name='registro_seguimiento'),
    ]