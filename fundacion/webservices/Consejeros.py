from django.db.models import Max
from django.http import Http404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Llamada, Victima, EstadoCivil, Municipio, Ocupacion, Religion, ViveCon, Sexo, NivelEstudio, \
    LenguaIndigena, Consejero, MedioContacto, Violentometro, TipoViolencia, AcudeInstitucion, TipoLlamada, \
    MotivoLLamada, EstadoMental, NivelRiesgo, EstatusLLamada, CategoriaTipificacion, TipificacionLLamada, RedesApoyo, \
    FaseCambio, ExamenMental, ModalidadViolencia, FaseViolencia, Semaforo, Agresor, ComoSeEntero, TareaLLamada, \
    VictimaInvolucrada, LineaNegocio, Aliado, LlamadaCanalizacion
from config.permissions import ConsejeroPermission
from webservices.serializers import PrimeraVezSerializer, SeguimientoSerializer, ConsejeroSerializer, LLamadaSerializer, \
    BusquedaSerializer, VictimaSerializer


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
        num_hijos_menores = serializer.data['num_hijos_menores']
        num_hijos_mayores = serializer.data['num_hijos_mayores']
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
        debilidades = serializer.data['debilidades']
        amenazas = serializer.data['amenazas']
        recursos = serializer.data['recursos']
        intervencion = serializer.data['intervencion']
        fase_cambio = FaseCambio.objects.get(pk=serializer.data['fase_cambio'])
        medio_contacto = MedioContacto.objects.get(pk=serializer.validated_data['medio_contacto'])
        violentometro = Violentometro.objects.filter(pk=serializer.validated_data['violentometro']).first()
        tipo_caso = serializer.data['tipo_caso']
        tipo_ayuda = serializer.data['tipo_ayuda']
        tipo_violencia = TipoViolencia.objects.filter(pk=serializer.validated_data['tipo_violencia']).first()
        posible_solucion = serializer.data['posible_solucion']
        vida_en_riesgo = serializer.validated_data['vida_en_riesgo']
        tipo_llamada = TipoLlamada.objects.get(pk=1)  # llamada de primera vez
        motivo_llamada = MotivoLLamada.objects.filter(pk=serializer.validated_data['motivo_llamada']).first()
        nivel_riesgo = NivelRiesgo.objects.filter(pk=serializer.data['nivel_riesgo']).first()
        estatus = EstatusLLamada.objects.get(pk=serializer.validated_data['estatus'])
        causa_riesgo = serializer.data['causa_riesgo']
        modalidad_violencia = ModalidadViolencia.objects.get(pk=serializer.data['modalidad_violencia'])
        fase_violencia = FaseViolencia.objects.get(pk=serializer.data['fase_violencia'])
        semaforo = Semaforo.objects.get(pk=serializer.data['semaforo'])
        victimas = VictimaInvolucrada.objects.get(pk=serializer.data['victimas'])
        agresor = Agresor.objects.get(pk=serializer.data['agresor'])
        como_se_entero = ComoSeEntero.objects.get(pk=serializer.data['como_se_entero'])
        devolver_llamada = serializer.validated_data['devolver_llamada']
        linea_negocio = LineaNegocio.objects.filter(pk=serializer.data['linea_negocio']).first()
        aliado = Aliado.objects.filter(pk=serializer.data['aliado']).first()
        num_llamada = 0

        num_hijos_menores = num_hijos_menores if num_hijos_menores is not None else 0
        num_hijos_mayores = num_hijos_mayores if num_hijos_mayores is not None else 0

        if motivo_llamada.pk == 8:
            num_llamada = 1

        # Tareas
        tarea1 = serializer.data['tarea1']
        tarea2 = serializer.data['tarea2']
        tarea3 = serializer.data['tarea3']

        # ---> DATOS DE LA TIPIFICACION <---

        cat_tipificacion = CategoriaTipificacion.objects.get(pk=serializer.validated_data['categoria_tipificacion'])

        # ---> Datos del examen mental <---

        em_ute = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_ute'])
        em_p = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_p'])
        em_l = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_l'])
        em_m = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_m'])
        em_a = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_a'])

        # ---> Datos de las canalizaciones a instituciones <---

        institucion = AcudeInstitucion.objects.filter(pk=serializer.validated_data['institucion']).first()
        institucion2 = AcudeInstitucion.objects.filter(pk=serializer.validated_data['institucion2']).first()

        # ---> REGISTRO DE VICTIMA <---

        victima = Victima.objects.create(nombre=nombre, telefono=telefono, apellido_paterno=apellido_paterno,
                                         apellido_materno=apellido_materno, estado_civil=estado_civil,
                                         municipio=municipio, ocupacion=ocupacion, religion=religion, vive_con=vive_con,
                                         sexo=sexo, nivel_estudio=nivel_estudio, lengua_indigena=lengua_indigena,
                                         num_hijos_mayores=num_hijos_mayores, num_hijos_menores=num_hijos_menores)

        # ---> REGISTRO DE LLAMADA <---

        llamada = Llamada.objects.create(hora_inicio=hora_inicio, hora_fin=hora_fin, consejero=consejero,
                                         victima=victima, f=f, recursos=recursos, intervencion=intervencion, medio_contacto=medio_contacto,
                                         violentometro=violentometro, tipo_caso=tipo_caso, tipo_ayuda=tipo_ayuda,
                                         tipo_violencia=tipo_violencia,
                                         posible_solucion=posible_solucion, vida_en_riesgo=vida_en_riesgo,
                                         tipo_llamada=tipo_llamada, motivo=motivo_llamada,
                                         nivel_riesgo=nivel_riesgo, estatus=estatus,
                                         causa_riesgo=causa_riesgo, fase_cambio=fase_cambio,
                                         modalidad_violencia=modalidad_violencia, fase_violencia=fase_violencia,
                                         semaforo=semaforo, victima_involucrada=victimas, agresor=agresor,
                                         como_se_entero=como_se_entero, devolver_llamada=devolver_llamada,
                                         num_llamada=num_llamada, debilidades=debilidades, amenazas=amenazas,
                                         linea_negocio=linea_negocio,aliado=aliado)

        # ---> REGISTRO DE CANALIZACIONES LLAMADA <---
        if institucion is not None and institucion2 is not None and institucion == institucion2:
            canalizacion_llamada = LlamadaCanalizacion.objects.create(llamada=llamada, institucion=institucion)
        else:
            if institucion is not None:
                canalizacion_llamada = LlamadaCanalizacion.objects.create(llamada=llamada, institucion=institucion)
            if institucion2 is not None:
                canalizacion_llamada2 = LlamadaCanalizacion.objects.create(llamada=llamada, institucion=institucion2)

        if tarea1 is not None:
            tarea = TareaLLamada.objects.create(nombre=tarea1)
            llamada.tareas.add(tarea)
        if tarea2 is not None:
            tarea = TareaLLamada.objects.create(nombre=tarea2)
            llamada.tareas.add(tarea)
        if tarea3 is not None:
            tarea = TareaLLamada.objects.create(nombre=tarea3)
            llamada.tareas.add(tarea)

        # ---> REGISTRO DE LLAMADA TIPIFICACION <---

        llamada_tipifificacion = TipificacionLLamada.objects.create(llamada=llamada, categoria_tipificacion=cat_tipificacion)

        # ---> REGISTRO DE EXAMEN MENTAL <---

        examen_mental = ExamenMental.objects.create(ute=em_ute, p=em_p, l=em_l, m=em_m, a=em_a, llamada=llamada)

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
        debilidades = serializer.data['debilidades']
        amenazas = serializer.data['amenazas']
        recursos = serializer.data['recursos']
        intervencion = serializer.data['intervencion']
        fase_cambio = FaseCambio.objects.get(pk=serializer.data['fase_cambio'])
        medio_contacto = MedioContacto.objects.get(pk=serializer.validated_data['medio_contacto'])
        violentometro = Violentometro.objects.filter(pk=serializer.validated_data['violentometro']).first()
        tipo_caso = serializer.data['tipo_caso']
        tipo_ayuda = serializer.data['tipo_ayuda']
        tipo_violencia = TipoViolencia.objects.filter(pk=serializer.validated_data['tipo_violencia']).first()
        posible_solucion = serializer.data['posible_solucion']
        vida_en_riesgo = serializer.validated_data['vida_en_riesgo']
        tipo_llamada = TipoLlamada.objects.get(pk=1)  # llamada de primera vez
        motivo_llamada = MotivoLLamada.objects.filter(pk=serializer.validated_data['motivo_llamada']).first()
        nivel_riesgo = NivelRiesgo.objects.filter(pk=serializer.data['nivel_riesgo']).first()
        estatus = EstatusLLamada.objects.get(pk=serializer.validated_data['estatus'])
        causa_riesgo = serializer.data['causa_riesgo']
        modalidad_violencia = ModalidadViolencia.objects.get(pk=serializer.data['modalidad_violencia'])
        fase_violencia = FaseViolencia.objects.get(pk=serializer.data['fase_violencia'])
        semaforo = Semaforo.objects.get(pk=serializer.data['semaforo'])
        victimas = VictimaInvolucrada.objects.get(pk=serializer.data['victimas'])
        agresor = Agresor.objects.get(pk=serializer.data['agresor'])
        como_se_entero = ComoSeEntero.objects.get(pk=serializer.data['como_se_entero'])
        devolver_llamada = serializer.validated_data['devolver_llamada']
        linea_negocio = LineaNegocio.objects.filter(pk=serializer.data['linea_negocio']).first()
        aliado = Aliado.objects.filter(pk=serializer.data['aliado']).first()
        num_llamada = 0
        if motivo_llamada.pk == 9:
            n = Llamada.objects.filter(victima=victima).aggregate(Max('num_llamada'))
            num_llamada = n['num_llamada__max'] + 1

        # Tareas
        tarea1 = serializer.data['tarea1']
        tarea2 = serializer.data['tarea2']
        tarea3 = serializer.data['tarea3']

        # ---> DATOS DE LA TIPIFICACION <---

        cat_tipificacion = CategoriaTipificacion.objects.get(pk=serializer.validated_data['categoria_tipificacion'])

        # ---> Datos del examen mental <---

        em_ute = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_ute'])
        em_p = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_p'])
        em_l = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_l'])
        em_m = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_m'])
        em_a = EstadoMental.objects.get(pk=serializer.validated_data['estado_mental_a'])

        # ---> Datos de las canalizaciones a instituciones <---

        institucion = AcudeInstitucion.objects.filter(pk=serializer.validated_data['institucion']).first()
        institucion2 = AcudeInstitucion.objects.filter(pk=serializer.validated_data['institucion2']).first()

        # ---> REGISTRO DE LLAMADA <---

        llamada = Llamada.objects.create(hora_inicio=hora_inicio, hora_fin=hora_fin, consejero=consejero,
                                         victima=victima, f=f, recursos=recursos, intervencion=intervencion ,medio_contacto=medio_contacto,
                                         violentometro=violentometro, tipo_caso=tipo_caso, tipo_ayuda=tipo_ayuda,
                                         tipo_violencia=tipo_violencia,
                                         posible_solucion=posible_solucion, vida_en_riesgo=vida_en_riesgo,
                                         tipo_llamada=tipo_llamada, motivo=motivo_llamada,
                                         nivel_riesgo=nivel_riesgo, estatus=estatus,
                                         causa_riesgo=causa_riesgo, fase_cambio=fase_cambio,
                                         modalidad_violencia=modalidad_violencia, fase_violencia=fase_violencia,
                                         semaforo=semaforo, victima_involucrada=victimas, agresor=agresor,
                                         como_se_entero=como_se_entero, devolver_llamada=devolver_llamada, num_llamada=num_llamada,
                                         debilidades=debilidades, amenazas=amenazas, linea_negocio=linea_negocio,aliado=aliado)

        # ---> REGISTRO DE CANALIZACIONES LLAMADA <---
        if institucion is not None and institucion2 is not None and institucion == institucion2:
            canalizacion_llamada = LlamadaCanalizacion.objects.create(llamada=llamada, institucion=institucion)
        else:
            if institucion is not None:
                canalizacion_llamada = LlamadaCanalizacion.objects.create(llamada=llamada, institucion=institucion)
            if institucion2 is not None:
                canalizacion_llamada2 = LlamadaCanalizacion.objects.create(llamada=llamada, institucion=institucion2)


        if tarea1 is not None:
            tarea = TareaLLamada.objects.create(nombre=tarea1)
            llamada.tareas.add(tarea)
        if tarea2 is not None:
            tarea = TareaLLamada.objects.create(nombre=tarea2)
            llamada.tareas.add(tarea)
        if tarea3 is not None:
            tarea = TareaLLamada.objects.create(nombre=tarea3)
            llamada.tareas.add(tarea)

        # ---> REGISTRO DE LLAMADA TIPIFICACION <---

        llamada_tipifificacion = TipificacionLLamada.objects.create(llamada=llamada, categoria_tipificacion=cat_tipificacion)

        # ---> REGISTRO DE EXAMEN MENTAL <---

        examen_mental = ExamenMental.objects.create(ute=em_ute, p=em_p, l=em_l, m=em_m, a=em_a, llamada=llamada)

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

class BusquedaUsuario(ListAPIView):
    """
    **Búsqueda básica**

    1. tipo_busqueda:
        - 0: busqueda por teléfono
        - 1: busqueda por nombre
        - 3: busqueda por ID de la víctima

    2. nombre: nombre de la victima

    3. telefono: teléfono de la víctima
    4. id: ID de la victima

    **Búsqueda por filtros**

    1. tipo_busqueda:
        - 0: busqueda por teléfono
        - 1: busqueda por nombre

    2. nombre: nombre de la victima

    3. telefono: teléfono de la victima

    4. filtro:
        - 1: para hábilitar filtros en la búsqueda

    5. consejero: ID del consejero

    6. fecha_inicio: fecha de inicio en la busqueda (yyyy-mm-dd)

    7. fecha_fin: fecha de fin en la busqueda de llamadas (yyyy-mm-dd)

    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = LLamadaSerializer

    def get_queryset(self):
        tipo_busqueda = self.request.query_params.get('tipo_busqueda', None)
        filtro = self.request.query_params.get('filtro', None)
        consejero = self.request.query_params.get('consejero', None)
        fecha_inicio = self.request.query_params.get('fecha_inicio', None)
        fecha_fin = self.request.query_params.get('fecha_fin', None)

        queryset = Llamada.objects.none()
        if tipo_busqueda == '0':
            telefono = self.request.query_params.get('telefono', None)
            if telefono is not None:
                list_last_llamadas = Victima.objects.filter(telefono__icontains=telefono)
                list_last_llamadas = list_last_llamadas.annotate(pk_llamada=Max('llamada__pk')).values_list('pk_llamada', flat=True)
                queryset = Llamada.objects.filter(pk__in=list_last_llamadas).annotate(num_max=Max('num_llamada'))
        if tipo_busqueda == '1':
            nombre = self.request.query_params.get('nombre', None)
            if nombre is not None:
                list_last_llamadas = Victima.objects.filter(nombre__icontains=nombre) | Victima.objects.filter(apellido_materno__icontains=nombre) | Victima.objects.filter(apellido_paterno__icontains=nombre)
                list_last_llamadas = list_last_llamadas.annotate(pk_llamada=Max('llamada__pk')).values_list('pk_llamada', flat=True)
                queryset = Llamada.objects.filter(pk__in=list_last_llamadas).annotate(num_max=Max('num_llamada'))
        if tipo_busqueda == '3':
            id_usuario = self.request.query_params.get('id', None)
            if id_usuario is not None:
                list_last_llamadas = Victima.objects.filter(pk=id_usuario)
                list_last_llamadas = list_last_llamadas.annotate(pk_llamada=Max('llamada__pk')).values_list(
                    'pk_llamada', flat=True)
                queryset = Llamada.objects.filter(pk__in=list_last_llamadas).annotate(num_max=Max('num_llamada'))
        if filtro == '1':
            if consejero is not None:
                try:
                    consejero = Consejero.objects.get(pk=consejero)
                    queryset = queryset.filter(consejero=consejero)
                except Consejero.DoesNotExist:
                    raise Http404("No existe el consejero")
            if fecha_inicio is not None and fecha_fin is not None:
                queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])
            elif fecha_inicio is not None:
                queryset = queryset.filter(fecha__gte=fecha_inicio)
            elif fecha_fin is not None:
                queryset = queryset.filter(fecha__lte=fecha_fin)
        queryset.order_by('-fecha')
        return queryset

class ListConsejeros(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = ConsejeroSerializer

    def get_queryset(self):
        queryset = Consejero.objects.all()
        return queryset

