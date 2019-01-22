from django.forms import ModelForm

from config.models import Victima


class VictimaForm(ModelForm):
    class Meta:
        model = Victima
        fields = ['telefono', 'nombre', 'apellido_materno', 'apellido_paterno', 'sexo', 'religion', 'nivel_estudio', 'fecha_nacimiento', 'cp', 'colonia', 'trabajo_remunerado']