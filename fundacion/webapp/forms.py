from django.forms import ModelForm, Select

from config.models import Pendiente


class PendienteForm(ModelForm):
    class Meta:
        model = Pendiente
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_limite', 'completado']
        labels = {'descripcion': 'Descripción', 'fecha_limite': 'Fecha límite'}
        widgets= {'completado': Select(choices=[[True, 'Sí'], [False, 'No']]),}