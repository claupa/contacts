# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-17 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0011_auto_20161014_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oncubauser',
            name='proyecto',
        ),
        migrations.AddField(
            model_name='oncubauser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='usertracker',
            name='action',
            field=models.CharField(choices=[('C', 'Creado'), ('M', 'Modificado'), ('B', 'Borrado'), ('I', 'Invitado'), ('L', 'Leido'), ('A', 'Accedido')], max_length=1),
        ),
    ]
