from django.urls import path

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

]
