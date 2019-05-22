from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum, Count, Avg, Q
from django.shortcuts import render

# Create your views here.
from django_datatables_view.base_datatable_view import BaseDatatableView
from pytz import timezone

from config.models import Llamada, Consejero, LlamadaCanalizacion
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
    columns = ['id', 'victima.nombre', 'nombre', 'fecha', 'hora_inicio', 'hora_fin', 'duracion_llamada', 'vida_en_riesgo', 'tipo_violencia', 'instituciones', 'medio_contacto']
    order_columns = ['id', 'victima__nombre', 'fecha', 'consejero.a_paterno', 'hora_inicio', 'hora_fin', '', 'vida_en_riesgo', 'tipo_violencia', '', 'estatus__nombre', 'medio_contacto']
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
        elif column=='instituciones':
            canalizaciones = LlamadaCanalizacion.objects.filter(llamada__pk=row.pk)
            if canalizaciones.count() >0:
                canalizaciones_str = ''
                for canalizacion in canalizaciones:
                    canalizaciones_str += canalizacion.institucion.nombre + '<br>'
                return canalizaciones_str
            return 'Sin canalización'

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
            tiempo_servicio=Sum('duracion_servicio')).annotate(
            abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
            promedio=Avg('duracion_servicio')).annotate(
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
            tiempo_servicio=Sum('duracion_servicio')).annotate(
            abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
            promedio=Avg('duracion_servicio')).annotate(
            transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
            transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
            llamadas_atendidas=Count('fecha'))
        if dia:
            datetime_object = datetime.strptime(dia, '%Y-%m-%d')
            llamadas = llamadas.filter(fecha=datetime_object)
            queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
                tiempo_servicio=Sum('duracion_servicio')).annotate(
                abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
                promedio=Avg('duracion_servicio')).annotate(
                transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
                transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
                llamadas_atendidas=Count('fecha')).order_by('consejero')
        elif mes:
            llamadas = llamadas.filter(fecha__month=mes)
            queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
                tiempo_servicio=Sum('duracion_servicio')).annotate(
                abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
                promedio=Avg('duracion_servicio')).annotate(
                transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
                transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
                llamadas_atendidas=Count('fecha')).order_by('consejero')
        elif fecha1 and fecha2:
            fecha_inicio = datetime.strptime(fecha1, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha2, '%Y-%m-%d')
            llamadas = llamadas.filter(fecha__range=(fecha_inicio, fecha_fin))
            queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
                tiempo_servicio=Sum('duracion_servicio')).annotate(
                abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
                promedio=Avg('duracion_servicio')).annotate(
                transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
                transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
                llamadas_atendidas=Count('fecha')).order_by('consejero')
        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
            queryset = llamadas.values('consejero').annotate(total_llamadas=Count('fecha')).annotate(
                tiempo_servicio=Sum('duracion_servicio')).annotate(
                abandonos=Count('tipo_llamada', filter=Q(motivo__pk__in=[3, 6]))).annotate(
                promedio=Avg('duracion_servicio')).annotate(
                transferencias_recibidas=Count('transferencia', filter=Q(recibido=True))).annotate(
                transferencias_realizadas=Count('transferencia', filter=Q(transferencia=True))).annotate(
                llamadas_atendidas=Count('fecha'))
        return queryset

class GeneralAjaxList(PermissionRequiredMixin, BaseDatatableView):
    redirect_field_name = 'next'
    login_url = '/'
    permission_required = 'supervisor'

    model = Llamada
    columns = ['id', 'victima.nombre', 'nombre', 'hora_inicio', 'hora_fin', 'duracion_llamada', 'vida_en_riesgo', 'tipo_violencia', 'instituciones', 'medio_contacto.nombre']
    order_columns = ['id', 'victima__nombre', 'consejero.a_paterno', 'hora_inicio', 'hora_fin', '', 'vida_en_riesgo', 'tipo_violencia', 'estatus', '', 'medio_contacto.nombre']
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
        elif column=='instituciones':
            canalizaciones = LlamadaCanalizacion.objects.filter(llamada__pk=row.pk)
            if canalizaciones.count() >0:
                canalizaciones_str = ''
                for canalizacion in canalizaciones:
                    canalizaciones_str += canalizacion.institucion.nombre + '<br>'
                return canalizaciones_str
            return 'Sin canalización'
        elif column == 'duracion_llamada':
            formato = '%H:%M:%S'
            h1 = str(row.hora_inicio.hour) + ':' + str(row.hora_inicio.minute) + ':' + str(row.hora_inicio.second)
            h2 = str(row.hora_fin.hour) + ':' + str(row.hora_fin.minute) + ':' + str(row.hora_fin.second)
            h1 = datetime.strptime(h1, formato)
            h2 = datetime.strptime(h2, formato)
            return str(h2-h1)

        return super(GeneralAjaxList, self).render_column(row, column)

    def get_initial_queryset(self):
        return Llamada.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        dia = self.request.GET.get(u'dia', None)
        mes = self.request.GET.get(u'mes', None)
        fecha1 = self.request.GET.get(u'fecha1', None)
        fecha2 = self.request.GET.get(u'fecha2', None)
        sexo = self.request.GET.get(u'sexo', None)
        ocupacion = self.request.GET.get(u'ocupacion', None)
        estado_civil = self.request.GET.get(u'estado_civil', None)
        nivel_academico = self.request.GET.get(u'nivel_academico', None)
        como_se_entero = self.request.GET.get(u'como_se_entero', None)
        contacto = self.request.GET.get(u'contacto', None)
        tipo_caso = self.request.GET.get(u'tipo_caso', None)
        consejero = self.request.GET.get(u'consejero', None)
        if dia:
            datetime_object = datetime.strptime(dia, '%Y-%m-%d')
            qs = qs.filter(fecha=datetime_object)
        if mes:
            qs = qs.filter(fecha__month=mes)
        if fecha1 and fecha2:
            fecha_inicio = datetime.strptime(fecha1, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha2, '%Y-%m-%d')
            qs = qs.filter(fecha__range=(fecha_inicio, fecha_fin))
        if sexo:
            qs = qs.filter(victima__sexo__pk=sexo)
        if ocupacion:
            qs = qs.filter(victima__ocupacion__pk=ocupacion)
        if estado_civil:
            qs = qs.filter(victima__estado_civil__pk=estado_civil)
        if nivel_academico:
            qs = qs.filter(victima__nivel_estudio__pk=nivel_academico)
        if como_se_entero:
            qs = qs.filter(como_se_entero__pk=como_se_entero)
        if contacto:
            qs = qs.filter(medio_contacto__pk=contacto)
        if tipo_caso:
            qs = qs.filter(tipificacionllamada__categoria_tipificacion__pk=tipo_caso)
        if consejero:
            qs = qs.filter(consejero__pk=consejero)

        if search:
            qs = qs.filter(nombre__icontains=search) | qs.filter(pk__icontains=search)
        return qs