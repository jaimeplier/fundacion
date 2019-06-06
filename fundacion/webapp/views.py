from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DetailView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from config.models import Usuario, Pendiente, Llamada, TipificacionLLamada, Evaluacion, \
    CalificacionLlamada, VictimaMenorEdad
from webapp.forms import PendienteForm


def index(request):
    template_name = 'config/index.html'
    rutas = [{'nombre': 'menu', 'url': reverse('webapp:index')}]
    context = {'rutas':rutas}
    return render(request, template_name, context)

def login(request):
    error_message = ''
    context = {}
    if request.method == 'POST':
        email = request.POST['correo']
        password = request.POST['password']
        user = authenticate(correo=email, password=password)
        if user is not None:
            auth_login(request, user)
            if request.POST.get('next') is not None:
                return redirect(request.POST.get('next'))
            elif user.rol.nombre == 'administrador':
                return redirect(reverse('webapp:index'))
            elif user.rol.nombre == 'directorio':
                return redirect(reverse('administrador:list_acude_institucion'))
            elif user.rol.nombre == 'consejero':
                return redirect(reverse('consejero:busqueda_usuario'))
            elif user.rol.nombre == 'supervisor':
                return redirect(reverse('supervisor:resumen'))
            elif user.rol.nombre == 'calidad':
                return redirect(reverse('calidad:list_evaluacion'))
            return redirect(reverse('webapp:index'))
        else:
            error_message = "Usuario y/o contraseña incorrectos"
            context = {
                'error_message': error_message, 'next': request.POST.get('next')
            }
            return render(request, 'config/login.html', context)
    if request.GET.get('next') is not None:
        context['next'] = request.GET.get('next')
    return render(request, 'config/login.html', context)

def logout_view(request):
    logout(request)
    return redirect(reverse('webapp:login'))

def avisos(request):
    template_name = 'config/enviar_avisos.html'
    return render(request, template_name)

def recados(request):
    template_name = 'config/enviar_recados.html'
    return render(request, template_name)

def ver_avisos(request):
    template_name = 'config/recibir_avisos.html'
    usuario = Usuario.objects.get(pk=request.user.pk)
    context = {
        'usuario': usuario
    }
    return render(request, template_name, context)

def ver_recados(request):
    return render(
        request, 'config/recibir_recados.html', dict(usuario=Usuario.objects.get(pk=request.user.pk))
    )

