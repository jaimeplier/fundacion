# Generated by Django 2.1.1 on 2019-05-14 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0077_auto_20190513_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='comentario',
            field=models.TextField(blank=True, max_length=512, null=True),
        ),
    ]
