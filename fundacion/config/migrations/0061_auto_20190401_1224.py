# Generated by Django 2.1.1 on 2019-04-01 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0060_auto_20190401_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='estatus_actividad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='config.EstatusUsuario'),
        ),
    ]
