# Generated by Django 2.1.1 on 2019-02-08 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0046_recado_asunto'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoMensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='adjunto_mensajes/')),
            ],
            options={
                'db_table': 'archivo_mensaje',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ArchivoRecado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='adjunto_recado/')),
                ('recado', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='archivos', to='config.Recado')),
            ],
            options={
                'db_table': 'archivo_recado',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='mensaje',
            name='archivos',
        ),
        migrations.DeleteModel(
            name='Archivo',
        ),
        migrations.AddField(
            model_name='archivomensaje',
            name='mensaje',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='archivos', to='config.Mensaje'),
        ),
    ]
