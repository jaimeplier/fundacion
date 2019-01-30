from datetime import timedelta, datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from calidad.forms import EvaluacionForm
from config.models import Evaluacion, Llamada, TipificacionLLamada


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

@permission_required(perm='calidad', login_url='/')
def list_llamada(request):
    template_name = 'calidad/tab_llamada.html'
    return render(request, template_name)


class LlamadaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'calidad'

    model = Llamada
    columns = ['id', 'victima', 'consejero', 'hora_inicio', 'hora_fin', 'duracion_llamada', 'vida_en_riesgo',
               'tipificacion', 'medio_contacto', 'calificacion']
    order_columns = ['id', 'victima__nombre', 'consejero__a_paterno', 'hora_inicio', 'hora_fin', '', 'vida_en_riesgo',
                     'tipificacionllamada__categoria_tipificacion__nombre', 'medio_contacto__nombre', '']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'victima':
            return row.victima.nombre
        elif column == 'consejero':
            return row.consejero.get_full_name()
        elif column == 'id':
            return row.pk
        elif column == 'duracion_llamada':
            formato = '%H:%M:%S'
            h1 = str(row.hora_inicio.hour) + ':' + str(row.hora_inicio.minute) + ':' + str(row.hora_inicio.second)
            h2 = str(row.hora_fin.hour) + ':' + str(row.hora_fin.minute) + ':' + str(row.hora_fin.second)
            h1 = datetime.strptime(h1, formato)
            h2 = datetime.strptime(h2, formato)
            r= h2-h1
            return str(h2-h1)
        elif column == 'vida_en_riesgo':
            if row.vida_en_riesgo:
                return 'Sí'
            return 'No'
        elif column == 'tipificacion':
            tll = TipificacionLLamada.objects.get(llamada__pk=row.pk)
            return tll.categoria_tipificacion.tipificacion.nombre
        elif column == 'medio_contacto':
            if row.medio_contacto:
                return row.medio_contacto.nombre
            return 'Sin medio de contacto'
        elif column == 'calificacion':
            if row.calificada:
                return 'Sí'
            return 'No'

        return super(LlamadaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Llamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs