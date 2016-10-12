# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-12 01:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0007_auto_20161012_0156'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oncubauser',
            options={'verbose_name': 'Usuario OnCuba', 'verbose_name_plural': 'Usuarios OnCuba'},
        ),
        migrations.AlterField(
            model_name='oncubauser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
