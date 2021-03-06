# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-11 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.CharField(blank=True, default=' ', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('descripcion', models.CharField(blank=True, default=' ', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'proyectos',
            },
        ),
    ]
