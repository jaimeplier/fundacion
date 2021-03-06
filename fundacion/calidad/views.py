from datetime import timedelta, datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.html import linebreaks
from django.views.generic import CreateView, UpdateView,DetailView
from django_datatables_view.base_datatable_view import BaseDatatableView

from calidad.forms import EvaluacionForm
from config.models import Evaluacion, Llamada, TipificacionLLamada, CalificacionLlamada, VictimaMenorEdad, \
    ExamenMentalLLamada, LlamadaCanalizacion


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
        if 'rutas' not in context:
            rutas = [{'nombre': 'menu', 'url': reverse('calidad:list_evaluacion')},
                     {'nombre': 'Rubros de evaluación', 'url': reverse('calidad:list_evaluacion')}]
            context['rutas']= rutas
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un rubro de evaluación'
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
    columns = ['id', 'nombre', 'comentario', 'editar', 'eliminar']
    order_columns = ['id', 'nombre', 'comentario']
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
        elif column == 'comentario':
            if row.comentario:
                a = linebreaks(row.comentario)
                return linebreaks(row.comentario)
            return 'Sin comentarios'

        return super(EvaluacionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Evaluacion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)| qs.filter(comentario__icontains=search)
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
        if 'rutas' not in context:
            rutas = [{'nombre': 'menu', 'url': reverse('calidad:list_evaluacion')},
                     {'nombre': 'Rubros de evaluación', 'url': reverse('calidad:list_evaluacion')}]
            context['rutas']= rutas
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
            return str(h2-h1)
        elif column == 'vida_en_riesgo':
            if row.vida_en_riesgo:
                return 'Sí'
            return 'No'
        elif column == 'tipificacion':
            try:
                tll = TipificacionLLamada.objects.get(llamada__pk=row.pk)
                return tll.categoria_tipificacion.tipificacion.nombre
            except:
                return "Sin tipificación"
        elif column == 'medio_contacto':
            if row.medio_contacto:
                return row.medio_contacto.nombre
            return 'Sin medio de contacto'
        elif column == 'calificacion':
            if row.calificacion is not None:
                return '<a href="'+ reverse('calidad:ver_servicio', kwargs={'pk': row.pk})+'">' + "{0:,.2f}".format(row.calificacion) + '</a>'
            return '<a href="'+ reverse('calidad:calificar_servicio', kwargs={'pk': row.pk}) + '">Calificar</a>'

        return super(LlamadaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Llamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs

class CalificarServicio(PermissionRequiredMixin, DetailView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'calidad'
    model = Llamada
    template_name = 'calidad/calificar_servicio.html'

    def get_context_data(self, **kwargs):
        context = super(CalificarServicio, self).get_context_data(**kwargs)
        servicio = Llamada.objects.get(pk=self.kwargs['pk'])
        victimas_menores = VictimaMenorEdad.objects.filter(llamada=servicio)
        tipificacion = TipificacionLLamada.objects.filter(llamada=servicio).first()
        examen_mental = ExamenMentalLLamada.objects.filter(llamada=servicio)
        canalizaciones = LlamadaCanalizacion.objects.filter(llamada=servicio)
        rubros = Evaluacion.objects.all()
        evaluacion = CalificacionLlamada.objects.filter(llamada=servicio)
        context['servicio'] = servicio
        context['tipificacion'] = tipificacion
        context['rubros'] = rubros
        context['tareas'] = servicio.tareas.all()
        context['evaluaciones'] = evaluacion
        context['victimas_menores'] = victimas_menores
        context['examen_mental'] = examen_mental
        context['canalizaciones'] = canalizaciones
        return context

class VerServicio(PermissionRequiredMixin, DetailView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'calidad'
    model = Llamada
    template_name = 'calidad/ver_servicio.html'

    def get_context_data(self, **kwargs):
        context = super(VerServicio, self).get_context_data(**kwargs)
        servicio = Llamada.objects.get(pk=self.kwargs['pk'])
        victimas_menores = VictimaMenorEdad.objects.filter(llamada=servicio)
        tipificacion = TipificacionLLamada.objects.filter(llamada=servicio).first()
        examen_mental = ExamenMentalLLamada.objects.filter(llamada=servicio)
        canalizaciones = LlamadaCanalizacion.objects.filter(llamada=servicio)
        rubros = Evaluacion.objects.all()
        evaluacion = CalificacionLlamada.objects.filter(llamada=servicio)
        context['servicio'] = servicio
        context['tipificacion'] = tipificacion
        context['rubros'] = rubros
        context['tareas'] = servicio.tareas.all()
        context['evaluaciones'] = evaluacion
        context['victimas_menores'] = victimas_menores
        context['examen_mental'] = examen_mental
        context['canalizaciones'] = canalizaciones
        return context

@permission_required(perm='calidad', login_url='/')
def list_evaluacion_rubro(request):
    template_name = 'calidad/tab_evaluacion_rubro.html'
    return render(request, template_name)


class EvaluacionRubroAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'calidad'

    model = CalificacionLlamada
    columns = ['nombre', 'estatus_true', 'estatus_false', 'total_estatus']
    order_columns = ['rubro__nombre', 'estatus_true', 'estatus_false', 'total_estatus']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'nombre':
            return row['rubro__nombre']
        elif column == 'estatus_true':
            return row['estatus_true']
        elif column == 'estatus_false':
            return row['estatus_false']
        elif column == 'total_estatus':
            return row['total_estatus']

        return super(EvaluacionRubroAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return CalificacionLlamada.objects.values('rubro__nombre').annotate(
            estatus_true=Count('estatus_rubro',filter=Q(estatus_rubro=True))).annotate(
            estatus_false=Count('estatus_rubro',filter=Q(estatus_rubro=False))).annotate(
            total_estatus=Count('estatus_rubro'))

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(rubro__nombre__icontains=search)
        return qs
