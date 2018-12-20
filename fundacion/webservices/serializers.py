from rest_framework import serializers


class FechaSerializer(serializers.Serializer):
    tipo = serializers.CharField(max_length=20)
    fecha = serializers.DateField(allow_null= True)
    fecha_fin = serializers.DateField(allow_null= True)
    mes = serializers.IntegerField(allow_null= True)
    anio = serializers.IntegerField(allow_null= True)