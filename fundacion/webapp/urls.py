from django.urls import path

from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.index, name='index'),

]
