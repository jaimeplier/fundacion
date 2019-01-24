from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada, Victima, EstadoCivil, Municipio, Ocupacion, Religion, ViveCon, Sexo, NivelEstudio, \
    LenguaIndigena, Consejero, MedioContacto, Violentometro, TipoViolencia, AcudeInstitucion, TipoLlamada, \
    MotivoLLamada, EstadoMental, NivelRiesgo, EstatusLLamada, CategoriaTipificacion, TipificacionLLamada, RedesApoyo
from config.permissions import ConsejeroPermission
from webservices.serializers import PrimeraVezSerializer, SeguimientoSerializer, ConsejeroSerializer, LLamadaSerializer


class PrimerRegistro(APIView):
    permission_classes = (IsAuthenticated, ConsejeroPermission)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        serializer = PrimeraVezSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

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
        redes_apoyo = RedesApoyo.objects.filter(pk=serializer.data['redes_apoyo']).first()

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
        tipo_caso = serializer.data['tipo_caso']
        tipo_ayuda = serializer.data['tipo_ayuda']
        tipo_violencia = TipoViolencia.objects.filter(pk=serializer.validated_data['tipo_violencia']).first()
        institucion = AcudeInstitucion.objects.filter(pk=serializer.validated_data['institucion']).first()
        posible_solucion = serializer.data['posible_solucion']
        vida_en_riesgo = serializer.validated_data['vida_en_riesgo']
        tipo_llamada = TipoLlamada.objects.get(pk=1)  # llamada de primera vez
        motivo_llamada = MotivoLLamada.objects.filter(pk=serializer.validated_data['motivo_llamada']).first()
        estado_mental = EstadoMental.objects.filter(pk=serializer.data['estado_mental']).first()
        nivel_riesgo = NivelRiesgo.objects.filter(pk=serializer.data['nivel_riesgo']).first()
        estatus = EstatusLLamada.objects.get(pk=serializer.validated_data['estatus'])
        causa_riesgo = serializer.data['causa_riesgo']

        # ---> DATOS DE LA TIPIFICACION <---

        cat_tipificacion = CategoriaTipificacion.objects.get(pk=serializer.validated_data['categoria_tipificacion'])
        descripcion_tipificacion = serializer.validated_data['descripcion_tipificacion']


        # ---> REGISTRO DE VICTIMA <---

        victima = Victima.objects.create(nombre=nombre, telefono=telefono, apellido_paterno=apellido_paterno,
                                         apellido_materno=apellido_materno, estado_civil=estado_civil,
                                         municipio=municipio, ocupacion=ocupacion, religion=religion, vive_con=vive_con,
                                         sexo=sexo, nivel_estudio=nivel_estudio, lengua_indigena=lengua_indigena, redes_apoyo=redes_apoyo)

        # ---> REGISTRO DE LLAMADA <---

        llamada = Llamada.objects.create(hora_inicio=hora_inicio, hora_fin=hora_fin, consejero=consejero,
                                         victima=victima, f=f, o=o, d=d, a=a, medio_contacto=medio_contacto,
                                         violentometro=violentometro, tipo_caso=tipo_caso, tipo_ayuda=tipo_ayuda,
                                         tipo_violencia=tipo_violencia, institucion=institucion,
                                         posible_solucion=posible_solucion, vida_en_riesgo=vida_en_riesgo,
                                         tipo_llamada=tipo_llamada, motivo=motivo_llamada,
                                         estado_mental=estado_mental, nivel_riesgo=nivel_riesgo, estatus=estatus,
                                         causa_riesgo=causa_riesgo)

        # ---> REGISTRO DE LLAMADA TIPIFICACION <---

        llamada_tipifificacion = TipificacionLLamada.objects.create(llamada=llamada, categoria_tipificacion=cat_tipificacion,
                                                                    descripcion=descripcion_tipificacion)

        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return PrimeraVezSerializer()

