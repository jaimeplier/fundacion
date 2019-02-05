from rest_framework import serializers

from config.models import Consejero, Llamada, Victima, MotivoLLamada, TipoLlamada, EstatusLLamada, Evaluacion, \
    CalificacionLlamada, TareaLLamada, Archivo, Usuario, Rol, Mensaje, Recado


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
    modalidad_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    fase_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    semaforo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    victimas = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    agresor = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    motivo_llamada = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estado_mental = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_riesgo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estatus = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    causa_riesgo = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False )
    redes_apoyo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    como_se_entero = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Tareas asiganadas a la llamada
    tarea1 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea2 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea3 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)

    # Tipificacion Categoria
    categoria_tipificacion = serializers.IntegerField(min_value=1)
    descripcion_tipificacion = serializers.CharField(max_length=512)


    # Examen mental
    estado_mental_ute = serializers.IntegerField(min_value=1)
    estado_mental_p = serializers.IntegerField(min_value=1)
    estado_mental_l = serializers.IntegerField(min_value=1)
    estado_mental_m = serializers.IntegerField(min_value=1)
    estado_mental_a = serializers.IntegerField(min_value=1)

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
    fase_cambio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    modalidad_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    fase_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    semaforo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    victimas = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    agresor = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    motivo_llamada = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estado_mental = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_riesgo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estatus = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    causa_riesgo = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    como_se_entero = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Tareas asiganadas a la llamada
    tarea1 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea2 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea3 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)

    # Tipificacion Categoria
    categoria_tipificacion = serializers.IntegerField(min_value=1)
    descripcion_tipificacion = serializers.CharField(max_length=512)

    # Examen mental
    estado_mental_ute = serializers.IntegerField(min_value=1)
    estado_mental_p = serializers.IntegerField(min_value=1)
    estado_mental_l = serializers.IntegerField(min_value=1)
    estado_mental_m = serializers.IntegerField(min_value=1)
    estado_mental_a = serializers.IntegerField(min_value=1)

class ConsejeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consejero
        fields = ['pk', 'get_full_name', 'nombre', 'a_paterno', 'a_materno']

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

class TareasLLamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TareaLLamada
        fields = '__all__'

class LLamadaSerializer(serializers.ModelSerializer):
    victima = VictimaSerializer(read_only=True, many=False)
    consejero = ConsejeroSerializer(read_only=True, many=False)
    motivo = MotivoLLamadaSerializer(read_only=True, many=False)
    tipo_llamada = TipoLLamadaSerializer(read_only=True, many=False)
    estatus = EstatusLLamadaSerializer(read_only=True, many=False)
    tareas = TareasLLamadaSerializer(read_only=True,many=True)

    class Meta:
        model = Llamada
        fields = '__all__'

class BusquedaSerializer(serializers.Serializer):
    tipo_busqueda = serializers.IntegerField(min_value=0, max_value=1)
    nombre = serializers.CharField(max_length=512, required=False)
    telefono = serializers.IntegerField(required=False)

class RubrosSerializer(serializers.Serializer):
    llamada = serializers.IntegerField(min_value=1)
    rubros = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, allow_null=True, required=False)

    def create(self, validated_data):
        llamada = Llamada.objects.get(pk=validated_data.get('llamada'))
        cantidad_rubros = Evaluacion.objects.all().count()
        evaluacion = Evaluacion.objects.exclude(pk__in=validated_data.get('rubros'))
        rubros = Evaluacion.objects.filter(pk__in=validated_data.get('rubros'))
        if validated_data.get('rubros') is not None and len(validated_data.get('rubros')) > 0:
            evaluaciones = CalificacionLlamada.objects.filter(llamada=llamada).delete()
            for rubro in rubros:
                e = CalificacionLlamada.objects.create(llamada=llamada, rubro=rubro, estatus_rubro=True)
            for rubro in evaluacion:
                e = CalificacionLlamada.objects.create(llamada=llamada, rubro=rubro, estatus_rubro=False)
            try:
                calificacion = (rubros.count() * 10) / cantidad_rubros
                llamada.calificacion = calificacion
                llamada.save()
            except Exception as e:
                pass
        else:
            evaluaciones = CalificacionLlamada.objects.filter(llamada=llamada).delete()
            for rubro in evaluacion:
                e = CalificacionLlamada.objects.create(llamada=llamada, rubro=rubro, estatus_rubro=False)
            llamada.calificacion = 0.0
            llamada.save()

        return rubros

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.PrimaryKeyRelatedField(many=False, queryset=Rol.objects.filter(pk__gt=1), read_only=False)
    genero = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Usuario
        fields = (
            'id', 'correo', 'nombre', 'a_paterno', 'a_materno', 'foto', 'estatus',
            'rol', 'genero')

class MensajeSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    archivos = ArchivoSerializer(many=True, read_only=True)
    destinatarios = UsuarioSerializer(many=True, read_only=True)

    class Meta:
        model = Mensaje
        fields = ('id', 'usuario', 'fecha', 'titulo', 'cuerpo', 'archivos', 'destinatarios')

class MensajeSerializerPk(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = ('titulo', 'cuerpo', 'destinatarios')

class RecadoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    destinatarios = UsuarioSerializer(many=True, read_only=True)

    class Meta:
        model = Recado
        fields = ('id', 'usuario', 'fecha', 'cuerpo', 'destinatarios')

class RecadoSerializerPk(serializers.ModelSerializer):
    class Meta:
        model = Recado
        fields = ('cuerpo', 'destinatarios')