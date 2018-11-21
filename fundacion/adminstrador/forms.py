from django.contrib.auth.models import User
from django.forms import ModelForm, Select, PasswordInput, DateTimeField

from config.models import AcudeInstitucion, Estado, Pais, EstadoCivil, Estatus, LenguaIndigena, MedioContacto, \
    ModalidadViolencia, Municipio, NivelEstudio, NivelViolencia, Ocupacion, Religion, TipoCaso, TipoViolencia, \
    Violentometro, ViveCon, ContactoInstitucion


class AsesorCallcenterForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        widgets = {
            'password': PasswordInput(), }

class PsicologoForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        widgets = {
            'password': PasswordInput(), }

class ReporteroForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        widgets = {
            'password': PasswordInput(), }

class AcudeInstitucionForm(ModelForm):
    class Meta:
        model = AcudeInstitucion
        exclude = ['fecha_alta', 'fecha_baja', 'fecha_actualizacion', 'coordenadas']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]),
            'convenio': Select(choices=[[True, 'Sí'], [False, 'No']]),
        }

class EstadoForm(ModelForm):
    class Meta:
        model = Estado
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class PaisForm(ModelForm):
    class Meta:
        model = Pais
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class EstadoCivilForm(ModelForm):
    class Meta:
        model = EstadoCivil
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class EstatusForm(ModelForm):
    class Meta:
        model = Estatus
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class LenguaIndigenaForm(ModelForm):
    class Meta:
        model = LenguaIndigena
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class MedioContactoForm(ModelForm):
    class Meta:
        model = MedioContacto
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class ModalidadViolenciaForm(ModelForm):
    class Meta:
        model = ModalidadViolencia
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class MunicipioForm(ModelForm):
    class Meta:
        model = Municipio
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class NivelEstudioForm(ModelForm):
    class Meta:
        model = NivelEstudio
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class NivelViolenciaForm(ModelForm):
    class Meta:
        model = NivelViolencia
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class OcupacionForm(ModelForm):
    class Meta:
        model = Ocupacion
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class ReligionForm(ModelForm):
    class Meta:
        model = Religion
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class TipoCasoForm(ModelForm):
    class Meta:
        model = TipoCaso
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class TipoViolenciaForm(ModelForm):
    class Meta:
        model = TipoViolencia
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class ViolentometroForm(ModelForm):
    class Meta:
        model = Violentometro
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class ViveConForm(ModelForm):
    class Meta:
        model = ViveCon
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class ContactoInstitucionForm(ModelForm):
    class Meta:
        model = ContactoInstitucion
        exclude = ['institucion']
        labels = {
            'telefono': 'Teléfono',
            'extension': 'Extensión'
        }