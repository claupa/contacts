# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-19 19:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0016_invitacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertracker',
            name='created_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oncuba.Invitacion', verbose_name='Usuario Invitado'),
        ),
    ]
