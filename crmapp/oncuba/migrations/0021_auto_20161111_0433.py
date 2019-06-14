# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-11 04:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0020_auto_20161110_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactperson',
            name='emails',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Correo(s) Electr\xf3nico(s)'),
        ),
        migrations.AlterField(
            model_name='phonenumberentidad',
            name='number',
            field=models.CharField(max_length=50, verbose_name='N\xfamero de Tel\xe9fono'),
        ),
        migrations.AlterField(
            model_name='phonenumberperson',
            name='number',
            field=models.CharField(max_length=100, verbose_name='N\xfamero de Tel\xe9fono'),
        ),
        migrations.AlterUniqueTogether(
            name='phonenumberentidad',
            unique_together=set([('number', 'contact')]),
        ),
        migrations.AlterUniqueTogether(
            name='phonenumberperson',
            unique_together=set([('number', 'contact')]),
        ),
    ]
