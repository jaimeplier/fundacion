from __future__ import unicode_literals

from django.db import models


class Catalogo(models.Model):
    nombre = models.CharField(max_length=512)
    estatus = models.IntegerField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True


class AcudeInstitucion(Catalogo):
    class Meta:
        managed = True
        db_table = 'acude_institucion'


class Estado(Catalogo):
    pais = models.ForeignKey('Estado',on_delete=models.DO_NOTHING)

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


class MedioContacto(Catalogo):

    class Meta:
        managed = True
        db_table = 'medio_contacto'


class ModalidadViolencia(Catalogo):

    class Meta:
        managed = True
        db_table = 'modalidad_violencia'


class Municipio(Catalogo):
    estado = models.ForeignKey('Estado',models.DO_NOTHING)

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


class Sexo(Catalogo):

    class Meta:
        managed = True
        db_table = 'sexo'


class TipoCaso(Catalogo):

    class Meta:
        managed = True
        db_table = 'tipo_caso'


class TipoViolencia(Catalogo):

    class Meta:
        managed = True
        db_table = 'tipo_violencia'


class Violentometro(Catalogo):

    class Meta:
        managed = True
        db_table = 'violentometro'


class ViveCon(Catalogo):

    class Meta:
        managed = True
        db_table = 'vive_con'
