# Generated by Django 2.1.1 on 2018-11-27 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_auto_20181126_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='a_materno',
            field=models.CharField(default=' ', max_length=50),
            preserve_default=False,
        ),
    ]
