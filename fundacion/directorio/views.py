from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.geos import Point

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from adminstrador.forms import AcudeInstitucionForm, ContactoInstitucionForm
from config.models import AcudeInstitucion, ContactoInstitucion


class AcudeInstitucionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'directorio'

    model = AcudeInstitucion
    template_name = 'config/formMapa.html'
    success_url = '/directorio/acude_institucion/list'
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
        return reverse('directorio:list_acude_institucion')


@permission_required(perm='directorio', login_url='/')
def list_acude_institucion(request):
    template_name = 'directorio/tab_acude_institucion.html'
    return render(request, template_name)


class AcudeInstitucionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'directorio'

    model = AcudeInstitucion
    columns = ['id', 'nombre', 'contacto', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('directorio:edit_acude_institucion',
                                                   kwargs={
                                                       'pk': row.pk}) + '"><img  src="http://orientacionjuvenil.colorsandberries.com/Imagenes/fundacion_origen/3/editar.png"></a>'
        elif column == 'contacto':
            return '<a class="" href ="' + reverse('directorio:list_contacto_institucion',
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


class AcudeInstitucionEdit(PermissionRequiredMixin, UpdateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'directorio'
    success_url = '/directorio/acude_institucion/list'

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
        return reverse('directorio:list_acude_institucion')


@permission_required(perm='directorio', login_url='/')
def delete_acude_institucion(request, pk):
    acude_institucion = get_object_or_404(AcudeInstitucion, pk=pk)
    acude_institucion.delete()
    return JsonResponse({'result': 1})

class ContactoInstitucionAdd(PermissionRequiredMixin, CreateView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'directorio'

    model = ContactoInstitucion
    template_name = 'config/formulario_1Col.html'
    success_url = '/directorio/contacto_institucion/list'
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
        return reverse('directorio:add_contacto_institucion', kwargs={'institucion': self.kwargs['institucion']})

    def get_success_url(self):
        return reverse('directorio:list_contacto_institucion', kwargs={'institucion': self.kwargs['institucion']})


@permission_required(perm='directorio', login_url='/')
def list_contacto_institucion(request, institucion):
    template_name = 'directorio/tab_contacto_institucion.html'
    institucion = AcudeInstitucion.objects.get(pk=institucion)
    context = {'institucion': institucion}
    return render(request, template_name, context)


class ContactoInstitucionAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'directorio'

    model = ContactoInstitucion
    columns = ['id', 'nombre', 'editar', 'eliminar']
    order_columns = ['id', 'nombre']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'editar':
            return '<a class="" href ="' + reverse('directorio:edit_contacto_institucion',
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
    permission_required = 'directorio'

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
        return reverse('directorio:list_contacto_institucion', kwargs={'institucion': self.kwargs['institucion']})


@permission_required(perm='directorio', login_url='/')
def delete_contacto_institucion(request, pk):
    contacto_institucion = get_object_or_404(ContactoInstitucion, pk=pk)
    contacto_institucion.delete()
    return JsonResponse({'result': 1})