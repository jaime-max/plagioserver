# Generated by Django 4.2.2 on 2023-06-28 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0002_rename_usuario_id_docente_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gestiondocumentos',
            name='comentario',
            field=models.CharField(default='', max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='gestiondocumentos',
            name='titulo',
            field=models.CharField(default='', max_length=70, null=True),
        ),
    ]
