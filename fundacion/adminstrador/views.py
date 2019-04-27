from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.gis.geos import Point
from django.contrib.auth.models import Permission
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from adminstrador.forms import AcudeInstitucionForm, EstadoForm, PaisForm, EstadoCivilForm, EstatusForm, \
    LenguaIndigenaForm, MedioContactoForm, ModalidadViolenciaForm, MunicipioForm, NivelEstudioForm, NivelViolenciaForm, \
    OcupacionForm, ReligionForm, TipoViolenciaForm, ViolentometroForm, ViveConForm, ConsejeroForm, \
    DirectorioForm, SupervisorForm, ContactoInstitucionForm, CalidadForm, SexoForm, MotivoLLamadaForm, \
    DependenciaForm, RedesApoyoForm, VictimaInvolucradaForm, \
    AgresorForm, ComoSeEnteroForm, EstadoMentalForm, NivelRiesgoForm, RecomendacionRiesgoForm, \
    FaseCambioForm, ActividadUsuarioForm, TipificacionForm, CategoriaTipificacionForm, SucursalInstitucionForm, \
    AliadoForm, LineaNegocioForm, SubcategoriaTipificacionForm
from config.models import AcudeInstitucion, Estado, Pais, EstadoCivil, Estatus, LenguaIndigena, MedioContacto, \
    ModalidadViolencia, Municipio, NivelEstudio, NivelViolencia, Ocupacion, Religion, TipoViolencia, \
    Violentometro, ViveCon, ContactoInstitucion, Consejero, Rol, Directorio, Supervisor, Calidad, Llamada, Sexo, \
    MotivoLLamada, Dependencia, RedesApoyo, VictimaInvolucrada, Agresor, \
    ComoSeEntero, EstadoMental, NivelRiesgo, RecomendacionRiesgo, FaseCambio, EstatusUsuario, Tipificacion, \
    CategoriaTipificacion, Sucursal, EstatusInstitucion, Aliado, LineaNegocio, SubcategoriaTipificacion


@permission_required(perm='administrador', login_url='/')
def reportes(request):
    template_name = 'administrador/tab_reportes.html'
    return render(request, template_name)


class LlamadaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Llamada
    columns = ['id', 'victima.nombre', 'nombre', 'hora_inicio', 'hora_fin', 'duracion_llamada',
               'vida_en_riesgo', 'tipo_violencia', 'institucion', 'estatus', 'medio_contacto']
    order_columns = ['id', 'victima__nombre', 'consejero.a_paterno', 'hora_inicio', 'hora_fin', '', 'vida_en_riesgo',
                     'tipo_violencia', 'estatus', 'institucion__nombre', 'estatus__nombre', 'medio_contacto']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'id':
            return row.pk
        elif column == 'nombre':
            return  row.consejero.get_full_name()
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

        return super(LlamadaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Llamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


@permission_required(perm='administrador', login_url='/')
def resumen(request):
    template_name = 'administrador/resumen.html'
    return render(request, template_name)


@permission_required(perm='catalogo', login_url='/')
def catalogos(request):
    template_name = 'administrador/catalogos.html'
    return render(request, template_name)


class ConsejeroAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Consejero
    template_name = 'config/formulario_1Col.html'
    form_class = ConsejeroForm

    def get_context_data(self, **kwargs):
        context = super(ConsejeroAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un consejero'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un consejero'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            rol = Rol.objects.get(pk=3)
            user.rol = rol
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_consejero')


@permission_required(perm='administrador', login_url='/')
def list_consejero(request):
    template_name = 'administrador/tab_consejero.html'
    return render(request, template_name)


class ConsejeroAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Consejero
    columns = ['id', 'nombre', 'correo', 'editar', 'eliminar']
    order_columns = ['id', 'a_paterno', 'correo']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_consejero',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"> </a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(ConsejeroAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Consejero.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search) | qs.filter(a_paterno__icontains=search) | qs.filter(
                a_materno__icontains=search)
        return qs


class ConsejeroEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'
    success_url = '/administrador/consejero/list'

    model = Consejero
    template_name = 'config/formulario_1Col.html'
    form_class = ConsejeroForm

    def get_context_data(self, **kwargs):
        context = super(ConsejeroEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = Consejero.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_consejero')


@permission_required(perm='administrador', login_url='/')
def delete_consejero(request, pk):
    consejero = get_object_or_404(Consejero, pk=pk)
    consejero.delete()
    return JsonResponse({'result': 1})


class DirectorioAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Directorio
    template_name = 'config/formulario_1Col.html'
    form_class = DirectorioForm

    def get_context_data(self, **kwargs):
        context = super(DirectorioAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar a alguien del directorio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un personal del directorio'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            rol = Rol.objects.get(pk=5)
            user.rol = rol
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_directorio')


@permission_required(perm='administrador', login_url='/')
def list_directorio(request):
    template_name = 'administrador/tab_directorio.html'
    return render(request, template_name)


class DirectorioAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Directorio
    columns = ['id', 'nombre', 'correo', 'editar', 'eliminar']
    order_columns = ['id', 'a_paterno', 'correo']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_directorio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(DirectorioAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        permiso = Permission.objects.get(codename='directorio')
        return Directorio.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search) | qs.filter(a_paterno__icontains=search) | qs.filter(
                a_materno__icontains=search)
        return qs


class DirectorioEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'
    success_url = '/administrador/directorio/list'

    model = Directorio
    template_name = 'config/formulario_1Col.html'
    form_class = DirectorioForm

    def get_context_data(self, **kwargs):
        context = super(DirectorioEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = Directorio.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_directorio')


@permission_required(perm='administrador', login_url='/')
def delete_directorio(request, pk):
    directorio = get_object_or_404(Directorio, pk=pk)
    directorio.delete()
    return JsonResponse({'result': 1})


class SupervisorAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Supervisor
    template_name = 'config/formulario_1Col.html'
    form_class = SupervisorForm

    def get_context_data(self, **kwargs):
        context = super(SupervisorAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar supervisor'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un supervisor'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            rol = Rol.objects.get(pk=4)
            user.rol = rol
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_supervisor')


@permission_required(perm='administrador', login_url='/')
def list_supervisor(request):
    template_name = 'administrador/tab_supervisor.html'
    return render(request, template_name)


class SupervisorAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Supervisor
    columns = ['id', 'nombre', 'correo', 'editar', 'eliminar']
    order_columns = ['id', 'a_paterno', 'correo']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_supervisor',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(SupervisorAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Supervisor.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search) | qs.filter(a_paterno__icontains=search) | qs.filter(
                a_materno__icontains=search)
        return qs


class SupervisorEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'
    success_url = '/administrador/supervisor/list'

    model = Supervisor
    template_name = 'config/formulario_1Col.html'
    form_class = SupervisorForm

    def get_context_data(self, **kwargs):
        context = super(SupervisorEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = Supervisor.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_supervisor')


@permission_required(perm='administrador', login_url='/')
def delete_supervisor(request, pk):
    supervisor = get_object_or_404(Supervisor, pk=pk)
    supervisor.delete()
    return JsonResponse({'result': 1})


class CalidadAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Calidad
    template_name = 'config/formulario_1Col.html'
    form_class = CalidadForm

    def get_context_data(self, **kwargs):
        context = super(CalidadAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar personal de calidad (QA)'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un personal de calidad'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            rol = Rol.objects.get(pk=6)
            user.rol = rol
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_calidad')


@permission_required(perm='administrador', login_url='/')
def list_calidad(request):
    template_name = 'administrador/tab_calidad.html'
    return render(request, template_name)


class CalidadAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'

    model = Calidad
    columns = ['id', 'nombre', 'correo', 'editar', 'eliminar']
    order_columns = ['id', 'a_paterno', 'correo']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_calidad',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(CalidadAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Calidad.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(id__icontains=search) | qs.filter(
                correo__icontains=search) | qs.filter(a_paterno__icontains=search) | qs.filter(
                a_materno__icontains=search)
        return qs


class CalidadEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'administrador'
    success_url = '/administrador/calidad/list'

    model = Calidad
    template_name = 'config/formulario_1Col.html'
    form_class = CalidadForm

    def get_context_data(self, **kwargs):
        context = super(CalidadEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        usuario = Calidad.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_calidad')


@permission_required(perm='administrador', login_url='/')
def delete_calidad(request, pk):
    calidad = get_object_or_404(Calidad, pk=pk)
    calidad.delete()
    return JsonResponse({'result': 1})


class AcudeInstitucionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = AcudeInstitucion
    template_name = 'config/formMapa.html'
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        if form.is_valid():
            try:
                pnt = Point(float(lon), float(lat))
                form.instance.coordenadas = pnt

                institucion = form.save(commit=False)
                if self.request.user.rol.pk == 3:
                    estatus = EstatusInstitucion.objects.get(pk=2)
                    institucion.estatus_institucion = estatus
                    institucion.save()
                    return HttpResponseRedirect(self.get_success_url())
                estatus = EstatusInstitucion.objects.get(pk=1)
                institucion.estatus_institucion = estatus
                institucion.save()
                return HttpResponseRedirect(self.get_success_url())
            except:
                return render(request, template_name=self.template_name,
                              context={'form': form, 'error': 'Falta ubicación de la institución'})
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_acude_institucion')


@permission_required(perm='institucion', login_url='/')
def list_acude_institucion(request):
    template_name = 'administrador/tab_acude_institucion.html'
    return render(request, template_name)


class AcudeInstitucionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = AcudeInstitucion
    columns = ['id', 'nombre', 'estatus_institucion', 'sucursal', 'contacto', 'editar', 'eliminar']
    order_columns = ['id', 'nombre', 'estatus_institucion__nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            if self.request.user.is_consejero:
                return 'NA'
            return '<a class="" href ="' + reverse('administrador:edit_acude_institucion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'contacto':
            if self.request.user.is_consejero:
                return 'NA'
            return '<a class="" href ="' + reverse('administrador:list_contacto_institucion',
                                                   kwargs={
                                                       'institucion': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/usuario.png"></a>'
        elif column == 'sucursal':
            return '<a class="" href ="' + reverse('administrador:list_sucursal_institucion',
                                                   kwargs={
                                                       'institucion': row.pk}) + '"><i class="material-icons">account_balance</i></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'estatus_institucion':
            if self.request.user.is_consejero:
                return row.estatus_institucion.nombre
            select =  '<select onchange="cambiar_estatus_institucion(' + str(row.pk) + ', this)">'
            estatus = {'Válida': 1, 'Validando': 2, 'Cancelada': 3}
            for key,est in estatus.items():
                if est == row.estatus_institucion.pk:
                    select = select + '<option value="'+str(est)+'" selected>'+key+'</option>'
                else:
                    select = select + '<option value="' + str(est) + '">' + key + '</option>'
            select = select + '</select><script>$("select").material_select();</script>'
            return select
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


class AcudeInstitucionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'
    success_url = '/administrador/acude_institucion/list'

    model = AcudeInstitucion
    template_name = 'config/formMapa.html'
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')

        l = self.model.objects.get(pk=self.kwargs['pk'])
        form = AcudeInstitucionForm(request.POST, request.FILES, instance=l)
        if form.is_valid():
            try:
                pnt = Point(float(lon), float(lat))
                form.instance.coordenadas = pnt
                institucion = form.save()
                return HttpResponseRedirect(self.get_success_url())
            except:
                return render(request, template_name=self.template_name,
                              context={'form': form, 'error': 'Falta ubicación de la institución'})
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_acude_institucion')


@permission_required(perm='institucion', login_url='/')
def delete_acude_institucion(request, pk):
    acude_institucion = get_object_or_404(AcudeInstitucion, pk=pk)
    acude_institucion.delete()
    return JsonResponse({'result': 1})


class EstadoAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_estado(request):
    template_name = 'administrador/tab_estado.html'
    return render(request, template_name)


class EstadoAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Estado
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_estado',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class EstadoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_estado(request, pk):
    estado = get_object_or_404(Estado, pk=pk)
    estado.delete()
    return JsonResponse({'result': 1})


class PaisAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_pais(request):
    template_name = 'administrador/tab_pais.html'
    return render(request, template_name)


class PaisAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Pais
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_pais',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class PaisEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_pais(request, pk):
    pais = get_object_or_404(Pais, pk=pk)
    pais.delete()
    return JsonResponse({'result': 1})


class EstadoCivilAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_estado_civil(request):
    template_name = 'administrador/tab_estado_civil.html'
    return render(request, template_name)


class EstadoCivilAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = EstadoCivil
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_estado_civil',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class EstadoCivilEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_estado_civil(request, pk):
    estado_civil = get_object_or_404(EstadoCivil, pk=pk)
    estado_civil.delete()
    return JsonResponse({'result': 1})


class EstatusAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_estatus(request):
    template_name = 'administrador/tab_estatus.html'
    return render(request, template_name)


class EstatusAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Estatus
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_estatus',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class EstatusEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_estatus(request, pk):
    estatus = get_object_or_404(Estatus, pk=pk)
    estatus.delete()
    return JsonResponse({'result': 1})


class LenguaIndigenaAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_lengua_indigena(request):
    template_name = 'administrador/tab_lengua_indigena.html'
    return render(request, template_name)


class LenguaIndigenaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = LenguaIndigena
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_lengua_indigena',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class LenguaIndigenaEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_lengua_indigena(request, pk):
    lengua_indigena = get_object_or_404(LenguaIndigena, pk=pk)
    lengua_indigena.delete()
    return JsonResponse({'result': 1})


class MedioContactoAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_medio_contacto(request):
    template_name = 'administrador/tab_medio_contacto.html'
    return render(request, template_name)


class MedioContactoAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = MedioContacto
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_medio_contacto',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class MedioContactoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_medio_contacto(request, pk):
    medio_contacto = get_object_or_404(MedioContacto, pk=pk)
    medio_contacto.delete()
    return JsonResponse({'result': 1})


class ModalidadViolenciaAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_modalidad_violencia(request):
    template_name = 'administrador/tab_modalidad_violencia.html'
    return render(request, template_name)


class ModalidadViolenciaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = ModalidadViolencia
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_modalidad_violencia',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class ModalidadViolenciaEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_modalidad_violencia(request, pk):
    modalidad_violencia = get_object_or_404(ModalidadViolencia, pk=pk)
    modalidad_violencia.delete()
    return JsonResponse({'result': 1})


class MunicipioAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_municipio(request):
    template_name = 'administrador/tab_municipio.html'
    return render(request, template_name)


class MunicipioAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Municipio
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_municipio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class MunicipioEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_municipio(request, pk):
    municipio = get_object_or_404(Municipio, pk=pk)
    municipio.delete()
    return JsonResponse({'result': 1})


class NivelEstudioAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_nivel_estudio(request):
    template_name = 'administrador/tab_nivel_estudio.html'
    return render(request, template_name)


class NivelEstudioAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = NivelEstudio
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_nivel_estudio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class NivelEstudioEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_nivel_estudio(request, pk):
    nivel_estudio = get_object_or_404(NivelEstudio, pk=pk)
    nivel_estudio.delete()
    return JsonResponse({'result': 1})


class NivelViolenciaAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

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


@permission_required(perm='catalogo', login_url='/')
def list_nivel_violencia(request):
    template_name = 'administrador/tab_nivel_violencia.html'
    return render(request, template_name)


class NivelViolenciaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = NivelViolencia
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_nivel_violencia',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


class NivelViolenciaEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
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


@permission_required(perm='catalogo', login_url='/')
def delete_nivel_violencia(request, pk):
    nivel_violencia = get_object_or_404(NivelViolencia, pk=pk)
    nivel_violencia.delete()
    return JsonResponse({'result': 1})


class OcupacionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Ocupacion
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/ocupacion/list'
    form_class = OcupacionForm

    def get_context_data(self, **kwargs):
        context = super(OcupacionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un ocupacion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_ocupacion(request):
    template_name = 'administrador/tab_ocupacion.html'
    return render(request, template_name)


class OcupacionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Ocupacion
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_ocupacion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(OcupacionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Ocupacion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class OcupacionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/ocupacion/list'

    model = Ocupacion
    template_name = 'config/formulario_1Col.html'
    form_class = OcupacionForm

    def get_context_data(self, **kwargs):
        context = super(OcupacionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_ocupacion(request, pk):
    ocupacion = get_object_or_404(Ocupacion, pk=pk)
    ocupacion.delete()
    return JsonResponse({'result': 1})


class ReligionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Religion
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/religion/list'
    form_class = ReligionForm

    def get_context_data(self, **kwargs):
        context = super(ReligionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un religion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_religion(request):
    template_name = 'administrador/tab_religion.html'
    return render(request, template_name)


class ReligionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Religion
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_religion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png">></a>'
        elif column == 'id':
            return row.pk

        return super(ReligionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Religion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ReligionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/religion/list'

    model = Religion
    template_name = 'config/formulario_1Col.html'
    form_class = ReligionForm

    def get_context_data(self, **kwargs):
        context = super(ReligionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_religion(request, pk):
    religion = get_object_or_404(Religion, pk=pk)
    religion.delete()
    return JsonResponse({'result': 1})

class TipoViolenciaAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = TipoViolencia
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/tipo_violencia/list'
    form_class = TipoViolenciaForm

    def get_context_data(self, **kwargs):
        context = super(TipoViolenciaAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un tipo_violencia'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_tipo_violencia(request):
    template_name = 'administrador/tab_tipo_violencia.html'
    return render(request, template_name)


class TipoViolenciaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = TipoViolencia
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_tipo_violencia',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(TipoViolenciaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoViolencia.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class TipoViolenciaEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/tipo_violencia/list'

    model = TipoViolencia
    template_name = 'config/formulario_1Col.html'
    form_class = TipoViolenciaForm

    def get_context_data(self, **kwargs):
        context = super(TipoViolenciaEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_tipo_violencia(request, pk):
    tipo_violencia = get_object_or_404(TipoViolencia, pk=pk)
    tipo_violencia.delete()
    return JsonResponse({'result': 1})


class ViolentometroAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Violentometro
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/violentometro/list'
    form_class = ViolentometroForm

    def get_context_data(self, **kwargs):
        context = super(ViolentometroAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un violentometro'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_violentometro(request):
    template_name = 'administrador/tab_violentometro.html'
    return render(request, template_name)


class ViolentometroAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Violentometro
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_violentometro',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(ViolentometroAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Violentometro.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ViolentometroEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/violentometro/list'

    model = Violentometro
    template_name = 'config/formulario_1Col.html'
    form_class = ViolentometroForm

    def get_context_data(self, **kwargs):
        context = super(ViolentometroEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_violentometro(request, pk):
    violentometro = get_object_or_404(Violentometro, pk=pk)
    violentometro.delete()
    return JsonResponse({'result': 1})


class ViveConAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = ViveCon
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/vive_con/list'
    form_class = ViveConForm

    def get_context_data(self, **kwargs):
        context = super(ViveConAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un vive_con'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_vive_con(request):
    template_name = 'administrador/tab_vive_con.html'
    return render(request, template_name)


class ViveConAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = ViveCon
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_vive_con',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(ViveConAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return ViveCon.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ViveConEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/vive_con/list'

    model = ViveCon
    template_name = 'config/formulario_1Col.html'
    form_class = ViveConForm

    def get_context_data(self, **kwargs):
        context = super(ViveConEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_vive_con(request, pk):
    vive_con = get_object_or_404(ViveCon, pk=pk)
    vive_con.delete()
    return JsonResponse({'result': 1})


class ContactoInstitucionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = ContactoInstitucion
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/contacto_institucion/list'
    form_class = ContactoInstitucionForm

    def get_context_data(self, **kwargs):
        context = super(ContactoInstitucionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un contacto_institucion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        if 'save_and_new' not in context:
            context['save_and_new'] = 'Guardar y nuevo'

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():

            institucion = AcudeInstitucion.objects.get(pk=self.kwargs['institucion'])
            cont_institucion = form.save(commit=False)

            cont_institucion.institucion = institucion
            cont_institucion.save()
            if 'save_and_new' in form.data:
                return HttpResponseRedirect(self.guardar_y_nuevo())

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def guardar_y_nuevo(self):
        return reverse('administrador:add_contacto_institucion', kwargs={'institucion': self.kwargs['institucion']})

    def get_success_url(self):
        return reverse('administrador:list_contacto_institucion', kwargs={'institucion': self.kwargs['institucion']})


@permission_required(perm='institucion', login_url='/')
def list_contacto_institucion(request, institucion):
    template_name = 'administrador/tab_contacto_institucion.html'
    institucion = AcudeInstitucion.objects.get(pk=institucion)
    context = {'institucion': institucion}
    return render(request, template_name, context)


class ContactoInstitucionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = ContactoInstitucion
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_contacto_institucion',
                                                   kwargs={
                                                       'pk': row.pk, 'institucion': self.kwargs[
                                                           'institucion']}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(ContactoInstitucionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return ContactoInstitucion.objects.filter(institucion__pk=self.kwargs['institucion'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ContactoInstitucionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = ContactoInstitucion
    template_name = 'config/formulario_1Col.html'
    form_class = ContactoInstitucionForm

    def get_context_data(self, **kwargs):
        context = super(ContactoInstitucionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def get_success_url(self):
        return reverse('administrador:list_contacto_institucion', kwargs={'institucion': self.kwargs['institucion']})


@permission_required(perm='institucion', login_url='/')
def delete_contacto_institucion(request, pk):
    contacto_institucion = get_object_or_404(ContactoInstitucion, pk=pk)
    contacto_institucion.delete()
    return JsonResponse({'result': 1})

class SucursalInstitucionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = Sucursal
    template_name = 'config/formMapa.html'
    success_url = '/administrador/sucursal_institucion/list'
    form_class = SucursalInstitucionForm

    def get_context_data(self, **kwargs):
        context = super(SucursalInstitucionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una sucursal a la institucion'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una sucursal'
        if 'save_and_new' not in context:
            context['save_and_new'] = 'Guardar y nuevo'

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')
        if form.is_valid():
            try:
                pnt = Point(float(lon), float(lat))
                form.instance.coordenadas = pnt

                institucion = AcudeInstitucion.objects.get(pk=self.kwargs['institucion'])
                sucursal_institucion = form.save(commit=False)

                sucursal_institucion.institucion = institucion
                if self.request.user.rol.pk == 3:
                    estatus = EstatusInstitucion.objects.get(pk=2)
                    sucursal_institucion.estatus_institucion = estatus
                    sucursal_institucion.save()
                    return HttpResponseRedirect(self.get_success_url())
                estatus = EstatusInstitucion.objects.get(pk=1)
                sucursal_institucion.estatus_institucion = estatus
                sucursal_institucion.save()
                return HttpResponseRedirect(self.get_success_url())
            except:
                return render(request, template_name=self.template_name,
                              context={'form': form, 'error': 'Falta ubicación de la institución'})
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def guardar_y_nuevo(self):
        return reverse('administrador:add_sucursal_institucion', kwargs={'institucion': self.kwargs['institucion']})

    def get_success_url(self):
        return reverse('administrador:list_sucursal_institucion', kwargs={'institucion': self.kwargs['institucion']})


@permission_required(perm='institucion', login_url='/')
def list_sucursal_institucion(request, institucion):
    template_name = 'administrador/tab_sucursal_institucion.html'
    institucion = AcudeInstitucion.objects.get(pk=institucion)
    context = {'institucion': institucion}
    return render(request, template_name, context)


class SucursalInstitucionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = Sucursal
    columns = ['id', 'nombre', 'estatus_institucion', 'editar', 'eliminar']
    order_columns = ['id', 'nombre', 'estatus_institucion__nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            if self.request.user.is_consejero:
                return 'NA'
            return '<a class="" href ="' + reverse('administrador:edit_sucursal_institucion',
                                                   kwargs={
                                                       'pk': row.pk, 'institucion': self.kwargs[
                                                           'institucion']}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'estatus_institucion':
            if self.request.user.is_consejero:
                return row.estatus_institucion.nombre
            select = '<select onchange="cambiar_estatus_institucion(' + str(row.pk) + ', this)">'
            estatus = {'Válida': 1, 'Validando': 2, 'Cancelada': 3}
            for key, est in estatus.items():
                if est == row.estatus_institucion.pk:
                    select = select + '<option value="' + str(est) + '" selected>' + key + '</option>'
                else:
                    select = select + '<option value="' + str(est) + '">' + key + '</option>'
            select = select + '</select><script>$("select").material_select();</script>'
            return select
        elif column == 'id':
            return row.pk

        return super(SucursalInstitucionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Sucursal.objects.filter(institucion__pk=self.kwargs['institucion'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class SucursalInstitucionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'institucion'

    model = Sucursal
    template_name = 'config/formMapa.html'
    form_class = SucursalInstitucionForm

    def get_context_data(self, **kwargs):
        context = super(SucursalInstitucionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)
        lon = self.request.POST.get('lgn')
        lat = self.request.POST.get('lat')

        l = self.model.objects.get(pk=self.kwargs['pk'])
        form = SucursalInstitucionForm(request.POST, request.FILES, instance=l)
        if form.is_valid():
            try:
                pnt = Point(float(lon), float(lat))
                form.instance.coordenadas = pnt
                sucursal_institucion = form.save(commit=False)

                sucursal_institucion.save()
                return HttpResponseRedirect(self.get_success_url())
            except:
                return render(request, template_name=self.template_name,
                              context={'form': form, 'error': 'Falta ubicación de la institución'})
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_sucursal_institucion', kwargs={'institucion': self.kwargs['institucion']})


@permission_required(perm='institucion', login_url='/')
def delete_sucursal_institucion(request, pk):
    sucursal_institucion = get_object_or_404(Sucursal, pk=pk)
    sucursal_institucion.delete()
    return JsonResponse({'result': 1})

class SexoAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Sexo
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/sexo/list'
    form_class = SexoForm

    def get_context_data(self, **kwargs):
        context = super(SexoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un sexo'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_sexo(request):
    template_name = 'administrador/tab_sexo.html'
    return render(request, template_name)


class SexoAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Sexo
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_sexo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(SexoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Sexo.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class SexoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/sexo/list'

    model = Sexo
    template_name = 'config/formulario_1Col.html'
    form_class = SexoForm

    def get_context_data(self, **kwargs):
        context = super(SexoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_sexo(request, pk):
    sexo = get_object_or_404(Sexo, pk=pk)
    sexo.delete()
    return JsonResponse({'result': 1})

class MotivoLLamadaAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = MotivoLLamada
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/motivo_llamada/list'
    form_class = MotivoLLamadaForm

    def get_context_data(self, **kwargs):
        context = super(MotivoLLamadaAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un motivo_llamada'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_motivo_llamada(request):
    template_name = 'administrador/tab_motivo_llamada.html'
    return render(request, template_name)


class MotivoLLamadaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = MotivoLLamada
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_motivo_llamada',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(MotivoLLamadaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return MotivoLLamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class MotivoLLamadaEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/motivo_llamada/list'

    model = MotivoLLamada
    template_name = 'config/formulario_1Col.html'
    form_class = MotivoLLamadaForm

    def get_context_data(self, **kwargs):
        context = super(MotivoLLamadaEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_motivo_llamada(request, pk):
    motivo_llamada = get_object_or_404(MotivoLLamada, pk=pk)
    motivo_llamada.delete()
    return JsonResponse({'result': 1})

class DependenciaAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Dependencia
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/dependencia/list'
    form_class = DependenciaForm

    def get_context_data(self, **kwargs):
        context = super(DependenciaAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un dependencia'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_dependencia(request):
    template_name = 'administrador/tab_dependencia.html'
    return render(request, template_name)


class DependenciaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Dependencia
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_dependencia',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(DependenciaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Dependencia.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class DependenciaEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/dependencia/list'

    model = Dependencia
    template_name = 'config/formulario_1Col.html'
    form_class = DependenciaForm

    def get_context_data(self, **kwargs):
        context = super(DependenciaEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_dependencia(request, pk):
    dependencia = get_object_or_404(Dependencia, pk=pk)
    dependencia.delete()
    return JsonResponse({'result': 1})


class RedesApoyoAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = RedesApoyo
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/redes_apoyo/list'
    form_class = RedesApoyoForm

    def get_context_data(self, **kwargs):
        context = super(RedesApoyoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un redes_apoyo'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_redes_apoyo(request):
    template_name = 'administrador/tab_redes_apoyo.html'
    return render(request, template_name)


class RedesApoyoAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = RedesApoyo
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_redes_apoyo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(RedesApoyoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return RedesApoyo.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class RedesApoyoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/redes_apoyo/list'

    model = RedesApoyo
    template_name = 'config/formulario_1Col.html'
    form_class = RedesApoyoForm

    def get_context_data(self, **kwargs):
        context = super(RedesApoyoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_redes_apoyo(request, pk):
    redes_apoyo = get_object_or_404(RedesApoyo, pk=pk)
    redes_apoyo.delete()
    return JsonResponse({'result': 1})

class VictimaInvolucradaAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = VictimaInvolucrada
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/victimas_involucradas/list'
    form_class = VictimaInvolucradaForm

    def get_context_data(self, **kwargs):
        context = super(VictimaInvolucradaAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una víctima involucrada'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_victimas_involucradas(request):
    template_name = 'administrador/tab_victimas_involucradas.html'
    return render(request, template_name)


class VictimaInvolucradaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = VictimaInvolucrada
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_victimas_involucradas',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(VictimaInvolucradaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return VictimaInvolucrada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class VictimaInvolucradaEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/victimas_involucradas/list'

    model = VictimaInvolucrada
    template_name = 'config/formulario_1Col.html'
    form_class = VictimaInvolucradaForm

    def get_context_data(self, **kwargs):
        context = super(VictimaInvolucradaEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_victimas_involucradas(request, pk):
    victimas_involucradas = get_object_or_404(VictimaInvolucrada, pk=pk)
    victimas_involucradas.delete()
    return JsonResponse({'result': 1})


class AgresorAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Agresor
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/agresor/list'
    form_class = AgresorForm

    def get_context_data(self, **kwargs):
        context = super(AgresorAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un agresor'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_agresor(request):
    template_name = 'administrador/tab_agresor.html'
    return render(request, template_name)


class AgresorAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Agresor
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_agresor',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(AgresorAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Agresor.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class AgresorEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/agresor/list'

    model = Agresor
    template_name = 'config/formulario_1Col.html'
    form_class = AgresorForm

    def get_context_data(self, **kwargs):
        context = super(AgresorEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_agresor(request, pk):
    agresor = get_object_or_404(Agresor, pk=pk)
    agresor.delete()
    return JsonResponse({'result': 1})


class ComoSeEnteroAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = ComoSeEntero
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/como_se_entero/list'
    form_class = ComoSeEnteroForm

    def get_context_data(self, **kwargs):
        context = super(ComoSeEnteroAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un como_se_entero'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_como_se_entero(request):
    template_name = 'administrador/tab_como_se_entero.html'
    return render(request, template_name)


class ComoSeEnteroAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = ComoSeEntero
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_como_se_entero',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(ComoSeEnteroAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return ComoSeEntero.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ComoSeEnteroEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/como_se_entero/list'

    model = ComoSeEntero
    template_name = 'config/formulario_1Col.html'
    form_class = ComoSeEnteroForm

    def get_context_data(self, **kwargs):
        context = super(ComoSeEnteroEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_como_se_entero(request, pk):
    como_se_entero = get_object_or_404(ComoSeEntero, pk=pk)
    como_se_entero.delete()
    return JsonResponse({'result': 1})

class EstadoMentalAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = EstadoMental
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/estado_mental/list'
    form_class = EstadoMentalForm

    def get_context_data(self, **kwargs):
        context = super(EstadoMentalAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un estado_mental'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_estado_mental(request):
    template_name = 'administrador/tab_estado_mental.html'
    return render(request, template_name)


class EstadoMentalAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = EstadoMental
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_estado_mental',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(EstadoMentalAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return EstadoMental.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class EstadoMentalEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/estado_mental/list'

    model = EstadoMental
    template_name = 'config/formulario_1Col.html'
    form_class = EstadoMentalForm

    def get_context_data(self, **kwargs):
        context = super(EstadoMentalEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_estado_mental(request, pk):
    estado_mental = get_object_or_404(EstadoMental, pk=pk)
    estado_mental.delete()
    return JsonResponse({'result': 1})

class NivelRiesgoAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = NivelRiesgo
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/nivel_riesgo/list'
    form_class = NivelRiesgoForm

    def get_context_data(self, **kwargs):
        context = super(NivelRiesgoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un nivel_riesgo'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_nivel_riesgo(request):
    template_name = 'administrador/tab_nivel_riesgo.html'
    return render(request, template_name)


class NivelRiesgoAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = NivelRiesgo
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_nivel_riesgo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(NivelRiesgoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return NivelRiesgo.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class NivelRiesgoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/nivel_riesgo/list'

    model = NivelRiesgo
    template_name = 'config/formulario_1Col.html'
    form_class = NivelRiesgoForm

    def get_context_data(self, **kwargs):
        context = super(NivelRiesgoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_nivel_riesgo(request, pk):
    nivel_riesgo = get_object_or_404(NivelRiesgo, pk=pk)
    nivel_riesgo.delete()
    return JsonResponse({'result': 1})

class RecomendacionRiesgoAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = RecomendacionRiesgo
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/recomendacion_riesgo/list'
    form_class = RecomendacionRiesgoForm

    def get_context_data(self, **kwargs):
        context = super(RecomendacionRiesgoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una recomendacion para vida en riesgo'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_recomendacion_riesgo(request):
    template_name = 'administrador/tab_recomendacion_riesgo.html'
    return render(request, template_name)


class RecomendacionRiesgoAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = RecomendacionRiesgo
    columns = ['id', 'nombre', 'tipificacion.nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre', 'tipificacion__nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_recomendacion_riesgo',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(RecomendacionRiesgoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return RecomendacionRiesgo.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)| qs.filter(tipificacion__nombre__icontains=search)
        return qs


class RecomendacionRiesgoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/recomendacion_riesgo/list'

    model = RecomendacionRiesgo
    template_name = 'config/formulario_1Col.html'
    form_class = RecomendacionRiesgoForm

    def get_context_data(self, **kwargs):
        context = super(RecomendacionRiesgoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_recomendacion_riesgo(request, pk):
    recomendacion_riesgo = get_object_or_404(RecomendacionRiesgo, pk=pk)
    recomendacion_riesgo.delete()
    return JsonResponse({'result': 1})

class FaseCambioAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = FaseCambio
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/fase_cambio/list'
    form_class = FaseCambioForm

    def get_context_data(self, **kwargs):
        context = super(FaseCambioAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un fase_cambio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_fase_cambio(request):
    template_name = 'administrador/tab_fase_cambio.html'
    return render(request, template_name)


class FaseCambioAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = FaseCambio
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_fase_cambio',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(FaseCambioAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return FaseCambio.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class FaseCambioEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/fase_cambio/list'

    model = FaseCambio
    template_name = 'config/formulario_1Col.html'
    form_class = FaseCambioForm

    def get_context_data(self, **kwargs):
        context = super(FaseCambioEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_fase_cambio(request, pk):
    fase_cambio = get_object_or_404(FaseCambio, pk=pk)
    fase_cambio.delete()
    return JsonResponse({'result': 1})

class AliadoAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Aliado
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/aliado/list'
    form_class = AliadoForm

    def get_context_data(self, **kwargs):
        context = super(AliadoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un aliado'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_aliado(request):
    template_name = 'administrador/tab_aliado.html'
    return render(request, template_name)


class AliadoAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Aliado
    columns = ['id', 'nombre', 'linea_negocio', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_aliado',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk
        elif column == 'linea_negocio':
            return '<a class="" href ="' + reverse('administrador:list_linea_negocio',
                                                   kwargs={
                                                       'aliado': row.pk}) + '"><i class="material-icons">business_center</i></a>'

        return super(AliadoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Aliado.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class AliadoEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/aliado/list'

    model = Aliado
    template_name = 'config/formulario_1Col.html'
    form_class = AliadoForm

    def get_context_data(self, **kwargs):
        context = super(AliadoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_aliado(request, pk):
    aliado = get_object_or_404(Aliado, pk=pk)
    aliado.delete()
    return JsonResponse({'result': 1})

class LineaNegocioAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = LineaNegocio
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/linea_negocio/list'
    form_class = LineaNegocioForm

    def get_context_data(self, **kwargs):
        context = super(LineaNegocioAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una línea de negocio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una línea de negocio'

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            aliado = Aliado.objects.get(pk=self.kwargs['aliado'])
            linea_negocio = form.save(commit=False)
            linea_negocio.aliado = aliado
            linea_negocio.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_linea_negocio', kwargs={'aliado': self.kwargs['aliado']})


@permission_required(perm='catalogo', login_url='/')
def list_linea_negocio(request, aliado):
    template_name = 'administrador/tab_linea_negocio.html'
    aliado = Aliado.objects.get(pk=aliado)
    context = {'aliado': aliado}
    return render(request, template_name, context)


class LineaNegocioAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Sucursal
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_linea_negocio',
                                                   kwargs={
                                                       'pk': row.pk, 'aliado': self.kwargs[
                                                           'aliado']}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(LineaNegocioAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return LineaNegocio.objects.filter(aliado__pk=self.kwargs['aliado'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class LineaNegocioEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = LineaNegocio
    template_name = 'config/formulario_1Col.html'
    form_class = LineaNegocioForm

    def get_context_data(self, **kwargs):
        context = super(LineaNegocioEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar línea de negocio'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST, request.FILES)

        l = self.model.objects.get(pk=self.kwargs['pk'])
        form = LineaNegocioForm(request.POST, request.FILES, instance=l)
        if form.is_valid():
            linea_negocio = form.save(commit=False)
            linea_negocio.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_linea_negocio', kwargs={'aliado': self.kwargs['aliado']})


@permission_required(perm='catalogo', login_url='/')
def delete_linea_negocio(request, pk):
    linea_negocio = get_object_or_404(LineaNegocio, pk=pk)
    linea_negocio.delete()
    return JsonResponse({'result': 1})

class ActividadUsuarioAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = EstatusUsuario
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/actividad_usuario/list'
    form_class = ActividadUsuarioForm

    def get_context_data(self, **kwargs):
        context = super(ActividadUsuarioAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una actividad de usuario'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una actividad de usuario'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_actividad_usuario(request):
    template_name = 'administrador/tab_actividad_usuario.html'
    return render(request, template_name)


class ActividadUsuarioAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = EstatusUsuario
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_actividad_usuario',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(ActividadUsuarioAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return EstatusUsuario.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ActividadUsuarioEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/actividad_usuario/list'

    model = EstatusUsuario
    template_name = 'config/formulario_1Col.html'
    form_class = ActividadUsuarioForm

    def get_context_data(self, **kwargs):
        context = super(ActividadUsuarioEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_actividad_usuario(request, pk):
    actividad_usuario = get_object_or_404(EstatusUsuario, pk=pk)
    actividad_usuario.delete()
    return JsonResponse({'result': 1})

class TipificacionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Tipificacion
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/tipificacion/list'
    form_class = TipificacionForm

    def get_context_data(self, **kwargs):
        context = super(TipificacionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una tipificación'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una actividad de usuario'
        return context


@permission_required(perm='catalogo', login_url='/')
def list_tipificacion(request):
    template_name = 'administrador/tab_tipificacion.html'
    return render(request, template_name)


class TipificacionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = Tipificacion
    columns = ['id', 'nombre', 'subcategoria', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_tipificacion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'subcategoria':
            return '<a class="" href ="' + reverse('administrador:list_categoria_tipificacion',
                                                   kwargs={
                                                       'tipificacion': row.pk}) + '"><i class="material-icons">assignment</i></a>'
        elif column == 'id':
            return row.pk

        return super(TipificacionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Tipificacion.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class TipificacionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/administrador/tipificacion/list'

    model = Tipificacion
    template_name = 'config/formulario_1Col.html'
    form_class = TipificacionForm

    def get_context_data(self, **kwargs):
        context = super(TipificacionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@permission_required(perm='catalogo', login_url='/')
def delete_tipificacion(request, pk):
    tipificacion = get_object_or_404(Tipificacion, pk=pk)
    tipificacion.delete()
    return JsonResponse({'result': 1})


class CategoriaTipificacionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = CategoriaTipificacion
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/categoria_tipificacion/list'
    form_class = CategoriaTipificacionForm

    def get_context_data(self, **kwargs):
        context = super(CategoriaTipificacionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una subcategoría a la tipificación'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        if 'save_and_new' not in context:
            context['save_and_new'] = 'Guardar y nuevo'

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():

            tipificacion = Tipificacion.objects.get(pk=self.kwargs['tipificacion'])
            cont_tipificacion = form.save(commit=False)

            cont_tipificacion.tipificacion = tipificacion
            cont_tipificacion.save()
            if 'save_and_new' in form.data:
                return HttpResponseRedirect(self.guardar_y_nuevo())

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def guardar_y_nuevo(self):
        return reverse('administrador:add_categoria_tipificacion', kwargs={'tipificacion': self.kwargs['tipificacion']})

    def get_success_url(self):
        return reverse('administrador:list_categoria_tipificacion', kwargs={'tipificacion': self.kwargs['tipificacion']})


@permission_required(perm='catalogo', login_url='/')
def list_categoria_tipificacion(request, tipificacion):
    template_name = 'administrador/tab_categoria_tipificacion.html'
    tipificacion_obj = Tipificacion.objects.get(pk=tipificacion)
    context = {'tipificacion': tipificacion_obj}
    return render(request, template_name, context)


class CategoriaTipificacionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = CategoriaTipificacion
    columns = ['id', 'nombre', 'subcategoria', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_categoria_tipificacion',
                                                   kwargs={
                                                       'pk': row.pk, 'tipificacion': self.kwargs[
                                                           'tipificacion']}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk
        elif column == 'subcategoria':
            return '<a class="" href ="' + reverse('administrador:list_subcategoria_tipificacion',
                                                   kwargs={
                                                       'categoria_tipificacion': row.pk}) + '"><i class="material-icons">assignment</i></a>'

        return super(CategoriaTipificacionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return CategoriaTipificacion.objects.filter(tipificacion__pk=self.kwargs['tipificacion'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class CategoriaTipificacionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = CategoriaTipificacion
    template_name = 'config/formulario_1Col.html'
    form_class = CategoriaTipificacionForm

    def get_context_data(self, **kwargs):
        context = super(CategoriaTipificacionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def get_success_url(self):
        return reverse('administrador:list_categoria_tipificacion', kwargs={'tipificacion': self.kwargs['tipificacion']})


@permission_required(perm='catalogo', login_url='/')
def delete_categoria_tipificacion(request, pk):
    categoria_tipificacion = get_object_or_404(CategoriaTipificacion, pk=pk)
    categoria_tipificacion.delete()
    return JsonResponse({'result': 1})

class SubcategoriaTipificacionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = SubcategoriaTipificacion
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/subcategoria_tipificacion/list'
    form_class = SubcategoriaTipificacionForm

    def get_context_data(self, **kwargs):
        context = super(SubcategoriaTipificacionAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar una subcategoría a la tipificación'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar una subcategoría'
        if 'save_and_new' not in context:
            context['save_and_new'] = 'Guardar y nuevo'

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():

            cat_tipificacion = CategoriaTipificacion.objects.get(pk=self.kwargs['categoria_tipificacion'])
            cont_tipificacion = form.save(commit=False)

            cont_tipificacion.categoria = cat_tipificacion
            cont_tipificacion.save()
            if 'save_and_new' in form.data:
                return HttpResponseRedirect(self.guardar_y_nuevo())

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def guardar_y_nuevo(self):
        return reverse('administrador:add_subcategoria_tipificacion', kwargs={'categoria_tipificacion': self.kwargs['categoria_tipificacion']})

    def get_success_url(self):
        return reverse('administrador:list_subcategoria_tipificacion', kwargs={'categoria_tipificacion': self.kwargs['categoria_tipificacion']})


@permission_required(perm='catalogo', login_url='/')
def list_subcategoria_tipificacion(request, categoria_tipificacion):
    template_name = 'administrador/tab_subcategoria_tipificacion.html'
    tipificacion_obj = CategoriaTipificacion.objects.get(pk=categoria_tipificacion)
    context = {'categoria_tipificacion': tipificacion_obj}
    return render(request, template_name, context)


class SubcategoriaTipificacionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = SubcategoriaTipificacion
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_subcategoria_tipificacion',
                                                   kwargs={
                                                       'pk': row.pk, 'categoria_tipificacion': self.kwargs[
                                                           'categoria_tipificacion']}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(SubcategoriaTipificacionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return SubcategoriaTipificacion.objects.filter(categoria__pk=self.kwargs['categoria_tipificacion'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class SubcategoriaTipificacionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'

    model = SubcategoriaTipificacion
    template_name = 'config/formulario_1Col.html'
    form_class = SubcategoriaTipificacionForm

    def get_context_data(self, **kwargs):
        context = super(SubcategoriaTipificacionEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context

    def get_success_url(self):
        return reverse('administrador:list_subcategoria_tipificacion', kwargs={'categoria_tipificacion': self.kwargs['categoria_tipificacion']})


@permission_required(perm='catalogo', login_url='/')
def delete_subcategoria_tipificacion(request, pk):
    subcategoria_tipificacion = get_object_or_404(SubcategoriaTipificacion, pk=pk)
    subcategoria_tipificacion.delete()
    return JsonResponse({'result': 1})