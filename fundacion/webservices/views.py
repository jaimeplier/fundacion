from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Sum, Count, Avg, Q
from config.models import Llamada, Mensaje, Recado, Usuario, EstatusUsuario, ArchivoMensaje, AcudeInstitucion, \
    EstatusInstitucion, Sucursal, Consejero, LlamadaCanalizacion, Pendiente
from webservices.serializers import FechaSerializer, MensajeSerializer, MensajeSerializerPk, RecadoSerializer, \
    RecadoSerializerPk, UsuarioSerializer, EstatusUsuarioSerializer, PkSerializer, ArchivoMensajeSerializer, \
    ArchivoRecadoSerializer, EstatusInstitucionSucursalSerializer, FechaSerializerMes, UsuariosAjaxListSerializer

class ResumenLlamada(APIView):

    def post(self, request):
        serializer = FechaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        fecha = serializer.data.get('fecha')
        llamadas = Llamada.objects.filter(fecha__exact=fecha)
        llamadas_entrantes = llamadas.count()
        usuarios = llamadas.values('victima').distinct().count()
        consejeros = Consejero.objects.all().count()
        ids_llamadas = llamadas.values_list('pk', flat=True)
        canalizaciones = LlamadaCanalizacion.objects.filter(llamada__pk__in=ids_llamadas).count()
        return Response({'llamadas_entrantes': llamadas_entrantes, 'usuarios': usuarios, 'consejeros': consejeros,
                         'canalizaciones': canalizaciones}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return FechaSerializer()


class ResumenLlamadaMes(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = FechaSerializerMes

    def get_queryset(self):

        mes = self.request.query_params.get('mes', None)
        anio = self.request.query_params.get('anio', None)
        if mes and anio:

            llamadas_mes = Llamada.objects.filter(fecha__year__gte=anio, fecha__month__gte=mes,
                                                  fecha__year__lte=anio, fecha__month__lte=mes)
            queryset = llamadas_mes.values('fecha').annotate(n_servicios=Count('fecha')).order_by('fecha')
            return queryset
        current_time = datetime.now()
        llamadas_mes = Llamada.objects.filter(fecha__year__gte=current_time.year, fecha__month__gte=current_time.month,
                               fecha__year__lte=current_time.year, fecha__month__lte=current_time.month)
        return llamadas_mes.values('fecha').annotate(n_servicios=Count('fecha')).order_by('fecha')


class MensajesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Mensaje.objects.all()

    def list(self, request):
        qs = Mensaje.objects.filter(usuario=self.request.user) | Mensaje.objects.filter(
            destinatarios=self.request.user)
        serializer = MensajeSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = MensajeSerializerPk(data=self.request.data)
        if serializer.is_valid():
            serializer.save(usuario=self.request.user)
            return Response({'id': serializer.instance.pk, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Mensaje.objects.all()
        mensaje = get_object_or_404(queryset, pk=pk)
        mensaje.leido = True
        mensaje.save()
        serializer = MensajeSerializer(mensaje)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request is None or self.request.method == 'POST':
            return MensajeSerializerPk
        else:
            return MensajeSerializer


class RecadosViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Recado.objects.all()

    def list(self, request):
        qs = Recado.objects.filter(usuario=self.request.user) or Recado.objects.filter(
            destinatarios=self.request.user
        )
        serializer = RecadoSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = RecadoSerializerPk(data=self.request.data)
        if serializer.is_valid():
            serializer.save(usuario=self.request.user)
            return Response({'id': serializer.instance.pk, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Recado.objects.all()
        recado = get_object_or_404(queryset, pk=pk)
        recado.leido = True
        recado.save()
        serializer = RecadoSerializer(recado)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request is None or self.request.method == 'POST':
            return RecadoSerializerPk
        else:
            return RecadoSerializer


class ListUsuarios(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = UsuarioSerializer

    def get_queryset(self):
        queryset = Usuario.objects.all()
        return queryset


class ListEstatusActividadUsuario(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = EstatusUsuarioSerializer

    def get_queryset(self):
        queryset = EstatusUsuario.objects.filter(estatus=True)
        return queryset


class UpdateEstatusActividadUsuario(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        serializer = PkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        estatus_pk = serializer.validated_data['pk']
        try:
            estatus = EstatusUsuario.objects.get(pk=estatus_pk)
            usuario = Usuario.objects.get(pk=request.user.pk)
            usuario.estatus_actividad = estatus
            usuario.save()
            return Response(status=status.HTTP_200_OK)
        except:
            response_data = {}
            response_data['error'] = 'Selecciona un estatus'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self):
        return PkSerializer()


class AgregaArchivoMensaje(CreateAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArchivoMensajeSerializer


class AgregaArchivoRecado(CreateAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArchivoRecadoSerializer


class ListArchivoMensaje(ListAPIView):
    """
    **Búsqueda de archivos en mensajes**

    1. id_mensaje: número entero del ID del mensaje

    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArchivoMensajeSerializer

    def get_queryset(self):
        pk_mensaje = self.request.query_params.get('id_mensaje', None)
        queryset = ArchivoMensaje.objects.none()
        if pk_mensaje is not None:
            queryset = ArchivoMensaje.objects.filter(mensaje__pk=pk_mensaje)
        return queryset


class ListArchivoRecado(ListAPIView):
    """
    **Búsqueda de archivos en recados**

    1. id_recado: número entero del ID del mensaje

    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ArchivoRecadoSerializer

    def get_queryset(self):
        pk_recado = self.request.query_params.get('id_recado', None)
        queryset = ArchivoMensaje.objects.none()
        if pk_recado is not None:
            queryset = ArchivoMensaje.objects.filter(mensaje__pk=pk_recado)
        return queryset

class CambiarEstatusInstitucion(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        serializer = EstatusInstitucionSucursalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_institucion = serializer.data.get('pk')
        id_estatus = serializer.data.get('estatus')
        tipo = serializer.data.get('tipo')

        try:
            if tipo == 0:
                institucion = AcudeInstitucion.objects.get(pk= id_institucion)
                estatus = EstatusInstitucion.objects.get(pk=id_estatus)
                institucion.estatus_institucion = estatus
                institucion.save()
            elif tipo == 1:
                sucursal = Sucursal.objects.get(pk=id_institucion)
                estatus = EstatusInstitucion.objects.get(pk=id_estatus)
                sucursal.estatus_institucion = estatus
                sucursal.save()

        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return EstatusInstitucionSucursalSerializer()

class CountPendientes(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):
        usuario = self.request.user
        pendientes = Pendiente.objects.filter(usuario = usuario, completado=False).count()
        return Response({'cantidad': pendientes})

class ReporteUsuarioViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):
        dia = self.request.query_params.get('dia', None)
        mes = self.request.query_params.get('mes', None)
        anio = self.request.query_params.get('anio', None)
        fecha1 = self.request.query_params.get('fecha1', None)
        fecha2 = self.request.query_params.get('fecha2', None)

        if dia:
            datetime_object = datetime.strptime(dia, '%Y-%m-%d')
            queryset = Llamada.objects.filter(fecha=datetime_object).aggregate(
                total_usuarios=Count('victima', distinct=True),
                primera_vez=Count('motivo', filter=Q(motivo__pk=8)),
                seguimiento=Count('motivo', filter=Q(motivo__pk=9)),
                total_servicios=Count('pk'))
        elif mes and anio:
            queryset = Llamada.objects.filter(fecha__month=mes, fecha__year=anio).aggregate(
                total_usuarios=Count('victima', distinct=True),
                primera_vez=Count('motivo', filter=Q(motivo__pk=8)),
                seguimiento=Count('motivo', filter=Q(motivo__pk=9)),
                total_servicios=Count('pk'))
        elif fecha1 and fecha2:
            fecha_inicio = datetime.strptime(fecha1, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha2, '%Y-%m-%d')
            queryset = Llamada.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(
                total_usuarios=Count('victima', distinct=True),
                primera_vez=Count('motivo', filter=Q(motivo__pk=8)),
                seguimiento=Count('motivo', filter=Q(motivo__pk=9)),
                total_servicios=Count('pk'))
        else:
            queryset = Llamada.objects.all().aggregate(
                total_usuarios=Count('victima', distinct=True),
                primera_vez=Count('motivo', filter=Q(motivo__pk=8)),
                seguimiento=Count('motivo', filter=Q(motivo__pk=9)),
                total_servicios=Count('pk'))

        return Response({'data':[[queryset['total_usuarios'], queryset['primera_vez'], queryset['seguimiento'],
                                 queryset['total_servicios']]]})


    def get_serializer(self):
        return UsuariosAjaxListSerializer()
