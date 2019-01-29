from rest_framework import serializers

from config.models import Consejero, Llamada, Victima, MotivoLLamada, TipoLlamada, EstatusLLamada


class FechaSerializer(serializers.Serializer):
    tipo = serializers.CharField(max_length=20)
    fecha = serializers.DateField(allow_null=True)
    fecha_fin = serializers.DateField(allow_null=True)
    mes = serializers.IntegerField(allow_null=True)
    anio = serializers.IntegerField(allow_null=True)


class CatalogoSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    nombre = serializers.CharField()
    estatus = serializers.BooleanField()


class PrimeraVezSerializer(serializers.Serializer):
    # victima
    telefono = serializers.IntegerField()
    nombre = serializers.CharField(max_length=256)
    apellido_paterno = serializers.CharField(max_length=128, allow_null=True, allow_blank=True, required=False)
    apellido_materno = serializers.CharField(max_length=128, allow_blank=True, allow_null=True, required=False)
    estado_civil = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    municipio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    ocupacion = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    religion = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    vive_con = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    sexo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_estudio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    lengua_indigena = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    #Fecha de nacimiento
    #Codigo postal
    #Colonia
    #Trabajo remunerado

    # Llamada
    #hora_inicio = serializers.TimeField()
    #hora_fin = serializers.TimeField()
    #consejero = serializers.IntegerField()
    #victima = serializers.IntegerField()
    f = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    o = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    d = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    a = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    medio_contacto = serializers.IntegerField()
    violentometro = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    tipo_caso = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True, required=False)
    tipo_ayuda = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True, required=False)
    tipo_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    institucion = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    posible_solucion = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    vida_en_riesgo = serializers.BooleanField(default=False)
    fase_cambio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    motivo_llamada = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estado_mental = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_riesgo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estatus = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    causa_riesgo = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False )
    redes_apoyo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    #Modalidad violencia
    #Tipo de violencia
    #Fase de violencia
    #semaforo
    #victimas involucradas
    #agresor


    # Tipificacion Categoria
    categoria_tipificacion = serializers.IntegerField(min_value=1)
    descripcion_tipificacion = serializers.CharField(max_length=512)


    # Examen mental
    estado_metal_ute = serializers.IntegerField(min_value=1)
    estado_metal_p = serializers.IntegerField(min_value=1)
    estado_metal_l = serializers.IntegerField(min_value=1)
    estado_metal_m = serializers.IntegerField(min_value=1)
    estado_metal_a = serializers.IntegerField(min_value=1)

class SeguimientoSerializer(serializers.Serializer):

    # Llamada
    #hora_inicio = serializers.TimeField()
    #hora_fin = serializers.TimeField()
    #consejero = serializers.IntegerField()
    victima = serializers.IntegerField()
    f = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    o = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    d = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    a = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    medio_contacto = serializers.IntegerField()
    violentometro = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    tipo_caso = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True, required=False)
    tipo_ayuda = serializers.CharField(max_length=1024, allow_blank=True, allow_null=True, required=False)
    tipo_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    institucion = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    posible_solucion = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    vida_en_riesgo = serializers.BooleanField(default=False)
    motivo_llamada = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estado_mental = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_riesgo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estatus = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    causa_riesgo = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    #Modalidad violencia
    #Tipo de violencia
    #Fase de violencia
    #semaforo
    #victimas involucradas
    #agresor


    # Tipificacion Categoria
    categoria_tipificacion = serializers.IntegerField(min_value=1)
    descripcion_tipificacion = serializers.CharField(max_length=512)

    # Examen mental
    estado_metal_ute = serializers.IntegerField(min_value=1)
    estado_metal_p = serializers.IntegerField(min_value=1)
    estado_metal_l = serializers.IntegerField(min_value=1)
    estado_metal_m = serializers.IntegerField(min_value=1)
    estado_metal_a = serializers.IntegerField(min_value=1)

class ConsejeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consejero
        fields = ['pk', 'get_full_name']

class VictimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victima
        fields = ['pk','nombre', 'apellido_paterno', 'apellido_materno', 'telefono']

class MotivoLLamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivoLLamada
        fields = '__all__'

class TipoLLamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoLlamada
        fields = '__all__'

class EstatusLLamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatusLLamada
        fields = '__all__'

class LLamadaSerializer(serializers.ModelSerializer):
    victima = VictimaSerializer(read_only=True, many=False)
    consejero = ConsejeroSerializer(read_only=True, many=False)
    motivo = MotivoLLamadaSerializer(read_only=True, many=False)
    tipo_llamada = TipoLLamadaSerializer(read_only=True, many=False)
    estatus = EstatusLLamadaSerializer(read_only=True, many=False)

    class Meta:
        model = Llamada
        fields = '__all__'

class BusquedaSerializer(serializers.Serializer):
    tipo_busqueda = serializers.IntegerField(min_value=0, max_value=1)
    nombre = serializers.CharField(max_length=512, required=False)
    telefono = serializers.IntegerField(required=False)
