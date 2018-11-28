from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

# Create your views here.
@permission_required(perm='supervisor', login_url='/')
def reportes(request):
    template_name = 'administrador/tab_reportes.html'
    return render(request, template_name)


@permission_required(perm='supervisor', login_url='/')
def resumen(request):
    template_name = 'administrador/resumen.html'
    return render(request, template_name)
