from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView

from config.models import Victima, Consejero
from consejero.forms import VictimaForm


@permission_required(perm='consejero', login_url='/')
def busqueda_usuario(request):
    template_name = 'consejero/busqueda_usuario.html'
    return render(request, template_name)


@permission_required(perm='consejero', login_url='/')
def registro_primera_vez(request):
    template_name = 'consejero/formulario_primera.html'
    consejero = Consejero.objects.get(pk=request.user.pk)
    return render(request, template_name, {'consejero': consejero})

class SeguimientoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'consejero'
    success_url = '/consejero/seguimiento/list'

    model = Victima
    template_name = 'consejero/formulario_seguimiento.html'
    form_class = VictimaForm

    def get_context_data(self, **kwargs):
        context = super(SeguimientoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        if 'victima' not in context:
            context['victima'] = self.model.pk
        return context

    def get_success_url(self):
        return reverse('consejero:registro_seguimiento', kwargs={'pk': self.kwargs['pk']})
