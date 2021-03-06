# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-11 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0021_auto_20161111_0433'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addressentidad',
            options={'verbose_name': 'Direcci\xf3n', 'verbose_name_plural': 'Listado de Direcciones'},
        ),
        migrations.AlterModelOptions(
            name='addressperson',
            options={'verbose_name': 'Direcci\xf3n', 'verbose_name_plural': 'Listado de Direcciones'},
        ),
        migrations.AlterModelOptions(
            name='entidad',
            options={'verbose_name': 'Entidad', 'verbose_name_plural': 'Entidades'},
        ),
        migrations.AlterModelOptions(
            name='phonenumberentidad',
            options={'verbose_name': 'N\xfamero de Tel\xe9fono', 'verbose_name_plural': 'Listado de Tel\xe9fonos'},
        ),
        migrations.AlterModelOptions(
            name='phonenumberperson',
            options={'verbose_name': 'N\xfamero de Tel\xe9fono', 'verbose_name_plural': 'Listado de Tel\xe9fonos'},
        ),
        migrations.AddField(
            model_name='addressentidad',
            name='address',
            field=models.CharField(default='', max_length=300, verbose_name='Direcci\xf3n'),
        ),
        migrations.AddField(
            model_name='addressperson',
            name='address',
            field=models.CharField(default='', max_length=300, verbose_name='Direcci\xf3n'),
        ),
        migrations.AlterField(
            model_name='emailentidad',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Correo Electr\xf3nico'),
        ),
        migrations.AlterField(
            model_name='emailperson',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Correo Electr\xf3nico'),
        ),
        migrations.RemoveField(
            model_name='addressentidad',
            name='address_one',
        ),
        migrations.RemoveField(
            model_name='addressentidad',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='addressentidad',
            name='provincia',
        ),
        migrations.AlterUniqueTogether(
            name='addressentidad',
            unique_together=set([('address', 'pais', 'contact')]),
        ),
        migrations.RemoveField(
            model_name='addressperson',
            name='address_one',
        ),
        migrations.RemoveField(
            model_name='addressperson',
            name='municipio',
        ),
        migrations.RemoveField(
            model_name='addressperson',
            name='provincia',
        ),
        migrations.AlterUniqueTogether(
            name='addressperson',
            unique_together=set([('address', 'pais', 'contact')]),
        ),
        migrations.AlterUniqueTogether(
            name='contactperson',
            unique_together=set([('persona', 'cargo', 'entidad')]),
        ),
        migrations.AlterUniqueTogether(
            name='emailentidad',
            unique_together=set([('email', 'contact')]),
        ),
        migrations.AlterUniqueTogether(
            name='emailperson',
            unique_together=set([('email', 'contact')]),
        ),
    ]
