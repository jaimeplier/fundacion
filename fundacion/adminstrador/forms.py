from django.forms import ModelForm, Select

from config.models import AcudeInstitucion, Estado, Pais, EstadoCivil, Estatus, LenguaIndigena, MedioContacto, \
    ModalidadViolencia, Municipio, NivelEstudio, NivelViolencia, Ocupacion


class AcudeInstitucionForm(ModelForm):
    class Meta:
        model = AcudeInstitucion
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }

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