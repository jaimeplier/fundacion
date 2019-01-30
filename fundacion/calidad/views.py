from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from calidad.forms import EvaluacionForm
from config.models import Evaluacion


class EvaluacionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'calidad'

    model = Evaluacion
    template_name = 'config/formulario_1Col.html'
    success_url = '/calidad/evaluacion/list'
    form_class = EvaluacionForm

    def get_context_data(self, **kwargs):
        context = super(EvaluacionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un evaluacion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='calidad', login_url='/')
def list_evaluacion(request):
    template_name = 'calidad/tab_evaluacion.html'
    return render(request, template_name)


class EvaluacionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'calidad'

    model = Evaluacion
    columns = ['id', 'nombre', 'valor', 'editar', 'eliminar']
    order_columns = ['id', 'nombre', 'valor']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('calidad:edit_evaluacion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(EvaluacionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Evaluacion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search) | qs.filter(valor__icontains=search)
        return qs


class EvaluacionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'calidad'
    success_url = '/calidad/evaluacion/list'

    model = Evaluacion
    template_name = 'config/formulario_1Col.html'
    form_class = EvaluacionForm

    def get_context_data(self, **kwargs):
        context = super(EvaluacionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='calidad', login_url='/')
def delete_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    evaluacion.delete()
    return JsonResponse({'result': 1})