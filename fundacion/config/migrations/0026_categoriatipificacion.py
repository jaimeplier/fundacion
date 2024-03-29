# Generated by Django 2.1.1 on 2019-01-17 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0025_auto_20190117_1445'),
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
                ('tipificacion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Tipificacion')),
            ],
            options={
                'db_table': 'categoria_tipificacion',
                'managed': True,
            },
        ),
    ]