class PendienteAdd(LoginRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'

    model = Pendiente
    template_name = 'config/formulario_1Col.html'
    form_class = PendienteForm

    def get_context_data(self, **kwargs):
        context = super(PendienteAdd, self).get_context_data(**kwargs)
        if 'rutas' not in context:
            if self.request.user.is_consejero:
                menu = reverse('consejero:busqueda_usuario')
            elif self.request.user.is_supervisor:
                menu = reverse('supervisor:resumen')
            elif self.request.user.is_directorio:
                menu = reverse('administrador:list_acude_institucion')
            elif self.request.user.is_calidad:
                menu = reverse('calidad:list_evaluacion')
            else:
                menu = reverse('webapp:index')
            rutas = [{'nombre': 'menu', 'url': menu},
                     {'nombre': 'Pendientes', 'url': reverse('webapp:list_pendiente')}]
            context['rutas'] = rutas
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Agregar un pendiente'
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Completa todos los campos para registrar un pendiente'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            pendiente = form.save(commit=False)
            usuario = Usuario.objects.get(pk=self.request.user.pk)
            pendiente.usuario = usuario
            pendiente.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('webapp:list_pendiente')


@login_required(login_url='/')
def list_pendiente(request):
    template_name = 'config/tab_pendiente.html'
    return render(request, template_name)


class PendienteAjaxList(LoginRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'

    model = Pendiente
    columns = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_limite', 'completado', 'editar', 'eliminar']
    order_columns = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_limite', 'completado']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('webapp:edit_pendiente',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'eliminar':
            return '<a class=" modal-trigger" href ="#" onclick="actualiza(' + str(
                row.pk) + ')"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/eliminar.png"></a>'
        elif column == 'id':
            return row.pk
        elif column == 'completado':
            if row.completado:
                return '<img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/aceptar.png">'
            return '<img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/rechazar.png">'
        elif column == 'fecha_inicio':
            if row.fecha_inicio is not None:
                return row.fecha_inicio.strftime("%d %A %Y")
            else:
                return 'Sin fecha'
        elif column == 'fecha_limite':
            if row.fecha_limite is not None:
                return row.fecha_limite.strftime("%d %A %Y")
            else:
                return 'Sinfecha'

        return super(PendienteAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Pendiente.objects.filter(usuario__pk=self.request.user.pk)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search) | qs.filter(
                descripcion__icontains=search) | qs.filter(fecha_limite__icontains=search) | qs.filter(
                completado__icontains=search) | qs.filter(fecha_inicio__icontains=search)
        return qs


class PendienteEdit(LoginRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'catalogo'
    success_url = '/pendiente/list'

    model = Pendiente
    template_name = 'config/formulario_1Col.html'
    form_class = PendienteForm

    def get_context_data(self, **kwargs):
        context = super(PendienteEdit, self).get_context_data(**kwargs)
        if 'rutas' not in context:
            if self.request.user.is_consejero:
                menu = reverse('consejero:busqueda_usuario')
            elif self.request.user.is_supervisor:
                menu = reverse('supervisor:resumen')
            elif self.request.user.is_directorio:
                menu = reverse('administrador:list_acude_institucion')
            elif self.request.user.is_calidad:
                menu = reverse('calidad:list_evaluacion')
            else:
                menu = reverse('webapp:index')
            rutas = [{'nombre': 'menu', 'url': menu},
                     {'nombre': 'Pendientes', 'url': reverse('webapp:list_pendiente')}]
            context['rutas'] = rutas
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'titulo' not in context:
            context['titulo'] = 'Editar '
        if 'instrucciones' not in context:
            context['instrucciones'] = 'Modifica o actualiza los datos que requieras'
        return context


@login_required(login_url='/')
def delete_pendiente(request, pk):
    pendiente = get_object_or_404(Pendiente, pk=pk)
    pendiente.delete()
    return JsonResponse({'result': 1})

@login_required(login_url='/')
def list_llamada(request):
    template_name = 'config/tab_llamada.html'
    return render(request, template_name)


class LlamadaAjaxList(LoginRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'

    model = Llamada
    columns = ['id', 'victima', 'consejero', 'hora_inicio', 'hora_fin', 'duracion_llamada', 'vida_en_riesgo',
               'tipificacion', 'medio_contacto', 'ver']
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
        elif column == 'ver':
            return '<a href="'+ reverse('webapp:ver_servicio', kwargs={'pk': row.pk})+'"><i class="material-icons">perm_phone_msg</i></a>'

        return super(LlamadaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Llamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs


class VerServicio(LoginRequiredMixin, DetailView):
    redirect_field_name = 'next'
    login_url = '/'
    model = Llamada
    template_name = 'config/ver_servicio.html'

    def get_context_data(self, **kwargs):
        context = super(VerServicio, self).get_context_data(**kwargs)
        servicio = Llamada.objects.get(pk=self.kwargs['pk'])
        victimas_menores = VictimaMenorEdad.objects.filter(llamada=servicio)
        tipificacion = TipificacionLLamada.objects.filter(llamada=servicio).first()
        ##examen_mental = ExamenMental.objects.filter(llamada=servicio).first()
        rubros = Evaluacion.objects.all()
        evaluacion = CalificacionLlamada.objects.filter(llamada=servicio)
        context['servicio'] = servicio
        context['tipificacion'] = tipificacion
        ##context['examen_mental'] = examen_mental
        context['rubros'] = rubros
        context['tareas'] = servicio.tareas.all()
        context['evaluaciones'] = evaluacion
        return context