# Generated by Django 2.1.1 on 2019-05-13 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0076_auto_20190513_1212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='llamada',
            old_name='duracion_minutos',
            new_name='duracion_servicio',
        ),
    ]
