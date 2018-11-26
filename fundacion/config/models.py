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

    def create_user(self, correo, rol, password, nombre, a_paterno, celular, fecha_nac, genero):
        if not correo:
            raise ValueError('El usuario necesita un email')

        user = self.model(
            correo=self.normalize_email(correo)
        )
        user.set_password(password)
        user.nombre = nombre
        user.a_paterno = a_paterno
        user.fecha_nac = fecha_nac
        user.celular = celular
        user.genero = genero
        user.estatus = True
        user.save(using=self._db)
        user.roles.add(rol)
        user.save()
        return user

    def create_superuser(self, correo, password, nombre, a_paterno, celular, fecha_nac, genero):
        user = self.create_user(correo=correo, rol=Rol.objects.get(pk=1), password=password, nombre=nombre,
                                a_paterno=a_paterno, celular=celular, fecha_nac=fecha_nac, genero=genero)
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
    password = models.CharField(max_length=256)
    fecha_nac = models.DateField()
    genero = models.ForeignKey('Sexo', models.DO_NOTHING, null=True)
    roles = models.ManyToManyField('Rol')
    estatus = models.BooleanField(default=False)
    foto = models.FileField(db_column='foto', upload_to='usuarios/', null=True, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'a_paterno', 'celular', 'fecha_nac', 'genero']

    def __str__(self):
        return self.nombre + ' ' + self.a_paterno

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        p = perm.split('.')
        if len(p) > 1:
            per = self.roles.filter(permisos__codename=p[1]).count()
        else:
            per = self.roles.filter(permisos__codename=p[0]).count()
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
                per = self.roles.filter(permisos__codename=pr[1]).count()
            else:
                per = self.roles.filter(permisos__codename=pr[0]).count()
            if per == 0:
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        if self.is_staff:
            return True
        if self.roles.filter(permisos__codename=app_label).count() > 0:
            return True
        return False

    @property
    def is_staff(self):
        if self.roles.filter(pk=1):
            return True
        else:
            return False

    @property
    def is_superuser(self):
        if self.roles.filter(pk=1):
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.roles.filter(pk=2):
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


class Consejero(Catalogo):
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
    s = models.CharField(max_length=4096, blank=True, null=True)
    o = models.CharField(max_length=4096, blank=True, null=True)
    a = models.CharField(max_length=4096, blank=True, null=True)
    p = models.CharField(max_length=4096, blank=True, null=True)
    medio_contacto = models.ForeignKey('MedioContacto', models.DO_NOTHING)
    violentometro = models.ForeignKey('Violentometro', models.DO_NOTHING, blank=True, null=True)
    tipo_caso = models.ForeignKey('TipoCaso', models.DO_NOTHING, blank=True, null=True)
    tipo_violencia = models.ForeignKey('TipoViolencia', models.DO_NOTHING, blank=True, null=True)
    institucion = models.ForeignKey('AcudeInstitucion', models.DO_NOTHING, blank=True, null=True)
    posible_solucion = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'llamada'


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
    nombre = models.CharField(max_length=256, blank=True, null=True)
    telefono = models.CharField(max_length=256, blank=True, null=True)
    estado_civil = models.ForeignKey('EstadoCivil', models.DO_NOTHING)
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING)
    ocupacion = models.ForeignKey('Ocupacion', models.DO_NOTHING)
    religion = models.ForeignKey('Religion', models.DO_NOTHING)
    vive_con = models.ForeignKey('ViveCon', models.DO_NOTHING)
    sexo = models.ForeignKey('Sexo', models.DO_NOTHING)
    nivel_estudio = models.ForeignKey('NivelEstudio', models.DO_NOTHING)
    lengua_indigena = models.ForeignKey('LenguaIndigena', models.DO_NOTHING)

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


class ContactoInstitucion(models.Model):
    nombre = models.CharField(max_length=256)
    telefono = models.CharField(max_length=15)
    extension = models.CharField(max_length=5, blank=True, null=True)
    institucion = models.ForeignKey('AcudeInstitucion', on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'contacto_institucion'
