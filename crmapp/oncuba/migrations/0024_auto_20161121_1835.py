# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-21 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0023_auto_20161111_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidad',
            name='nacionalidad',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Nacionalidad'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nacionalidad',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='nacionalidad'),
        ),
    ]