from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, get_object_or_404

from config.models import Sexo, Religion
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