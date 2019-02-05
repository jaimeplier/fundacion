from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada, Mensaje, Recado
from webservices.serializers import FechaSerializer, MensajeSerializer, MensajeSerializerPk, RecadoSerializer, \
    RecadoSerializerPk


class ResumenLlamada(APIView):

    def post(self, request):
        serializer = FechaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tipo = serializer.validated_data['tipo']
        if tipo == 'dia':
            dia = serializer.validated_data['fecha']
            llamadas_dia = Llamada.objects.filter(fecha__date = dia)
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