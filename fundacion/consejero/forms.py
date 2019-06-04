from django.forms import ModelForm

from config.models import Victima, Colonia


class VictimaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        pk_victima = kwargs['instance'].id
        v = Victima.objects.get(pk=pk_victima)
        super(VictimaForm, self).__init__(*args, **kwargs)
        if v.cp is not None:
            self.fields['colonia'].queryset = Colonia.objects.filter(cp = v.cp)
        else:
            self.fields['colonia'].queryset = Colonia.objects.none()

    class Meta:
        model = Victima
        fields = ['telefono', 'nombre', 'apellido_materno', 'apellido_paterno', 'sexo', 'religion', 'nivel_estudio',
                  'fecha_nacimiento', 'cp', 'colonia', 'trabajo_remunerado', 'vive_con', 'num_hijos_menores',
                  'num_hijos_mayores', 'estatus', 'comentarios_estatus']