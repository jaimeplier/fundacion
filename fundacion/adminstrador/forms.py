from django.forms import ModelForm, Select

from config.models import AcudeInstitucion


class AcudeInstitucionForm(ModelForm):
    class Meta:
        model = AcudeInstitucion
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }