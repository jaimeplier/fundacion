from django.forms import ModelForm, Select, PasswordInput

from config.models import AcudeInstitucion, Estado, Pais, EstadoCivil, Estatus, LenguaIndigena, MedioContacto, \
    ModalidadViolencia, Municipio, NivelEstudio, NivelViolencia, Ocupacion, Religion, TipoCaso, TipoViolencia, \
    Violentometro, ViveCon, ContactoInstitucion, Consejero, Directorio, Supervisor, Calidad, Sexo, Ayuda, MotivoLLamada


class ConsejeroForm(ModelForm):
    class Meta:
        model = Consejero
        exclude = ['rol', 'estatus', 'last_login']
        labels = {
            'tipo_usuario': 'Tipo de consejero',
            'a_paterno': 'Apellido paterno',
            'a_materno': 'Apellido materno',
            'fecha_nac': 'Fecha de nacimiento',
            'genero': 'Género',
        }
        widgets = {
            'password': PasswordInput()
        }

class DirectorioForm(ModelForm):
    class Meta:
        model = Directorio
        exclude = ['rol', 'estatus', 'last_login']
        labels = {
            'a_paterno': 'Apellido paterno',
            'a_materno': 'Apellido materno',
            'fecha_nac': 'Fecha de nacimiento',
            'genero': 'Género',
        }
        widgets = {
            'password': PasswordInput()
        }

class SupervisorForm(ModelForm):
    class Meta:
        model = Supervisor
        exclude = ['rol', 'estatus', 'last_login']
        labels = {
            'a_paterno': 'Apellido paterno',
            'a_materno': 'Apellido materno',
            'fecha_nac': 'Fecha de nacimiento',
            'genero': 'Género',
        }
        widgets = {
            'password': PasswordInput()
        }

class CalidadForm(ModelForm):
    class Meta:
        model = Calidad
        exclude = ['rol', 'estatus', 'last_login']
        labels = {
            'a_paterno': 'Apellido paterno',
            'a_materno': 'Apellido materno',
            'fecha_nac': 'Fecha de nacimiento',
            'genero': 'Género',
        }
        widgets = {
            'password': PasswordInput()
        }

class AcudeInstitucionForm(ModelForm):
    class Meta:
        model = AcudeInstitucion
        exclude = ['fecha_alta', 'fecha_baja', 'fecha_actualizacion', 'coordenadas']
        labels = {
            'direccion': 'Dirección',
        }
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

class SexoForm(ModelForm):
    class Meta:
        model = Sexo
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class AyudaForm(ModelForm):
    class Meta:
        model = Ayuda
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

class MotivoLLamadaForm(ModelForm):
    class Meta:
        model = MotivoLLamada
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }