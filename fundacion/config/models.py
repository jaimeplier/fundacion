from __future__ import unicode_literals

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Permission
from django.contrib.gis.db import models


class Catalogo(models.Model):
    nombre = models.CharField(max_length=512)
    estatus = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True


class UsuarioManager(BaseUserManager):

    def create_user(self, correo, rol, password, nombre, a_paterno, a_materno, fecha_nac, genero):
        if not correo:
            raise ValueError('El usuario necesita un email')

        user = self.model(
            correo=self.normalize_email(correo)
        )
        user.set_password(password)
        user.nombre = nombre
        user.a_paterno = a_paterno
        user.a_materno = a_materno
        user.fecha_nac = fecha_nac
        user.genero = genero
        user.estatus = True
        user.rol = rol
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password, nombre, a_paterno, a_materno, fecha_nac, genero):
        user = self.create_user(correo=correo, rol=Rol.objects.get(pk=1), password=password, nombre=nombre,
                                a_paterno=a_paterno, a_materno=a_materno, fecha_nac=fecha_nac,
                                genero=Sexo.objects.get(pk=genero))
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super(UsuarioManager, self).get_queryset().filter(estatus=True)

    def all_users(self):
        return super(UsuarioManager, self).get_queryset().all()


class Usuario(AbstractBaseUser):
    correo = models.EmailField(unique=True, max_length=128)
    nombre = models.CharField(max_length=50)
    a_paterno = models.CharField(max_length=50)
    a_materno = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    fecha_nac = models.DateField()
    genero = models.ForeignKey('Sexo', models.DO_NOTHING, null=True)
    rol = models.ForeignKey('Rol', models.DO_NOTHING)
    estatus = models.BooleanField(default=True)
    foto = models.FileField(db_column='foto', upload_to='usuarios/')

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'a_paterno', 'a_materno', 'fecha_nac', 'genero']

    def __str__(self):
        return self.nombre + ' ' + self.a_paterno + ' ' + self.a_materno

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        p = perm.split('.')
        if len(p) > 1:
            per = self.rol.permisos.filter(codename=p[1]).count()
        else:
            per = self.rol.permisos.filter(codename=p[0]).count()
        if per > 0:
            return True
        return False

    def has_perms(self, perm, obj=None):
        # Este válida
        if self.is_superuser:
            return True
        for p in perm:
            pr = p.split('.')
            if len(pr) > 1:
                per = self.rol.permisos.filter(codename=pr[1]).count()
            else:
                per = self.rol.permisos.filter(codename=pr[0]).count()
            if per == 0:
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        if self.is_staff:
            return True
        if self.rol.permisos.filter(codename=app_label).count() > 0:
            return True
        return False

    @property
    def is_staff(self):
        if self.rol.pk == 1:
            return True
        else:
            return False

    @property
    def is_superuser(self):
        if self.rol.pk == 1:
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.rol.pk == 2:
            return True
        else:
            return False

    @property
    def is_consejero(self):
        if self.rol.pk == 3:
            return True
        else:
            return False

    @property
    def is_supervisor(self):
        if self.rol.pk == 4:
            return True
        else:
            return False

    @property
    def is_directorio(self):
        if self.rol.pk == 5:
            return True
        else:
            return False

    @property
    def is_calidad(self):
        if self.rol.pk == 6:
            return True
        else:
            return False

    @property
    def is_active(self):
        return self.estatus == 1

    def get_full_name(self):
        name = self.__str__()
        return name.title()

    def get_short_name(self):
        return self.correo

    class Meta:
        managed = True
        db_table = 'usuario'


class AcudeInstitucion(Catalogo):
    dependencia = models.ForeignKey('Dependencia', on_delete=models.DO_NOTHING)
    coordenadas = models.PointField()
    convenio = models.BooleanField(default=False)
    direccion = models.CharField(max_length=512)

    @property
    def latitud(self):
        """I'm the 'x' property."""
        return str(self.coordenadas.coords[1])

    @property
    def longitud(self):
        """I'm the 'x' property."""
        return str(self.coordenadas.coords[0])

    class Meta:
        managed = True
        db_table = 'acude_institucion'


class Ayuda(Catalogo):
    tipo_ayuda = models.ForeignKey('TipoAyuda', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'ayuda'


class Consejero(Usuario):
    tipo_usuario = models.ForeignKey('TipoUsuario', on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'consejero'


class Estado(Catalogo):
    pais = models.ForeignKey('Pais', on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'estado'


class EstadoCivil(Catalogo):
    class Meta:
        managed = True
        db_table = 'estado_civil'


class Estatus(Catalogo):
    class Meta:
        managed = True
        db_table = 'estatus'


class LenguaIndigena(Catalogo):
    class Meta:
        managed = True
        db_table = 'lengua_indigena'


class Llamada(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    consejero = models.ForeignKey('Consejero', models.DO_NOTHING)
    victima = models.ForeignKey('Victima', models.DO_NOTHING)
    f = models.CharField(max_length=4096, blank=True, null=True)
    o = models.CharField(max_length=4096, blank=True, null=True)
    a = models.CharField(max_length=4096, blank=True, null=True)
    d = models.CharField(max_length=4096, blank=True, null=True)
    medio_contacto = models.ForeignKey('MedioContacto', models.DO_NOTHING)
    violentometro = models.ForeignKey('Violentometro', models.DO_NOTHING, blank=True, null=True)
    tipo_caso = models.TextField(max_length=1024)
    tipo_ayuda = models.TextField(max_length=1024)
    tipo_violencia = models.ForeignKey('TipoViolencia', models.DO_NOTHING, blank=True, null=True)
    institucion = models.ForeignKey('AcudeInstitucion', models.DO_NOTHING, blank=True, null=True)
    posible_solucion = models.CharField(max_length=4096, blank=True, null=True)
    vida_en_riesgo = models.BooleanField(default=False)
    tipo_llamada = models.ForeignKey('TipoLlamada', models.DO_NOTHING, blank=True, null=True)
    motivo = models.ForeignKey('MotivoLLamada', models.DO_NOTHING, blank=True, null=True)
    estado_mental = models.ForeignKey('EstadoMental', models.DO_NOTHING)
    nivel_riesgo = models.ForeignKey('NivelRiesgo', models.DO_NOTHING)
    estatus = models.ForeignKey('EstatusLLamada', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'llamada'


class EstatusLLamada(Catalogo):
    class Meta:
        managed = True
        db_table = 'estatus_llamada'


class MotivoLLamada(Catalogo):
    class Meta:
        managed = True
        db_table = 'motivo_llamada'


class TipoLlamada(Catalogo):
    class Meta:
        managed = True
        db_table = 'tipo_llamada'


class LLamadaAyuda(models.Model):
    llamada = models.ForeignKey('Llamada', models.DO_NOTHING)
    ayuda = models.ForeignKey('Ayuda', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'llamada_ayuda'


class MedioContacto(Catalogo):
    class Meta:
        managed = True
        db_table = 'medio_contacto'


class ModalidadViolencia(Catalogo):
    class Meta:
        managed = True
        db_table = 'modalidad_violencia'


class Municipio(Catalogo):
    estado = models.ForeignKey('Estado', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'municipio'


class NivelEstudio(Catalogo):
    class Meta:
        managed = True
        db_table = 'nivel_estudio'


class NivelViolencia(Catalogo):
    class Meta:
        managed = True
        db_table = 'nivel_violencia'


class Ocupacion(Catalogo):
    class Meta:
        managed = True
        db_table = 'ocupacion'


class Pais(Catalogo):
    class Meta:
        managed = True
        db_table = 'pais'


class Religion(Catalogo):
    class Meta:
        managed = True
        db_table = 'religion'


class Rol(Catalogo):
    permisos = models.ManyToManyField(Permission, through='RolHasPermissions')

    class Meta:
        managed = True
        db_table = 'rol'


class RolHasPermissions(models.Model):
    rol = models.ForeignKey(Rol, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'rol_has_permissions'


class Sexo(Catalogo):
    class Meta:
        managed = True
        db_table = 'sexo'


class TipoAyuda(Catalogo):
    class Meta:
        managed = True
        db_table = 'tipo_ayuda'


class TipoCaso(Catalogo):
    class Meta:
        managed = True
        db_table = 'tipo_caso'


class TipoViolencia(Catalogo):
    class Meta:
        managed = True
        db_table = 'tipo_violencia'


class Victima(models.Model):
    telefono = models.CharField(max_length=256)
    nombre = models.CharField(max_length=256)
    apellido_paterno = models.CharField(max_length=128, blank=True, null=True)
    apellido_materno = models.CharField(max_length=128, blank=True, null=True)
    estado_civil = models.ForeignKey('EstadoCivil', models.DO_NOTHING, blank=True, null=True)
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, blank=True, null=True)
    ocupacion = models.ForeignKey('Ocupacion', models.DO_NOTHING, blank=True, null=True)
    religion = models.ForeignKey('Religion', models.DO_NOTHING, blank=True, null=True)
    vive_con = models.ForeignKey('ViveCon', models.DO_NOTHING, blank=True, null=True)
    sexo = models.ForeignKey('Sexo', models.DO_NOTHING, blank=True, null=True)
    nivel_estudio = models.ForeignKey('NivelEstudio', models.DO_NOTHING, blank=True, null=True)
    lengua_indigena = models.ForeignKey('LenguaIndigena', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'victima'


class Violentometro(Catalogo):
    class Meta:
        managed = True
        db_table = 'violentometro'


class ViveCon(Catalogo):
    class Meta:
        managed = True
        db_table = 'vive_con'


class Dependencia(Catalogo):
    class Meta:
        managed = True
        db_table = 'dependencia'


class RedesApoyo(Catalogo):
    class Meta:
        managed = True
        db_table = 'redes_de_apoyo'


class FaseViolencia(Catalogo):
    class Meta:
        managed = True
        db_table = 'fase_de_violencia'


class Semaforo(Catalogo):
    class Meta:
        managed = True
        db_table = 'semaforo'


class VictimaInvolucrada(Catalogo):
    class Meta:
        managed = True
        db_table = 'victima_involucrada'


class Agresor(Catalogo):
    class Meta:
        managed = True
        db_table = 'agresor'


class ContactoInstitucion(models.Model):
    nombre = models.CharField(max_length=256)
    telefono = models.CharField(max_length=15)
    extension = models.CharField(max_length=5, blank=True, null=True)
    institucion = models.ForeignKey('AcudeInstitucion', on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'contacto_institucion'


class TipoUsuario(Catalogo):
    class Meta:
        managed = True
        db_table = 'tipo_usuario'


class Supervisor(Usuario):
    class Meta:
        managed = True
        db_table = 'supervisor'


class Directorio(Usuario):
    class Meta:
        managed = True
        db_table = 'directorio'


class Calidad(Usuario):
    class Meta:
        managed = True
        db_table = 'calidad'


class MedioComunicacion(Catalogo):
    class Meta:
        managed = True
        db_table = 'medio_de_comunicacion'


class ComoSeEntero(Catalogo):
    medio = models.ForeignKey('MedioComunicacion', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'como_se_entero'

class EstadoMental(Catalogo):

    class Meta:
        managed = True
        db_table = 'estado_mental'

class NivelRiesgo(Catalogo):

    class Meta:
        managed = True
        db_table = 'nivel_de_riesgo'

class Tipificacion(Catalogo):

    class Meta:
        managed = True
        db_table = 'tipificacion'

class CategoriaTipificacion(Catalogo):
    tipificacion = models.ForeignKey('Tipificacion', models.DO_NOTHING)
    class Meta:
        managed = True
        db_table = 'categoria_tipificacion'

class TipificacionLLamada(models.Model):
    llamada = models.ForeignKey('Llamada', models.DO_NOTHING)
    categoria_tipificacion = models.ForeignKey('CategoriaTipificacion', models.DO_NOTHING)
    descripcion = models.TextField(max_length=512)
    class Meta:
        managed = True
        db_table = 'tipificacion_llamada'