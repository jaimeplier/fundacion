# Generated by Django 2.1.1 on 2019-05-28 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0082_cpcolonia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catcolonias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idcolonia', models.IntegerField(db_column='idColonia')),
                ('idmunicipio', models.IntegerField(db_column='idMunicipio')),
                ('idestado', models.IntegerField(db_column='idEstado')),
                ('cpostal', models.CharField(blank=True, db_column='cPostal', max_length=5, null=True)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('tipoasentamiento', models.CharField(blank=True, db_column='tipoAsentamiento', max_length=75, null=True)),
            ],
            options={
                'db_table': 'catcolonias',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Catestados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idestado', models.IntegerField(db_column='idEstado')),
                ('nombre', models.CharField(blank=True, max_length=20, null=True)),
                ('nomcorto', models.CharField(blank=True, db_column='nomCorto', max_length=10, null=True)),
                ('clave', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'catestados',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Catmunicipios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idmun', models.IntegerField(db_column='idMun')),
                ('idestado', models.IntegerField(db_column='idEstado')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('clave', models.CharField(blank=True, max_length=5, null=True)),
            ],
            options={
                'db_table': 'catmunicipios',
                'managed': False,
            },
        ),
    ]
