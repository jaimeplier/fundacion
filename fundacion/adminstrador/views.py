from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from adminstrador.forms import AcudeInstitucionForm, EstadoForm, PaisForm, EstadoCivilForm, EstatusForm, \
    LenguaIndigenaForm, MedioContactoForm, ModalidadViolenciaForm, MunicipioForm, NivelEstudioForm, NivelViolenciaForm
from config.models import AcudeInstitucion, Estado, Pais, EstadoCivil, Estatus, LenguaIndigena, MedioContacto, \
    ModalidadViolencia, Municipio, NivelEstudio, NivelViolencia


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

class PaisAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_pais'

    model = Pais
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/pais/list'
    form_class = PaisForm

    def get_context_data(self, **kwargs):
        context = super(PaisAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un pais'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_pais', login_url='/login/')
def list_pais(request):
    template_name = 'administrador/tab_pais.html'
    return render(request, template_name)


class PaisAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_pais'

    model = Pais
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_pais',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(PaisAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Pais.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class PaisEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_pais'
    success_url = '/administrador/pais/list'

    model = Pais
    template_name = 'config/formulario_1Col.html'
    form_class = PaisForm

    def get_context_data(self, **kwargs):
        context = super(PaisEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_pais', login_url='/login/')
def delete_pais(request, pk):
    pais = get_object_or_404(Pais, pk=pk)
    pais.delete()
    return JsonResponse({'result': 1})

class EstadoCivilAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_estado_civil'

    model = EstadoCivil
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/estado_civil/list'
    form_class = EstadoCivilForm

    def get_context_data(self, **kwargs):
        context = super(EstadoCivilAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un estado_civil'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_estado_civil', login_url='/login/')
def list_estado_civil(request):
    template_name = 'administrador/tab_estado_civil.html'
    return render(request, template_name)


class EstadoCivilAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_estado_civil'

    model = EstadoCivil
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_estado_civil',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(EstadoCivilAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return EstadoCivil.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class EstadoCivilEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_estado_civil'
    success_url = '/administrador/estado_civil/list'

    model = EstadoCivil
    template_name = 'config/formulario_1Col.html'
    form_class = EstadoCivilForm

    def get_context_data(self, **kwargs):
        context = super(EstadoCivilEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_estado_civil', login_url='/login/')
def delete_estado_civil(request, pk):
    estado_civil = get_object_or_404(EstadoCivil, pk=pk)
    estado_civil.delete()
    return JsonResponse({'result': 1})

class EstatusAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_estatus'

    model = Estatus
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/estatus/list'
    form_class = EstatusForm

    def get_context_data(self, **kwargs):
        context = super(EstatusAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un estatus'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_estatus', login_url='/login/')
def list_estatus(request):
    template_name = 'administrador/tab_estatus.html'
    return render(request, template_name)


class EstatusAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_estatus'

    model = Estatus
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_estatus',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(EstatusAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Estatus.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class EstatusEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_estatus'
    success_url = '/administrador/estatus/list'

    model = Estatus
    template_name = 'config/formulario_1Col.html'
    form_class = EstatusForm

    def get_context_data(self, **kwargs):
        context = super(EstatusEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_estatus', login_url='/login/')
def delete_estatus(request, pk):
    estatus = get_object_or_404(Estatus, pk=pk)
    estatus.delete()
    return JsonResponse({'result': 1})


class LenguaIndigenaAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_lengua_indigena'

    model = LenguaIndigena
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/lengua_indigena/list'
    form_class = LenguaIndigenaForm

    def get_context_data(self, **kwargs):
        context = super(LenguaIndigenaAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un lengua_indigena'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_lengua_indigena', login_url='/login/')
def list_lengua_indigena(request):
    template_name = 'administrador/tab_lengua_indigena.html'
    return render(request, template_name)


class LenguaIndigenaAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_lengua_indigena'

    model = LenguaIndigena
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_lengua_indigena',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(LenguaIndigenaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return LenguaIndigena.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class LenguaIndigenaEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_lengua_indigena'
    success_url = '/administrador/lengua_indigena/list'

    model = LenguaIndigena
    template_name = 'config/formulario_1Col.html'
    form_class = LenguaIndigenaForm

    def get_context_data(self, **kwargs):
        context = super(LenguaIndigenaEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_lengua_indigena', login_url='/login/')
def delete_lengua_indigena(request, pk):
    lengua_indigena = get_object_or_404(LenguaIndigena, pk=pk)
    lengua_indigena.delete()
    return JsonResponse({'result': 1})


class MedioContactoAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_medio_contacto'

    model = MedioContacto
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/medio_contacto/list'
    form_class = MedioContactoForm

    def get_context_data(self, **kwargs):
        context = super(MedioContactoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un medio_contacto'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_medio_contacto', login_url='/login/')
def list_medio_contacto(request):
    template_name = 'administrador/tab_medio_contacto.html'
    return render(request, template_name)


class MedioContactoAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_medio_contacto'

    model = MedioContacto
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_medio_contacto',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(MedioContactoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return MedioContacto.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class MedioContactoEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_medio_contacto'
    success_url = '/administrador/medio_contacto/list'

    model = MedioContacto
    template_name = 'config/formulario_1Col.html'
    form_class = MedioContactoForm

    def get_context_data(self, **kwargs):
        context = super(MedioContactoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_medio_contacto', login_url='/login/')
def delete_medio_contacto(request, pk):
    medio_contacto = get_object_or_404(MedioContacto, pk=pk)
    medio_contacto.delete()
    return JsonResponse({'result': 1})

class ModalidadViolenciaAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_modalidad_violencia'

    model = ModalidadViolencia
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/modalidad_violencia/list'
    form_class = ModalidadViolenciaForm

    def get_context_data(self, **kwargs):
        context = super(ModalidadViolenciaAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un modalidad_violencia'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_modalidad_violencia', login_url='/login/')
def list_modalidad_violencia(request):
    template_name = 'administrador/tab_modalidad_violencia.html'
    return render(request, template_name)


class ModalidadViolenciaAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_modalidad_violencia'

    model = ModalidadViolencia
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_modalidad_violencia',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(ModalidadViolenciaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return ModalidadViolencia.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ModalidadViolenciaEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_modalidad_violencia'
    success_url = '/administrador/modalidad_violencia/list'

    model = ModalidadViolencia
    template_name = 'config/formulario_1Col.html'
    form_class = ModalidadViolenciaForm

    def get_context_data(self, **kwargs):
        context = super(ModalidadViolenciaEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_modalidad_violencia', login_url='/login/')
def delete_modalidad_violencia(request, pk):
    modalidad_violencia = get_object_or_404(ModalidadViolencia, pk=pk)
    modalidad_violencia.delete()
    return JsonResponse({'result': 1})

class MunicipioAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_municipio'

    model = Municipio
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/municipio/list'
    form_class = MunicipioForm

    def get_context_data(self, **kwargs):
        context = super(MunicipioAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un municipio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_municipio', login_url='/login/')
def list_municipio(request):
    template_name = 'administrador/tab_municipio.html'
    return render(request, template_name)


class MunicipioAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_municipio'

    model = Municipio
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_municipio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(MunicipioAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Municipio.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class MunicipioEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_municipio'
    success_url = '/administrador/municipio/list'

    model = Municipio
    template_name = 'config/formulario_1Col.html'
    form_class = MunicipioForm

    def get_context_data(self, **kwargs):
        context = super(MunicipioEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_municipio', login_url='/login/')
def delete_municipio(request, pk):
    municipio = get_object_or_404(Municipio, pk=pk)
    municipio.delete()
    return JsonResponse({'result': 1})

class NivelEstudioAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_nivel_estudio'

    model = NivelEstudio
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/nivel_estudio/list'
    form_class = NivelEstudioForm

    def get_context_data(self, **kwargs):
        context = super(NivelEstudioAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un nivel_estudio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_nivel_estudio', login_url='/login/')
def list_nivel_estudio(request):
    template_name = 'administrador/tab_nivel_estudio.html'
    return render(request, template_name)


class NivelEstudioAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_nivel_estudio'

    model = NivelEstudio
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_nivel_estudio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(NivelEstudioAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return NivelEstudio.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class NivelEstudioEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_nivel_estudio'
    success_url = '/administrador/nivel_estudio/list'

    model = NivelEstudio
    template_name = 'config/formulario_1Col.html'
    form_class = NivelEstudioForm

    def get_context_data(self, **kwargs):
        context = super(NivelEstudioEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_nivel_estudio', login_url='/login/')
def delete_nivel_estudio(request, pk):
    nivel_estudio = get_object_or_404(NivelEstudio, pk=pk)
    nivel_estudio.delete()
    return JsonResponse({'result': 1})

class NivelViolenciaAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_nivel_violencia'

    model = NivelViolencia
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/nivel_violencia/list'
    form_class = NivelViolenciaForm

    def get_context_data(self, **kwargs):
        context = super(NivelViolenciaAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un nivel_violencia'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


#@permission_required(perm='change_nivel_violencia', login_url='/login/')
def list_nivel_violencia(request):
    template_name = 'administrador/tab_nivel_violencia.html'
    return render(request, template_name)


class NivelViolenciaAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_nivel_violencia'

    model = NivelViolencia
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_nivel_violencia',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><i class="material-icons">edit</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><i class="material-icons">delete_forever</i></a>'
        elif column == 'id':
            return row.pk

        return super(NivelViolenciaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return NivelViolencia.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class NivelViolenciaEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_nivel_violencia'
    success_url = '/administrador/nivel_violencia/list'

    model = NivelViolencia
    template_name = 'config/formulario_1Col.html'
    form_class = NivelViolenciaForm

    def get_context_data(self, **kwargs):
        context = super(NivelViolenciaEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


#@permission_required(perm='delete_nivel_violencia', login_url='/login/')
def delete_nivel_violencia(request, pk):
    nivel_violencia = get_object_or_404(NivelViolencia, pk=pk)
    nivel_violencia.delete()
    return JsonResponse({'result': 1})