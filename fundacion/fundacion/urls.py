"""fundacion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

from fundacion import settings

urlpatterns = [
    path('docs/', include_docs_urls(title='Fundacion', public=True)),
    path('admin/', admin.site.urls),
    path('administrador/', include('adminstrador.urls')),
    path('supervisor/', include('supervisor.urls')),
    path('directorio/', include('directorio.urls')),
    path('consejero/', include('consejero.urls')),
    path('calidad/', include('calidad.urls')),
    path('', include('webapp.urls')),
    path('ws/', include('webservices.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)