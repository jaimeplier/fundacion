# Generated by Django 2.1.1 on 2019-01-24 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0032_auto_20190121_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='llamada',
            name='causa_riesgo',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
    ]
