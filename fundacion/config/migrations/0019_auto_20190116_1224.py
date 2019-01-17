# Generated by Django 2.1.1 on 2019-01-16 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0018_agresor_faseviolencia_redesapoyo_semaforo_victimainvolucrada'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComoSeEntero',
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
                'db_table': 'como_se_entero',
            },
        ),
        migrations.CreateModel(
            name='MedioComunicacion',
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
                'db_table': 'medio_de_comunicacion',
            },
        ),
        migrations.AddField(
            model_name='comoseentero',
            name='medio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.MedioComunicacion'),
        ),
    ]