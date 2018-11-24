from django.contrib.auth import logout
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from adminstrador.forms import AcudeInstitucionForm, EstadoForm, PaisForm, EstadoCivilForm, EstatusForm, \
    LenguaIndigenaForm, MedioContactoForm, ModalidadViolenciaForm, MunicipioForm, NivelEstudioForm, NivelViolenciaForm, \
    OcupacionForm, ReligionForm, TipoCasoForm, TipoViolenciaForm, ViolentometroForm, ViveConForm, ConsejeroForm, \
    DirectorioForm, SupervisorForm, ContactoInstitucionForm, CalidadForm
from config.models import AcudeInstitucion, Estado, Pais, EstadoCivil, Estatus, LenguaIndigena, MedioContacto, \
    ModalidadViolencia, Municipio, NivelEstudio, NivelViolencia, Ocupacion, Religion, TipoCaso, TipoViolencia, \
    Violentometro, ViveCon, ContactoInstitucion

def logout_view(request):
    logout(request)
    return redirect(reverse('webapp:login'))

def index(request):
    template_name = 'config/index.html'
    return render(request, template_name)

def catalogos(request):
    template_name = 'administrador/catalogos.html'
    return render(request, template_name)

class ConsejeroAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_consejero'

    model = User
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
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            permiso = Permission.objects.get(codename='consejero')
            user.save()
            user.user_permissions.add(permiso)
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_consejero')


# @permission_required(perm='change_consejero', login_url='/login/')
def list_consejero(request):
    template_name = 'administrador/tab_consejero.html'
    return render(request, template_name)


class ConsejeroAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_consejero'

    model = User
    columns = ['id', 'username', 'email', 'editar', 'eliminar']
    order_columns = ['id', 'username', 'email']
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
        permiso = Permission.objects.get(codename='consejero')
        return User.objects.all().filter(user_permissions=permiso)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(username__icontains=search) | qs.filter(pk__icontains=search) | qs.filter(
                email__icontains=search)
        return qs


class ConsejeroEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_consejero'
    success_url = '/administrador/consejero/list'

    model = User
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
        usuario = User.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_consejero')


# @permission_required(perm='delete_consejero', login_url='/login/')
def delete_consejero(request, pk):
    consejero = get_object_or_404(User, pk=pk)
    consejero.delete()
    return JsonResponse({'result': 1})

class DirectorioAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_directorio'

    model = User
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
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            permiso = Permission.objects.get(codename='directorio')
            user.save()
            user.user_permissions.add(permiso)
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_directorio')


# @permission_required(perm='change_directorio', login_url='/login/')
def list_directorio(request):
    template_name = 'administrador/tab_directorio.html'
    return render(request, template_name)


class DirectorioAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_directorio'

    model = User
    columns = ['id', 'username', 'email', 'editar', 'eliminar']
    order_columns = ['id', 'username', 'email']
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
        return User.objects.all().filter(user_permissions=permiso)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(username__icontains=search) | qs.filter(pk__icontains=search) | qs.filter(
                email__icontains=search)
        return qs


class DirectorioEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_directorio'
    success_url = '/administrador/directorio/list'

    model = User
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
        usuario = User.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_directorio')


# @permission_required(perm='delete_directorio', login_url='/login/')
def delete_directorio(request, pk):
    directorio = get_object_or_404(User, pk=pk)
    directorio.delete()
    return JsonResponse({'result': 1})

class SupervisorAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_supervisor'

    model = User
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
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            permiso = Permission.objects.get(codename='supervisor')
            user.save()
            user.user_permissions.add(permiso)
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_supervisor')


# @permission_required(perm='change_supervisor', login_url='/login/')
def list_supervisor(request):
    template_name = 'administrador/tab_supervisor.html'
    return render(request, template_name)


class SupervisorAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_supervisor'

    model = User
    columns = ['id', 'username', 'email', 'editar', 'eliminar']
    order_columns = ['id', 'username', 'email']
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
        permiso = Permission.objects.get(codename='supervisor')
        return User.objects.all().filter(user_permissions=permiso)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(username__icontains=search) | qs.filter(pk__icontains=search) | qs.filter(
                email__icontains=search)
        return qs


class SupervisorEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_supervisor'
    success_url = '/administrador/supervisor/list'

    model = User
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
        usuario = User.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_supervisor')


# @permission_required(perm='delete_supervisor', login_url='/login/')
def delete_supervisor(request, pk):
    supervisor = get_object_or_404(User, pk=pk)
    supervisor.delete()
    return JsonResponse({'result': 1})

class CalidadAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_calidad'

    model = User
    template_name = 'config/formulario_1Col.html'
    form_class = CalidadForm

    def get_context_data(self, **kwargs):
        context = super(CalidadAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar calidad'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un calidad'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            permiso = Permission.objects.get(codename='calidad')
            user.save()
            user.user_permissions.add(permiso)
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_calidad')


# @permission_required(perm='change_calidad', login_url='/login/')
def list_calidad(request):
    template_name = 'administrador/tab_calidad.html'
    return render(request, template_name)


class CalidadAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_calidad'

    model = User
    columns = ['id', 'username', 'email', 'editar', 'eliminar']
    order_columns = ['id', 'username', 'email']
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
        permiso = Permission.objects.get(codename='calidad')
        return User.objects.all().filter(user_permissions=permiso)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(username__icontains=search) | qs.filter(pk__icontains=search) | qs.filter(
                email__icontains=search)
        return qs


class CalidadEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_calidad'
    success_url = '/administrador/calidad/list'

    model = User
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
        usuario = User.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_calidad')


# @permission_required(perm='delete_calidad', login_url='/login/')
def delete_calidad(request, pk):
    calidad = get_object_or_404(User, pk=pk)
    calidad.delete()
    return JsonResponse({'result': 1})

class AcudeInstitucionAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_acude_institucion'

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
                institucion.save()
                return HttpResponseRedirect(self.get_success_url())
            except:
                return render(request, template_name=self.template_name,
                              context={'form': form, 'error': 'Falta ubicación de la institución'})
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('administrador:list_acude_institucion')


# @permission_required(perm='change_acude_institucion', login_url='/login/')
def list_acude_institucion(request):
    template_name = 'administrador/tab_acude_institucion.html'
    return render(request, template_name)


class AcudeInstitucionAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_acude_institucion'

    model = AcudeInstitucion
    columns = ['id', 'nombre', 'contacto', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_acude_institucion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'contacto':
            return '<a class="" href ="' + reverse('administrador:list_contacto_institucion',
                                                   kwargs={
                                                       'institucion': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/usuario.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
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


# @permission_required(perm='delete_acude_institucion', login_url='/login/')
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


# @permission_required(perm='change_estado', login_url='/login/')
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


# @permission_required(perm='delete_estado', login_url='/login/')
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


# @permission_required(perm='change_pais', login_url='/login/')
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


# @permission_required(perm='delete_pais', login_url='/login/')
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


# @permission_required(perm='change_estado_civil', login_url='/login/')
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


# @permission_required(perm='delete_estado_civil', login_url='/login/')
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


# @permission_required(perm='change_estatus', login_url='/login/')
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


# @permission_required(perm='delete_estatus', login_url='/login/')
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


# @permission_required(perm='change_lengua_indigena', login_url='/login/')
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


# @permission_required(perm='delete_lengua_indigena', login_url='/login/')
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


# @permission_required(perm='change_medio_contacto', login_url='/login/')
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


# @permission_required(perm='delete_medio_contacto', login_url='/login/')
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


# @permission_required(perm='change_modalidad_violencia', login_url='/login/')
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


# @permission_required(perm='delete_modalidad_violencia', login_url='/login/')
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


# @permission_required(perm='change_municipio', login_url='/login/')
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


# @permission_required(perm='delete_municipio', login_url='/login/')
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


# @permission_required(perm='change_nivel_estudio', login_url='/login/')
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


# @permission_required(perm='delete_nivel_estudio', login_url='/login/')
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


# @permission_required(perm='change_nivel_violencia', login_url='/login/')
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


# @permission_required(perm='delete_nivel_violencia', login_url='/login/')
def delete_nivel_violencia(request, pk):
    nivel_violencia = get_object_or_404(NivelViolencia, pk=pk)
    nivel_violencia.delete()
    return JsonResponse({'result': 1})


class OcupacionAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_ocupacion'

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


# @permission_required(perm='change_ocupacion', login_url='/login/')
def list_ocupacion(request):
    template_name = 'administrador/tab_ocupacion.html'
    return render(request, template_name)


class OcupacionAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_ocupacion'

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


class OcupacionEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_ocupacion'
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


# @permission_required(perm='delete_ocupacion', login_url='/login/')
def delete_ocupacion(request, pk):
    ocupacion = get_object_or_404(Ocupacion, pk=pk)
    ocupacion.delete()
    return JsonResponse({'result': 1})


class ReligionAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_religion'

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


# @permission_required(perm='change_religion', login_url='/login/')
def list_religion(request):
    template_name = 'administrador/tab_religion.html'
    return render(request, template_name)


class ReligionAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_religion'

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


class ReligionEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_religion'
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


# @permission_required(perm='delete_religion', login_url='/login/')
def delete_religion(request, pk):
    religion = get_object_or_404(Religion, pk=pk)
    religion.delete()
    return JsonResponse({'result': 1})


class TipoCasoAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_tipo_caso'

    model = TipoCaso
    template_name = 'config/formulario_1Col.html'
    success_url = '/administrador/tipo_caso/list'
    form_class = TipoCasoForm

    def get_context_data(self, **kwargs):
        context = super(TipoCasoAdd, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un tipo_caso'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un'
        return context


# @permission_required(perm='change_tipo_caso', login_url='/login/')
def list_tipo_caso(request):
    template_name = 'administrador/tab_tipo_caso.html'
    return render(request, template_name)


class TipoCasoAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_tipo_caso'

    model = TipoCaso
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_tipo_caso',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(TipoCasoAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return TipoCaso.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class TipoCasoEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_tipo_caso'
    success_url = '/administrador/tipo_caso/list'

    model = TipoCaso
    template_name = 'config/formulario_1Col.html'
    form_class = TipoCasoForm

    def get_context_data(self, **kwargs):
        context = super(TipoCasoEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


# @permission_required(perm='delete_tipo_caso', login_url='/login/')
def delete_tipo_caso(request, pk):
    tipo_caso = get_object_or_404(TipoCaso, pk=pk)
    tipo_caso.delete()
    return JsonResponse({'result': 1})


class TipoViolenciaAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_tipo_violencia'

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


# @permission_required(perm='change_tipo_violencia', login_url='/login/')
def list_tipo_violencia(request):
    template_name = 'administrador/tab_tipo_violencia.html'
    return render(request, template_name)


class TipoViolenciaAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_tipo_violencia'

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


class TipoViolenciaEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_tipo_violencia'
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


# @permission_required(perm='delete_tipo_violencia', login_url='/login/')
def delete_tipo_violencia(request, pk):
    tipo_violencia = get_object_or_404(TipoViolencia, pk=pk)
    tipo_violencia.delete()
    return JsonResponse({'result': 1})


class ViolentometroAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_violentometro'

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


# @permission_required(perm='change_violentometro', login_url='/login/')
def list_violentometro(request):
    template_name = 'administrador/tab_violentometro.html'
    return render(request, template_name)


class ViolentometroAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_violentometro'

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


class ViolentometroEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_violentometro'
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


# @permission_required(perm='delete_violentometro', login_url='/login/')
def delete_violentometro(request, pk):
    violentometro = get_object_or_404(Violentometro, pk=pk)
    violentometro.delete()
    return JsonResponse({'result': 1})


class ViveConAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_vive_con'

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


# @permission_required(perm='change_vive_con', login_url='/login/')
def list_vive_con(request):
    template_name = 'administrador/tab_vive_con.html'
    return render(request, template_name)


class ViveConAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_vive_con'

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


class ViveConEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_vive_con'
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


# @permission_required(perm='delete_vive_con', login_url='/login/')
def delete_vive_con(request, pk):
    vive_con = get_object_or_404(ViveCon, pk=pk)
    vive_con.delete()
    return JsonResponse({'result': 1})


class ContactoInstitucionAdd(CreateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'add_contacto_institucion'

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


# @permission_required(perm='change_contacto_institucion', login_url='/login/')
def list_contacto_institucion(request, institucion):
    template_name = 'administrador/tab_contacto_institucion.html'
    institucion = AcudeInstitucion.objects.get(pk=institucion)
    context = {'institucion': institucion}
    return render(request, template_name, context)


class ContactoInstitucionAjaxList(BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_contacto_institucion'

    model = ContactoInstitucion
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('administrador:edit_contacto_institucion',
                                                   kwargs={
                                                       'pk': row.pk, 'institucion': self.kwargs['institucion']}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk

        return super(ContactoInstitucionAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return ContactoInstitucion.objects.filter(institucion__pk= self.kwargs['institucion'])

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class ContactoInstitucionEdit(UpdateView):
    redirect_field_name = 'next'
    login_url = '/login/'
    permission_required = 'change_contacto_institucion'

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


# @permission_required(perm='delete_contacto_institucion', login_url='/login/')
def delete_contacto_institucion(request, pk):
    contacto_institucion = get_object_or_404(ContactoInstitucion, pk=pk)
    contacto_institucion.delete()
    return JsonResponse({'result': 1})
