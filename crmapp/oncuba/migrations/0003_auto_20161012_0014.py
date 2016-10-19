# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-12 00:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oncuba', '0002_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_one', models.CharField(max_length=200, verbose_name='Direcci\xf3n')),
                ('provincia', models.CharField(max_length=50)),
                ('municipio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(max_length=50, verbose_name='Pa\xeds')),
                ('sitio_web', models.URLField(verbose_name='Sitio Web')),
                ('observaciones', models.TextField()),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('categoria', models.ManyToManyField(to='oncuba.Categoria')),
                ('proyecto', models.ManyToManyField(to='oncuba.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electr\xf3nico')),
                ('descripcion', models.CharField(blank=True, default=' ', max_length=100)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncuba.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar_de_trabajo', models.CharField(max_length=50, verbose_name='Lugar de Trabajo')),
                ('ocupacion', models.CharField(max_length=50, verbose_name='Ocupaci\xf3n')),
                ('fecha_de_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('sexo', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=1)),
                ('estado_civil', models.CharField(choices=[('S', 'Solter'), ('C', 'Casad'), ('V', 'Viud'), ('D', 'Divorciad')], max_length=1)),
                ('hijos', models.BooleanField()),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oncuba.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, unique=True, verbose_name='N\xfamero de Tel\xe9fono')),
                ('descripcion', models.CharField(blank=True, default=' ', max_length=100)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncuba.Contact')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oncuba.Contact'),
        ),
    ]
