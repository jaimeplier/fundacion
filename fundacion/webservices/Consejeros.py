from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada, Victima, EstadoCivil, Municipio, Ocupacion, Religion, ViveCon, Sexo, NivelEstudio, \
    LenguaIndigena, Consejero, MedioContacto, Violentometro, TipoViolencia, AcudeInstitucion, TipoLlamada, \
    MotivoLLamada, EstadoMental, NivelRiesgo, EstatusLLamada
from webservices.serializers import PrimeraVezSerializer


class PrimerRegistro(APIView):

    def post(self, request):
        serializer = PrimeraVezSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # ---> DATOS VICTIMA <---

            telefono = serializer.validated_data['telefono']
            nombre = serializer.validated_data['nombre']
            apellido_paterno = serializer.data['apellido_paterno']
            apellido_materno = serializer.data['apellido_materno']
            estado_civil = EstadoCivil.objects.filter(pk=serializer.data['estado_civil']).first()
            municipio = Municipio.objects.filter(pk=serializer.data['municipio']).first()
            ocupacion = Ocupacion.objects.filter(pk=serializer.data['ocupacion']).first()
            religion = Religion.objects.filter(pk=serializer.data['religion']).first()
            vive_con = ViveCon.objects.filter(pk=serializer.data['vive_con']).first()
            sexo = Sexo.objects.filter(pk=serializer.data['sexo']).first()
            nivel_estudio = NivelEstudio.objects.filter(pk=serializer.data['nivel_estudio']).first()
            lengua_indigena = LenguaIndigena.objects.filter(pk=serializer.data['lengua_indigena']).first()

            # ---> DATOS DE LA LLAMADA <---

            hora_inicio = '14:00'
            hora_fin = '14:20'
            consejero = Consejero.objects.get(pk=self.request.user.pk)
            f = serializer.data['f']
            o = serializer.data['o']
            d = serializer.data['d']
            a = serializer.data['a']
            medio_contacto = MedioContacto.objects.get(pk=serializer.validated_data['medio_contacto'])
            violentometro = Violentometro.objects.filter(pk=serializer.validated_data['violentometro']).first()
            tipo_caso = serializer.validated_data['tipo_caso']
            tipo_ayuda = serializer.validated_data['tipo_ayuda']
            tipo_violencia = TipoViolencia.objects.filter(pk=serializer.validated_data['tipo_violencia']).first()
            institucion = AcudeInstitucion.objects.filter(serializer.validated_data['institucion']).first()
            posible_solucion = serializer.data['posible_solucion']
            vida_en_riesgo = serializer.validated_data['vida_en_riesgo']
            tipo_llamada = TipoLlamada.objects.get(pk=1)  # llamada de primera vez
            motivo_llamada = MotivoLLamada.objects.filter(pk=serializer.validated_data['motivo_llamada']).first()
            estado_mental = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental'])
            nivel_riesgo = NivelRiesgo.objects.get(pk=serializer.validated_data['nivel_riesgo'])
            estatus = EstatusLLamada.objects.get(pk=serializer.validated_data['estatus'])

        except:
            response_data = {}
            response_data['error'] = 'Datos erroneos'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # ---> REGISTRO DE VICTIMA <---

        victima = Victima.objects.create(nombre=nombre, telefono=telefono, apellido_paterno=apellido_paterno,
                                         apellido_materno=apellido_materno, estado_civil=estado_civil,
                                         municipio=municipio, ocupacion=ocupacion, religion=religion, vive_con=vive_con,
                                         sexo=sexo, nivel_estudio=nivel_estudio, lengua_indigena=lengua_indigena)

        # ---> REGISTRO DE VICTIMA <---

        llamada = Llamada.objects.create(hora_inicio=hora_inicio, hora_fin=hora_fin, consejero=consejero,
                                         victima=victima, f=f, o=o, d=d, a=a, medio_contacto=medio_contacto,
                                         violentometro=violentometro, tipo_caso=tipo_caso, tipo_ayuda=tipo_ayuda,
                                         tipo_violencia=tipo_violencia, institucion=institucion,
                                         posible_solucion=posible_solucion, vida_en_riesgo=vida_en_riesgo,
                                         tipo_llamada=tipo_llamada, motivo_llamada=motivo_llamada,
                                         estado_mental=estado_mental, nivel_riesgo=nivel_riesgo, estatus=estatus)

        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)

    # else:
    # response_data = {}
    # response_data['error'] = 'Datos erroneos'
    # return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self):
        return PrimeraVezSerializer()
