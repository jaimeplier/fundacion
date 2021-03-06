# Generated by Django 2.1.1 on 2019-01-17 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0023_auto_20190116_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaTipificacion',
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
                'db_table': 'categoria_tipificacion',
            },
        ),
        migrations.CreateModel(
            name='TipicifacionLLamada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(max_length=512)),
                ('categoria_tipificacion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.CategoriaTipificacion')),
            ],
            options={
                'managed': True,
                'db_table': 'tipificacion_llamada',
            },
        ),
        migrations.CreateModel(
            name='Tipificacion',
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
                'db_table': 'tipificacion',
            },
        ),
        migrations.AddField(
            model_name='categoriatipificacion',
            name='tipificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Tipificacion'),
        ),
    ]
