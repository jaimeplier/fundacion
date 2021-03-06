# Generated by Django 2.1.1 on 2019-01-22 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0030_auto_20190118_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='llamada',
            name='colonia',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='llamada',
            name='cp',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='llamada',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='llamada',
            name='trabajo_remunerado',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
