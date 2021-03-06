from django.forms import ModelForm, Select, PasswordInput

from config.models import AcudeInstitucion, Estado, Pais, EstadoCivil, Estatus, LenguaIndigena, MedioContacto, \
    ModalidadViolencia, Municipio, NivelEstudio, NivelViolencia, Ocupacion, Religion, TipoViolencia, \
    Violentometro, ViveCon, ContactoInstitucion, Consejero, Directorio, Supervisor, Calidad, Sexo, MotivoLLamada, \
    Dependencia, RedesApoyo, VictimaInvolucrada, Agresor, \
    ComoSeEntero, NivelRiesgo, RecomendacionRiesgo, FaseCambio, EstatusUsuario, Tipificacion, \
    CategoriaTipificacion, Sucursal, Aliado, LineaNegocio, SubcategoriaTipificacion, Tutor, Colonia, \
    ExamenMental, CategoriaExamenMental


class ConsejeroForm(ModelForm):
    class Meta:
        model = Consejero
        exclude = ['rol', 'estatus', 'last_login', 'estatus_actividad']
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
        exclude = ['rol', 'estatus', 'last_login', 'estatus_actividad']
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
        exclude = ['rol', 'estatus', 'last_login', 'estatus_actividad']
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
        exclude = ['rol', 'estatus', 'last_login', 'estatus_actividad']
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
        exclude = ['fecha_alta', 'fecha_baja', 'fecha_actualizacion', 'coordenadas', 'estatus_institucion', 'estatus']
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
        exclude = ['pais', 'fecha_alta', 'fecha_baja', 'estatus']


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
        exclude = ['estado', 'cat_mun_id', 'fecha_alta', 'fecha_baja', 'estatus']

class ColoniaForm(ModelForm):
    class Meta:
        model = Colonia
        exclude = ['municipio', 'fecha_alta', 'fecha_baja', 'estatus']


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


class SucursalInstitucionForm(ModelForm):
    class Meta:
        model = Sucursal
        exclude = ['institucion', 'fecha_alta', 'fecha_baja', 'fecha_actualizacion', 'coordenadas', 'estatus_institucion', 'estatus']
        labels = {
            'direccion': 'Dirección',
        }
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]),
            'convenio': Select(choices=[[True, 'Sí'], [False, 'No']]),
        }


class SexoForm(ModelForm):
    class Meta:
        model = Sexo
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class MotivoLLamadaForm(ModelForm):
    class Meta:
        model = MotivoLLamada
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class DependenciaForm(ModelForm):
    class Meta:
        model = Dependencia
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class RedesApoyoForm(ModelForm):
    class Meta:
        model = RedesApoyo
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class VictimaInvolucradaForm(ModelForm):
    class Meta:
        model = VictimaInvolucrada
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class AgresorForm(ModelForm):
    class Meta:
        model = Agresor
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class ComoSeEnteroForm(ModelForm):
    class Meta:
        model = ComoSeEntero
        fields = ['nombre', 'estatus']
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class NivelRiesgoForm(ModelForm):
    class Meta:
        model = NivelRiesgo
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class RecomendacionRiesgoForm(ModelForm):
    class Meta:
        model = RecomendacionRiesgo
        exclude = ['fecha_alta', 'fecha_baja', 'estatus']


class FaseCambioForm(ModelForm):
    class Meta:
        model = FaseCambio
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class ActividadUsuarioForm(ModelForm):
    class Meta:
        model = EstatusUsuario
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }


class TipificacionForm(ModelForm):
    class Meta:
        model = Tipificacion
        exclude = ['fecha_alta', 'fecha_baja', 'estatus']

class AliadoForm(ModelForm):
    class Meta:
        model = Aliado
        exclude = ['fecha_alta', 'fecha_baja', 'estatus']

class LineaNegocioForm(ModelForm):
    class Meta:
        model = LineaNegocio
        exclude = ['fecha_alta', 'fecha_baja', 'estatus', 'aliado']


class CategoriaTipificacionForm(ModelForm):
    class Meta:
        model = CategoriaTipificacion
        exclude = ['fecha_alta', 'fecha_baja', 'estatus', 'tipificacion']

class SubcategoriaTipificacionForm(ModelForm):
    class Meta:
        model = SubcategoriaTipificacion
        exclude = ['fecha_alta', 'fecha_baja', 'estatus', 'categoria']

class TutorForm(ModelForm):
    class Meta:
        model = Tutor
        exclude = ['fecha_alta', 'fecha_baja', 'estatus']

class ExamenMentalForm(ModelForm):
    class Meta:
        model = ExamenMental
        exclude = ['fecha_alta', 'fecha_baja', 'estatus']

class CategoriaExamenMentalForm(ModelForm):
    class Meta:
        model = CategoriaExamenMental
        exclude = ['fecha_alta', 'fecha_baja', 'estatus', 'examen_mental']