from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render

# Create your views here.
from django_datatables_view.base_datatable_view import BaseDatatableView
from pytz import timezone

from config.models import Llamada
from fundacion import settings


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
    columns = ['id', 'victima.nombre', 'nombre', 'fecha', 'hora_inicio', 'hora_fin', 'duracion_llamada', 'vida_en_riesgo', 'tipo_violencia', 'institucion', 'estatus', 'medio_contacto']
    order_columns = ['id', 'victima__nombre', 'fecha', 'consejero.a_paterno', 'hora_inicio', 'hora_fin', '', 'vida_en_riesgo', 'tipo_violencia', 'estatus', 'institucion__nombre', 'estatus__nombre', 'medio_contacto']
    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)

    def render_column(self, row, column):

        if column == 'id':
            return row.pk
        elif column == 'nombre':
            return  row.consejero.get_full_name()
        elif column == 'vida_en_riesgo':
            if row.vida_en_riesgo:
                return 'Sí'
            return 'No'
        elif column == 'duracion_llamada':
            formato = '%H:%M:%S'
            h1 = str(row.hora_inicio.hour) + ':' + str(row.hora_inicio.minute) + ':' + str(row.hora_inicio.second)
            h2 = str(row.hora_fin.hour) + ':' + str(row.hora_fin.minute) + ':' + str(row.hora_fin.second)
            h1 = datetime.strptime(h1, formato)
            h2 = datetime.strptime(h2, formato)
            return str(h2-h1)

        return super(LlamadaAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Llamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        dia = self.request.GET.get(u'dia', None)
        mes = self.request.GET.get(u'mes', None)
        fecha1 = self.request.GET.get(u'fecha1', None)
        fecha2 = self.request.GET.get(u'fecha2', None)
        if dia:
            datetime_object = datetime.strptime(dia, '%Y-%m-%d')
            qs = qs.filter(fecha=datetime_object)
        if mes:
            qs = qs.filter(fecha__month=mes)
        if fecha1 and fecha2:
            fecha_inicio = datetime.strptime(fecha1, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha2, '%Y-%m-%d')
            qs = qs.filter(fecha__range=(fecha_inicio, fecha_fin))
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs
