from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada, ComentarioLlamada, CompromisoLlamada
from config.permissions import CalidadPermission
from webservices.serializers import RubrosSerializer, ComentarioLlamadaSerializer


class EvaluarServicio(APIView):

    def post(self, request):
        serializer = RubrosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return RubrosSerializer()

class ComentarioServicio(APIView):
    permission_classes = (IsAuthenticated, CalidadPermission)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        serializer = ComentarioLlamadaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ComentarioLlamadaSerializer()