from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada
from webservices.serializers import FechaSerializer


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