# Generated by Django 2.1.1 on 2019-03-08 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0058_auto_20190308_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='llamada',
            name='num_llamada',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
