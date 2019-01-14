from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


@permission_required(perm='consejero', login_url='/')
def busqueda_usuario(request):
    template_name = 'consejero/busqueda_usuario.html'
    return render(request, template_name)


@permission_required(perm='consejero', login_url='/')
def registro_primera_vez(request):
    template_name = 'consejero/formulario_primera.html'
    return render(request, template_name)


@permission_required(perm='consejero', login_url='/')
def registro_seguimiento(request):
    template_name = 'consejero/formulario_seguimiento.html'
    return render(request, template_name)
