# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-19 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0015_auto_20161018_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre de Usuario')),
                ('first_name', models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='Nombre(s)')),
                ('last_name', models.CharField(blank=True, default=' ', max_length=100, null=True, verbose_name='Apellido(s)')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electr\xf3nico')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('cargo', models.CharField(blank=True, max_length=200, null=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncuba.Role')),
            ],
            options={
                'verbose_name_plural': 'Invitaciones',
            },
        ),
    ]