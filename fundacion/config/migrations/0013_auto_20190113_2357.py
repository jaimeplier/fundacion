# Generated by Django 2.1.1 on 2019-01-14 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0012_auto_20181217_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoLlamada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=512)),
                ('estatus', models.BooleanField(default=True)),
                ('fecha_alta', models.DateTimeField(auto_now_add=True)),
                ('fecha_baja', models.DateTimeField(blank=True, null=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'managed': True,
                'db_table': 'tipo_llamada',
            },
        ),
        migrations.AddField(
            model_name='llamada',
            name='tipo_llamada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.TipoLlamada'),
        ),
    ]
