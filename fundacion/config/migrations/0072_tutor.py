# Generated by Django 2.1.1 on 2019-05-03 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0071_auto_20190426_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor',
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
                'db_table': 'tutor',
            },
        ),
    ]
