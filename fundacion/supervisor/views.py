from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum, Count, Avg, Q
from django.shortcuts import render

# Create your views here.
from django_datatables_view.base_datatable_view import BaseDatatableView
from pytz import timezone

from config.models import Llamada, Consejero
from fundacion import settings


@permission_required(perm='supervisor', login_url='/')
def reportes(request):
    template_name = 'supervisor/tab_productividad.html'
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

class ProductividadAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'supervisor'

    model = Consejero
    columns = ['consejero', 'tiempo_servicio', 'total_llamadas', 'llamadas_atendidas', 'transferencias_recibidas',
               'transferencias_realizadas', 'abandonos', 'promedio']
    order_columns = ['consejero', '', '', '', '', '', '', '']
    max_display_length = 100
    settingstime_zone = timezone(settings.TIME_ZONE)

    def render_column(self, row, column):

        if column == 'tiempo_servicio':
            return row['tiempo_servicio']
        elif column == 'consejero':
            consejero = Consejero.objects.get(pk=row['consejero'])
            return consejero.get_full_name()
        elif column == 'total_llamadas':
            return row['total_llamadas']
        elif column == 'llamadas_atendidas':
            return row['llamadas_atendidas']
        elif column == 'transferencias_recibidas':
            return row['transferencias_recibidas']
        elif column == 'transferencias_realizadas':
            return row['transferencias_realizadas']
        elif column == 'abandonos':
            return row['abandonos']
        elif column == 'promedio':
            return row['promedio']
        elif column == 'duracion_llamada':
            formato = '%H:%M:%S'
            h1 = str(row.hora_inicio.hour) + ':' + str(row.hora_inicio.minute) + ':' + str(row.hora_inicio.second)
            h2 = str(row.hora_fin.hour) + ':' + str(row.hora_fin.minute) + ':' + str(row.hora_fin.second)
            h1 = datetime.strptime(h1, formato)
            h2 = datetime.strptime(h2, formato)
            return str(h2-h1)

        return super(ProductividadAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        current_time = datetime.now()
        llamadas = Llamada.objects.all()
        queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
            tiempo_servicio=Sum('duracion_minutos')).annotate(
            abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
            promedio=Avg('duracion_minutos')).annotate(
            transferencias_recibidas=Count('transferencia',filter=Q(recibido=True))).annotate(
            transferencias_realizadas=Count('transferencia',filter=Q(transferencia=True))).annotate(
            llamadas_atendidas=Count('fecha', filter=Q(fecha__month__gte=current_time.month,
                                                       fecha__month__lte=current_time.month)))
        return queryset

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        dia = self.request.GET.get('dia', None)
        mes = self.request.GET.get(u'mes', None)
        fecha1 = self.request.GET.get(u'fecha1', None)
        fecha2 = self.request.GET.get(u'fecha2', None)
        llamadas = Llamada.objects.all()
        queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
            tiempo_servicio=Sum('duracion_minutos')).annotate(
            abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
            promedio=Avg('duracion_minutos')).annotate(
            transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
            transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
            llamadas_atendidas=Count('fecha'))
        if dia:
            datetime_object = datetime.strptime(dia, '%Y-%m-%d')
            llamadas = llamadas.filter(fecha=datetime_object)
            queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
                tiempo_servicio=Sum('duracion_minutos')).annotate(
                abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
                promedio=Avg('duracion_minutos')).annotate(
                transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
                transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
                llamadas_atendidas=Count('fecha')).order_by('consejero')
            return queryset
        elif mes:
            llamadas = llamadas.filter(fecha__month=mes)
        elif fecha1 and fecha2:
            fecha_inicio = datetime.strptime(fecha1, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha2, '%Y-%m-%d')
            llamadas = llamadas.filter(fecha__range=(fecha_inicio, fecha_fin))
        if search=='tyty':
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
            queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
                tiempo_servicio=Sum('duracion_minutos')).annotate(
                abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
                promedio=Avg('duracion_minutos')).annotate(
                transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
                transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
                llamadas_atendidas=Count('fecha'))
        return queryset
