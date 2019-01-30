from django.forms import ModelForm, Select

from config.models import Evaluacion


class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        exclude = ['fecha_alta', 'fecha_baja']
        widgets = {
            'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']]), }
