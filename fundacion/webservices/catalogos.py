from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.views import APIView

from config.models import Sexo, Religion, NivelEstudio, Ocupacion, ViveCon, TipoLlamada, TipoViolencia, \
    Violentometro, AcudeInstitucion, MotivoLLamada, Tipificacion, CategoriaTipificacion, ModalidadViolencia, \
    VictimaInvolucrada, Agresor, RedesApoyo, MedioContacto, NivelRiesgo, \
    RecomendacionRiesgo, FaseCambio, ComoSeEntero, Aliado, LineaNegocio, SubcategoriaTipificacion, \
    Consejero, Tutor, EstadoCivil, Sucursal, CategoriaExamenMental, ExamenMental, Colonia, Estado, Municipio
from webservices.serializers import CatalogoSerializer, AliadoSerializer, LineaNegocioSerializer, TutorSerializer, \
    CategoriaExamenMentalSerializerpk, ExamenMentalSerializer, ColoniaSerializer, SucursalSerializer


class ListSexo(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Sexo.objects.all()
        return queryset

class ListReligion(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Religion.objects.all()
        return queryset

class ListGradoEstudios(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = NivelEstudio.objects.all()
        return queryset

class ListOcupacion(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Ocupacion.objects.all()
        return queryset

class ListViveCon(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = ViveCon.objects.all()
        return queryset

class ListTipoLlamada(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = TipoLlamada.objects.all()
        return queryset

class ListMotivoLlamada(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = MotivoLLamada.objects.all()
        return queryset

class ListTipificaciones(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        u = self.request.user
        try:
            consejero = Consejero.objects.get(pk=u.pk)
            tipo_usuario = consejero.tipo_usuario.pk
            if tipo_usuario == 1: # Abogado
                queryset = Tipificacion.objects.filter(pk=4)
            elif tipo_usuario == 2: # Medico
                queryset = Tipificacion.objects.filter(pk__in=[2,3])
            elif tipo_usuario == 3: # Psicologo
                queryset = Tipificacion.objects.filter(pk=1)
        except Consejero.DoesNotExist:
            queryset = Tipificacion.objects.all()
            return  queryset
        return queryset

class ListTipificacionesCategorias(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        tipificacion = self.request.query_params.get('tipificacion', None)
        queryset = CategoriaTipificacion.objects.none()
        if tipificacion is not None:
            queryset = CategoriaTipificacion.objects.filter(tipificacion__pk=tipificacion)
        return queryset

class ListTipificacionesSubcategorias(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        categoria = self.request.query_params.get('categoria', None)
        queryset = SubcategoriaTipificacion.objects.none()
        if categoria is not None:
            queryset = SubcategoriaTipificacion.objects.filter(categoria__pk=categoria)
        return queryset

class ListModalidadViolencia(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = ModalidadViolencia.objects.all()
        return queryset

class ListTipoViolencia(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = TipoViolencia.objects.all()
        return queryset

class ListViolentometro(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Violentometro.objects.all()
        return queryset

class ListVictimas(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = VictimaInvolucrada.objects.all()
        return queryset

class ListAgresor(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Agresor.objects.all()
        return queryset

class ListRedesApoyo(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = RedesApoyo.objects.all()
        return queryset

class ListMedioContacto(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = MedioContacto.objects.all()
        return queryset

class ListAcudeInstitucion(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = AcudeInstitucion.objects.all()
        return queryset

class ListSucursales(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        keywords = self.request.query_params.get('keywords', None)
        estado = self.request.query_params.get('estado', None)
        colonia = self.request.query_params.get('colonia', None)
        queryset = Sucursal.objects.filter(estatus_institucion__pk__in=[1,2])
        if keywords is not None:
            list_keywords = keywords.strip()
            query='Select id, nombre, match(palabras_clave) AGAINST ("'+list_keywords+'") as Relevance from sucursal where match(palabras_clave) AGAINST ("'+list_keywords+'");'
            queryset = queryset.raw(query)
        if estado is not None:
            queryset = Sucursal.objects.filter(estado__pk=estado)
        if colonia is not None:
            colonia_obj = Colonia.objects.get(pk=colonia)
            queryset = Sucursal.objects.filter(estado=colonia_obj.municipio.estado)
        return queryset

class GetSucursal(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = SucursalSerializer
    def get_queryset(self):
        sucursal_pk = self.request.query_params.get('sucursal', None)
        queryset = Sucursal.objects.none()
        if sucursal_pk is not None:
            queryset= Sucursal.objects.filter(pk=sucursal_pk)
        return queryset


class ListNivelRiesgo(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = NivelRiesgo.objects.all()
        return queryset

class ListRecomendacionesRiesgo(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        tipificacion = self.request.query_params.get('tipificacion', None)
        queryset = RecomendacionRiesgo.objects.none()
        if tipificacion is not None:
            queryset = RecomendacionRiesgo.objects.filter(tipificacion__pk=tipificacion)
        return queryset

class ListFaseCambio(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = FaseCambio.objects.all()
        return queryset

class ListComoSeEntero(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = ComoSeEntero.objects.all()
        return queryset

class ListAliado(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = AliadoSerializer

    def get_queryset(self):
        aliado = self.request.query_params.get('aliado', None)
        queryset = Aliado.objects.all()
        if aliado is not None:
            queryset = Aliado.objects.filter(pk=aliado)
        return queryset

class ListLineaNegocio(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = LineaNegocioSerializer

    def get_queryset(self):
        aliado = self.request.query_params.get('aliado', None)
        queryset = LineaNegocio.objects.none()
        if aliado is not None:
            queryset = LineaNegocio.objects.filter(aliado__pk=aliado)
        return queryset

class ListTutor(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TutorSerializer

    def get_queryset(self):
        queryset = Tutor.objects.filter(estatus=True)
        return queryset

class ListDatosCP(ListAPIView):
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = ColoniaSerializer

    def get_queryset(self):
        cp = self.request.query_params.get('cp', None)
        queryset = Colonia.objects.none()
        if cp is not None:
            queryset = Colonia.objects.filter(cp=cp)
        return queryset

class ListEstadoCivil(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = EstadoCivil.objects.filter(estatus=True)
        return queryset

class ListExamenMental(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = ExamenMentalSerializer

    def get_queryset(self):
        queryset = ExamenMental.objects.filter(estatus=True)
        return queryset

class ListEstado(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Estado.objects.filter(estatus=True)
        return queryset

class ListMunicipio(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        estado = self.request.query_params.get('estado', None)
        queryset = Municipio.objects.none()
        if estado is not None:
            queryset = Municipio.objects.filter(estado__pk=estado, estatus=True)
        return queryset