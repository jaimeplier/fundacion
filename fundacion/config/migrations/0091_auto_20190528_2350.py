# Generated by Django 2.1.1 on 2019-05-28 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0090_auto_20190528_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catestados',
            name='nombre',
            field=models.CharField(max_length=64),
        ),
    ]
