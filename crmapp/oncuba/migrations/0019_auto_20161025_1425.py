# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-25 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0018_invitacion_usada'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addressperson',
            options={'verbose_name': 'Direcci\xf3n', 'verbose_name_plural': 'Direcciones'},
        ),
        migrations.RenameField(
            model_name='entidad',
            old_name='pais',
            new_name='nacionalidad',
        ),
        migrations.RenameField(
            model_name='persona',
            old_name='pais',
            new_name='nacionalidad',
        ),
        migrations.RemoveField(
            model_name='addressentidad',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='addressperson',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='emailentidad',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='emailperson',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='apellidos',
        ),
        migrations.RemoveField(
            model_name='phonenumberentidad',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='phonenumberperson',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='addressentidad',
            name='pais',
            field=models.CharField(default='Cuba', max_length=50, verbose_name='Pa\xeds'),
        ),
        migrations.AddField(
            model_name='addressperson',
            name='pais',
            field=models.CharField(default='Cuba', max_length=50, verbose_name='Pa\xeds'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='descripcion',
            field=models.CharField(blank=True, default=' ', max_length=100, verbose_name='Descripci\xf3n'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(default=' ', max_length=200, verbose_name='Nombre(s) y Apellido(s)'),
        ),
        migrations.AlterField(
            model_name='phonenumberperson',
            name='number',
            field=models.CharField(max_length=100, unique=True, verbose_name='N\xfamero de Tel\xe9fono'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='descripcion',
            field=models.CharField(blank=True, default=' ', max_length=100, verbose_name='Descripci\xf3n'),
        ),
    ]
