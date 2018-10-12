from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from adminstrador.forms import AcudeInstitucionForm, EstadoForm
from config.models import AcudeInstitucion, Estado


class AcudeInstitucionAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_acude_institucion'

    model = AcudeInstitucion
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/acude_institucion/list'
    form_class = AcudeInstitucionForm

    def get_context_data(self, **kwargs):
        context = super(AcudeInstitucionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar institucion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_acude_institucion', login_url='/login/')
def list_acude_institucion(request):
    template_name = 'administrador/tab_acude_institucion.html'
    return render(request, template_name)


class AcudeInstitucionAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_acude_institucion'

    model = AcudeInstitucion
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_acude_institucion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(AcudeInstitucionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return AcudeInstitucion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class AcudeInstitucionEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_acude_institucion'
    success_url = '/administrador/acude_institucion/list'

    model = AcudeInstitucion
    template_name = 'config/formulario_1Col.html'
    form_class = AcudeInstitucionForm

    def get_context_data(self, **kwargs):
        context = super(AcudeInstitucionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_acude_institucion', login_url='/login/')
def delete_acude_institucion(request, pk):
    acude_institucion = get_object_or_404(AcudeInstitucion, pk=pk)
    acude_institucion.delete()
    return JsonResponse({'result': 1})


class EstadoAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_estado'

    model = Estado
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/estado/list'
    form_class = EstadoForm

    def get_context_data(self, **kwargs):
        context = super(EstadoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un estado'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_estado', login_url='/login/')
def list_estado(request):
    template_name = 'administrador/tab_estado.html'
    return render(request, template_name)


class EstadoAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_estado'

    model = Estado
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_estado',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(EstadoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Estado.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class EstadoEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_estado'
    success_url = '/administrador/estado/list'

    model = Estado
    template_name = 'config/formulario_1Col.html'
    form_class = EstadoForm

    def get_context_data(self, **kwargs):
        context = super(EstadoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_estado', login_url='/login/')
def delete_estado(request, pk):
    estado = get_object_or_404(Estado, pk=pk)
    estado.delete()
    return JsonResponse({'result': 1})