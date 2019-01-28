# Generated by Django 2.1.1 on 2019-01-28 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0036_fasecambio'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamenMental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='a', to='config.EstadoMental')),
                ('l', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='l', to='config.EstadoMental')),
            ],
            options={
                'managed': True,
                'db_table': 'examen_mental',
            },
        ),
        migrations.RemoveField(
            model_name='llamada',
            name='estado_mental',
        ),
        migrations.AddField(
            model_name='llamada',
            name='fase_cambio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='config.FaseCambio'),
        ),
        migrations.AddField(
            model_name='examenmental',
            name='llamada',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='config.Llamada'),
        ),
        migrations.AddField(
            model_name='examenmental',
            name='m',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='m', to='config.EstadoMental'),
        ),
        migrations.AddField(
            model_name='examenmental',
            name='p',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='p', to='config.EstadoMental'),
        ),
        migrations.AddField(
            model_name='examenmental',
            name='ute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ute', to='config.EstadoMental'),
        ),
    ]
