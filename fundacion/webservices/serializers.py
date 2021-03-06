from rest_framework import serializers

from config.models import Consejero, Llamada, Victima, MotivoLLamada, TipoLlamada, Evaluacion, \
    CalificacionLlamada, TareaLLamada, Usuario, Rol, Mensaje, Recado, ComentarioLlamada, CompromisoLlamada, \
    EstatusUsuario, ArchivoMensaje, ArchivoRecado, Aliado, LineaNegocio, Tutor, Colonia, Municipio, Estado, \
    Pais, CategoriaExamenMental, ExamenMental, Sucursal, AcudeInstitucion, ContactoInstitucion


class FechaSerializer(serializers.Serializer):
    fecha = serializers.DateField()

class FechaSerializerMes(serializers.Serializer):
    n_servicios = serializers.IntegerField()
    fecha = serializers.DateField()

class CatalogoSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    nombre = serializers.CharField()
    estatus = serializers.BooleanField()

class ContactoInstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactoInstitucion
        fields = ['pk', 'nombre', 'telefono', 'extension']

class InstitucionSerializer(serializers.ModelSerializer):
    contactos = ContactoInstitucionSerializer(source='contactoinstitucion_set', many=True)
    class Meta:
        model = AcudeInstitucion
        fields = ['pk', 'nombre', 'direccion', 'contactos']

class SucursalSerializer(serializers.ModelSerializer):
    institucion = InstitucionSerializer(many=False)
    class Meta:
        model = Sucursal
        fields = ['pk', 'convenio', 'nombre', 'telefonos', 'horarios', 'direccion', 'institucion']

class AliadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aliado
        fields = ['pk', 'script', 'nombre']

class LineaNegocioSerializer(serializers.ModelSerializer):
    aliado = AliadoSerializer(read_only=True)
    class Meta:
        model = LineaNegocio
        fields = ['pk', 'nombre', 'aliado']

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['pk', 'nombre']

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ['pk', 'nombre']

class EstadoSerializer(serializers.ModelSerializer):
    pais = PaisSerializer()
    class Meta:
        model = Estado
        fields = ['pk', 'nombre', 'pais']

class MunicipioSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer()
    class Meta:
        model = Municipio
        fields = ['pk', 'nombre', 'estado']

class ColoniaSerializer(serializers.ModelSerializer):
    municipio = MunicipioSerializer()
    class Meta:
        model = Colonia
        fields = ['pk', 'nombre', 'municipio']

class menorSerializer(serializers.Serializer):
    edad = serializers.IntegerField(min_value=0, max_value=17)
    tutor = serializers.IntegerField()
    registro = serializers.BooleanField(default=False)

    def validate_tutor(self, value):
        try:
            Tutor.objects.get(pk=value)
        except:
            raise serializers.ValidationError('El ID:' +str(value) +' tutor no existe')
        return value

class CategoriaExamenMentalSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

    def validate_pk(self, value):
        try:
            CategoriaExamenMental.objects.get(pk=value)
        except:
            raise serializers.ValidationError('El ID: '+str(value)+ 'de categoría no existe')
        return value

class CategoriaExamenMentalSerializerpk(serializers.ModelSerializer):
    class Meta:
        model = CategoriaExamenMental
        fields = ['pk', 'nombre']

class ExamenMentalSerializer(serializers.ModelSerializer):
    categorias = CategoriaExamenMentalSerializerpk(source='categoria_examen', many=True)
    class Meta:
        model = ExamenMental
        fields = ['pk', 'nombre', 'categorias']


class PrimeraVezSerializer(serializers.Serializer):
    # victima
    telefono = serializers.IntegerField()
    nombre = serializers.CharField(max_length=256)
    apellido_paterno = serializers.CharField(max_length=128, allow_null=True, allow_blank=True, required=False)
    apellido_materno = serializers.CharField(max_length=128, allow_blank=True, allow_null=True, required=False)
    estado_civil = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    ocupacion = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    religion = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    vive_con = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    sexo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_estudio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    lengua_indigena = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    num_hijos_menores = serializers.IntegerField(min_value=0, allow_null=True, required=False)
    num_hijos_mayores = serializers.IntegerField(min_value=0, allow_null=True, required=False)
    colonia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    cp = serializers.CharField(max_length=5, allow_null=True, allow_blank=True, required=False)
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
    amenazas = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    debilidades = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    recursos = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    intervencion = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    medio_contacto = serializers.IntegerField()
    violentometro = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    tipo_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    sucursal1 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    sucursal2 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    posible_solucion = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    vida_en_riesgo = serializers.BooleanField(default=False)
    fase_cambio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    modalidad_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    victimas = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    agresor = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    motivo_llamada = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estado_mental = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_riesgo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    redes_apoyo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    como_se_entero = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    devolver_llamada = serializers.BooleanField(default=False)
    linea_negocio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    aliado = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Tareas asiganadas a la llamada
    tarea1 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea2 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea3 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)

    # Tipificacion Categoria
    categoria_tipificacion1 = serializers.IntegerField(min_value=1)
    categoria_tipificacion2 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    categoria_tipificacion3 = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Tipificacion Subcategoria
    subcategoria_tipificacion1 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    subcategoria_tipificacion2 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    subcategoria_tipificacion3 = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Examen mental
    examen_mental = serializers.ListField(child=CategoriaExamenMentalSerializer(), required=False)


    # Array menores en riesgo
    victimas_menores = serializers.ListField(child=menorSerializer(), required=False)


class SeguimientoSerializer(serializers.Serializer):

    # Llamada
    #hora_inicio = serializers.TimeField()
    #hora_fin = serializers.TimeField()
    #consejero = serializers.IntegerField()
    victima = serializers.IntegerField()
    f = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    amenazas = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    debilidades = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    recursos = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    intervencion = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    medio_contacto = serializers.IntegerField()
    violentometro = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    tipo_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    sucursal1 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    sucursal2 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    posible_solucion = serializers.CharField(max_length=4096, allow_blank=True, allow_null=True, required=False)
    vida_en_riesgo = serializers.BooleanField(default=False)
    fase_cambio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    modalidad_violencia = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    victimas = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    agresor = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    motivo_llamada = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    estado_mental = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    nivel_riesgo = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    como_se_entero = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    devolver_llamada = serializers.BooleanField(default=False)
    linea_negocio = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    aliado = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    colonia = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Tareas asiganadas a la llamada
    tarea1 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea2 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)
    tarea3 = serializers.CharField(max_length=512, allow_blank=True, allow_null=True, required=False)

    # Tipificacion Categoria
    categoria_tipificacion1 = serializers.IntegerField(min_value=1)
    categoria_tipificacion2 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    categoria_tipificacion3 = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Tipificacion Subcategoria
    subcategoria_tipificacion1 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    subcategoria_tipificacion2 = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    subcategoria_tipificacion3 = serializers.IntegerField(min_value=1, allow_null=True, required=False)

    # Examen mental
    examen_mental = serializers.ListField(child=CategoriaExamenMentalSerializer(), required=False)

    # Array menores en riesgo
    victimas_menores = serializers.ListField(child=menorSerializer(), required=False, allow_null=True)

class ConsejeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consejero
        fields = ['pk', 'get_full_name', 'nombre', 'a_paterno', 'a_materno']

class VictimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victima
        fields = ['pk','nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'estatus', 'comentarios_estatus']

class MotivoLLamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivoLLamada
        fields = '__all__'

class TipoLLamadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoLlamada
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
    tareas = TareasLLamadaSerializer(read_only=True,many=True)
    num_max = serializers.IntegerField(required=False)

    class Meta:
        model = Llamada
        fields = (
        'victima', 'consejero', 'motivo', 'tipo_llamada', 'tareas', 'num_max', 'fecha', 'hora_inicio',
        'hora_fin', 'f', 'recursos', 'intervencion', 'medio_contacto', 'violentometro',
        'tipo_violencia', 'posible_solucion', 'vida_en_riesgo', 'nivel_riesgo',
        'fase_cambio', 'calificacion', 'modalidad_violencia', 'victima_involucrada',
        'agresor', 'como_se_entero', 'devolver_llamada', 'id', 'num_llamada')

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

class UsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.PrimaryKeyRelatedField(many=False, queryset=Rol.objects.filter(pk__gt=1), read_only=False)
    genero = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Usuario
        fields = (
            'id', 'correo', 'nombre', 'a_paterno', 'a_materno', 'foto', 'estatus',
            'rol', 'genero')

class ArchivoMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoMensaje
        fields = ('archivo', 'mensaje')


class ArchivoRecadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoRecado
        fields = ('file', 'recado')

class MensajeSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    destinatarios = UsuarioSerializer(many=True, read_only=True)
    archivo = ArchivoMensajeSerializer(source='archivos', many=True)

    class Meta:
        model = Mensaje
        fields = ('id', 'usuario', 'fecha', 'titulo', 'cuerpo', 'archivo', 'destinatarios', 'leido')

class MensajeSerializerPk(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = ('titulo', 'cuerpo', 'destinatarios')

class RecadoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False, read_only=True)
    destinatarios = UsuarioSerializer(many=True, read_only=True)
    archivo = ArchivoRecadoSerializer(source='archivos', many=True)

    class Meta:
        model = Recado
        fields = ('id', 'usuario', 'fecha', 'cuerpo', 'destinatarios', 'asunto', 'archivo', 'leido')

class RecadoSerializerPk(serializers.ModelSerializer):
    class Meta:
        model = Recado
        fields = ('cuerpo', 'destinatarios', 'asunto')

class ComentarioLlamadaSerializer(serializers.Serializer):
    llamada_pk = serializers.IntegerField(min_value=1)
    comentario = serializers.CharField(max_length=3000)
    compromisos = serializers.ListField(
        child=serializers.CharField(max_length=512), allow_empty=True, allow_null=True, required=False)

    def create(self, validated_data):
        llamada = Llamada.objects.get(pk=validated_data.get('llamada_pk'))

        coment = ComentarioLlamada.objects.filter(llamada=llamada).first()
        if coment is not None:
            comprom = coment.compromisos.all().values_list('pk', flat=True)
            comp_llamada = CompromisoLlamada.objects.filter(pk__in=comprom).delete()
            coment.delete()

        comentario = validated_data.get('comentario')
        cll = ComentarioLlamada.objects.create(llamada=llamada, comentario=comentario)
        if validated_data.get('compromisos') is not None and len(validated_data.get('compromisos')) > 0:
            compromisos = validated_data.get('compromisos')
            for compromiso in compromisos:
                compromiso_ll = CompromisoLlamada.objects.create(nombre=compromiso)
                cll.compromisos.add(compromiso_ll)
        else:
            pass

        return cll

class EstatusUsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstatusUsuario
        fields = ('id', 'nombre', 'estatus')

class PkSerializer(serializers.Serializer):

    pk = serializers.IntegerField(min_value=1)

class EstatusInstitucionSucursalSerializer(serializers.Serializer):
    # tipo 0: institucion
    # tipo 1: sucursal
    tipo = serializers.IntegerField()
    pk = serializers.IntegerField()
    estatus = serializers.IntegerField()

class UsuariosAjaxListSerializer(serializers.Serializer):
    dia = serializers.DateField(required=False)