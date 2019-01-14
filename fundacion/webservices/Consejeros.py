from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada, Victima, EstadoCivil, Municipio, Ocupacion, Religion, ViveCon, Sexo, NivelEstudio, \
    LenguaIndigena
from webservices.serializers import PrimeraVezSerializer


class PrimerRegistro(APIView):

    def post(self, request):
        serializer = PrimeraVezSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Datos victima
        telefono = serializer.validated_data['telefono']
        nombre = serializer.validated_data['nombre']
        apellido_paterno = serializer.data['apellido_paterno']
        apellido_materno = serializer.data['apellido_materno']
        estado_civil = EstadoCivil.objects.filter(pk = serializer.data['estado_civil']).first()
        municipio = Municipio.objects.filter(pk = serializer.data['municipio']).first()
        ocupacion = Ocupacion.objects.filter(pk = serializer.data['ocupacion']).first()
        religion = Religion.objects.filter(pk=serializer.data['religion']).first()
        vive_con = ViveCon.objects.filter(pk=serializer.data['vive_con']).first()
        sexo = Sexo.objects.filter(pk=serializer.data['sexo']).first()
        nivel_estudio = NivelEstudio.objects.filter(pk=serializer.data['nivel_estudio']).first()
        lengua_indigena = LenguaIndigena.objects.filter(pk=serializer.data['lengua_indigena']).first()

        victima = Victima.objects.create(nombre=nombre, telefono=telefono, apellido_paterno=apellido_paterno,
                                         apellido_materno=apellido_materno, estado_civil=estado_civil,
                                         municipio=municipio, ocupacion=ocupacion, religion=religion, vive_con=vive_con,
                                         sexo=sexo, nivel_estudio=nivel_estudio, lengua_indigena=lengua_indigena)

        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)

    # else:
    # response_data = {}
    # response_data['error'] = 'Datos erroneos'
    # return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer(self):
        return PrimeraVezSerializer()
