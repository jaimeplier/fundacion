from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, get_object_or_404

from config.models import Sexo, Religion, NivelEstudio, Ocupacion, ViveCon, TipoLlamada, TipoCaso, TipoViolencia, \
    Violentometro, AcudeInstitucion, MotivoLLamada, Tipificacion, CategoriaTipificacion, ModalidadViolencia, \
    FaseViolencia, Semaforo, VictimaInvolucrada, Agresor, RedesApoyo, EstatusLLamada
from webservices.serializers import CatalogoSerializer


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
        queryset = Tipificacion.objects.all()
        return queryset

class ListTipificacionesCategorias(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = CategoriaTipificacion.objects.all()
        return queryset

class ListTipoCaso(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = TipoCaso.objects.all()
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

class ListFaseViolencia(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = FaseViolencia.objects.all()
        return queryset

class ListSemaforo(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Semaforo.objects.all()
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

class ListAcudeInstitucion(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = AcudeInstitucion.objects.all()
        return queryset

class ListEstatusLLamada(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = EstatusLLamada.objects.all()
        return queryset