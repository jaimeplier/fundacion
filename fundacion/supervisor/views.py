from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render

# Create your views here.
from django_datatables_view.base_datatable_view import BaseDatatableView

from config.models import Llamada


@permission_required(perm='supervisor', login_url='/')
def reportes(request):
    template_name = 'supervisor/tab_reportes.html'
    return render(request, template_name)


@permission_required(perm='supervisor', login_url='/')
def resumen(request):
    template_name = 'administrador/resumen.html'
    return render(request, template_name)

class LlamadaAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'supervisor'

    model = Llamada
    columns = ['id', 'victima.nombre', 'consejero.get_full_name', 'hora_inicio', 'hora_fin', 'duracion_llamada', 'vida_riesgo', 'tipo_violencia', 'institucion', 'estatus', 'medio_contacto']
    order_columns = ['id', 'victima__nombre', 'consejero.a_paterno', 'hora_inicio', 'hora_fin', '', 'vida_en_riesgo', 'tipo_violencia', 'estatus', 'institucion__nombre', 'estatus__nombre', 'medio_contacto']
    max_display_length = 100

    def render_column(self, row, column):

        if column == 'id':
            return row.pk

        return super(LlamadaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Llamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs
