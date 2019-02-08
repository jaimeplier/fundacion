from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada, Mensaje, Recado, Usuario, EstatusUsuario, ArchivoMensaje
from webservices.serializers import FechaSerializer, MensajeSerializer, MensajeSerializerPk, RecadoSerializer, \
    RecadoSerializerPk, UsuarioSerializer, EstatusUsuarioSerializer, PkSerializer, ArchivoMensajeSerializer, \
    ArchivoRecadoSerializer


class ResumenLlamada(APIView):

    def post(self, request):
        serializer = FechaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tipo = serializer.validated_data['tipo']
        if tipo == 'dia':
            dia = serializer.validated_data['fecha']
            llamadas_dia = Llamada.objects.filter(fecha__date=dia)
            return Response(llamadas_dia, status=status.HTTP_200_OK)
        elif tipo == 'mes':
            year = serializer.validated_data['anio']
            month = serializer.validated_data['mes']

            llamadas_mes = Llamada.objects.filter(fecha__year__gte=year, fecha__month__gte=month,
                                                  fecha__year__lte=year, fecha__month__lte=month, accion__pk=1)
            return Response(llamadas_mes, status=status.HTTP_200_OK)
        elif tipo == 'rango':
            dia = serializer.validated_data['fecha']
            dia_fin = serializer.validated_data['fecha_fin']
            llamadas_rango = Llamada.objects.filter(fecha__range=[dia, dia_fin])
            return Response(llamadas_rango, status=status.HTTP_200_OK)
        else:
            response_data = {}
            response_data['error'] = 'Datos erroneos'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self):
        return FechaSerializer()


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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        qs = Recado.objects.filter(usuario=self.request.user) | Recado.objects.filter(
            destinatarios=self.request.user)
        serializer = RecadoSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = RecadoSerializerPk(data=self.request.data)
        if serializer.is_valid():
            serializer.save(usuario=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

