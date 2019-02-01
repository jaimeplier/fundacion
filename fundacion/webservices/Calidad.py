from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from webservices.serializers import RubrosSerializer


class EvaluarServicio(APIView):

    def post(self, request):
        serializer = RubrosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return RubrosSerializer()