class SeguimientoRegistro(APIView):
    permission_classes = (IsAuthenticated, ConsejeroPermission)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        serializer = SeguimientoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ---> DATOS DE LA LLAMADA <---

        hora_inicio = '14:00'
        hora_fin = '14:20'
        consejero = Consejero.objects.get(pk=self.request.user.pk)
        victima = Victima.objects.get(pk=serializer.validated_data['victima'])
        f = serializer.data['f']
        o = serializer.data['o']
        d = serializer.data['d']
        a = serializer.data['a']
        medio_contacto = MedioContacto.objects.get(pk=serializer.validated_data['medio_contacto'])
        violentometro = Violentometro.objects.filter(pk=serializer.validated_data['violentometro']).first()
        tipo_caso = serializer.data['tipo_caso']
        tipo_ayuda = serializer.data['tipo_ayuda']
        tipo_violencia = TipoViolencia.objects.filter(pk=serializer.validated_data['tipo_violencia']).first()
        institucion = AcudeInstitucion.objects.filter(pk=serializer.validated_data['institucion']).first()
        posible_solucion = serializer.data['posible_solucion']
        vida_en_riesgo = serializer.validated_data['vida_en_riesgo']
        tipo_llamada = TipoLlamada.objects.get(pk=1)  # llamada de primera vez
        motivo_llamada = MotivoLLamada.objects.filter(pk=serializer.validated_data['motivo_llamada']).first()
        estado_mental = EstadoMental.objects.filter(pk=serializer.data['estado_mental']).first()
        nivel_riesgo = NivelRiesgo.objects.filter(pk=serializer.data['nivel_riesgo']).first()
        estatus = EstatusLLamada.objects.get(pk=serializer.validated_data['estatus'])
        causa_riesgo = serializer.data['causa_riesgo']

        # ---> DATOS DE LA TIPIFICACION <---

        cat_tipificacion = CategoriaTipificacion.objects.get(pk=serializer.validated_data['categoria_tipificacion'])
        descripcion_tipificacion = serializer.validated_data['descripcion_tipificacion']


        # ---> REGISTRO DE LLAMADA <---

        llamada = Llamada.objects.create(hora_inicio=hora_inicio, hora_fin=hora_fin, consejero=consejero,
                                         victima=victima, f=f, o=o, d=d, a=a, medio_contacto=medio_contacto,
                                         violentometro=violentometro, tipo_caso=tipo_caso, tipo_ayuda=tipo_ayuda,
                                         tipo_violencia=tipo_violencia, institucion=institucion,
                                         posible_solucion=posible_solucion, vida_en_riesgo=vida_en_riesgo,
                                         tipo_llamada=tipo_llamada, motivo=motivo_llamada,
                                         estado_mental=estado_mental, nivel_riesgo=nivel_riesgo, estatus=estatus,
                                         causa_riesgo=causa_riesgo)

        # ---> REGISTRO DE LLAMADA TIPIFICACION <---

        llamada_tipifificacion = TipificacionLLamada.objects.create(llamada=llamada, categoria_tipificacion=cat_tipificacion,
                                                                    descripcion=descripcion_tipificacion)

        return Response({'exito': 'registro exitoso'}, status=status.HTTP_200_OK)


    def get_serializer(self):
        return SeguimientoSerializer()

class ListConsejerosVictima(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = ConsejeroSerializer

    def get_queryset(self):
        victima = self.request.query_params.get('victima', None)
        queryset = Consejero.objects.none()
        if victima is not None:
            consejeros_list = Llamada.objects.filter(victima__pk=victima).values_list('consejero__pk', flat=True)
            queryset = Consejero.objects.filter(pk__in=consejeros_list)
        return queryset

class ListHistorialLLamada(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = LLamadaSerializer

    def get_queryset(self):
        victima = self.request.query_params.get('victima', None)
        consejero = self.request.query_params.get('consejero', None)
        f_inicio = self.request.query_params.get('f_inicio', None)
        f_fin = self.request.query_params.get('f_fin', None)
        queryset = Consejero.objects.none()
        if victima is not None and f_inicio is not None and f_fin is not None and consejero is not None:
            consejeros_list = Llamada.objects.filter(victima__pk=victima).values_list('consejero__pk', flat=True)
            queryset = Llamada.objects.filter(victima__pk=victima, consejero=consejero, fecha__range=[f_inicio, f_fin])
        return queryset

class UltimaLLamada(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = LLamadaSerializer

    def get_queryset(self):
        victima = self.request.query_params.get('victima', None)
        queryset = Llamada.objects.none()
        if victima is not None:
            ultima_llamada = Llamada.objects.filter(victima__pk=victima).order_by('-fecha').first()
            queryset = Llamada.objects.filter(pk=ultima_llamada.pk)
        return queryset