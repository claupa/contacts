from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    name = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, default=" ")
    

    class Meta:
        verbose_name_plural = 'categorias'

    def __unicode__(self):
        return u"Categoria: %s" % self.name

class Proyecto(models.Model):
    name = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, default=" ")
    

    class Meta:
        verbose_name_plural = 'proyectos'

    def __unicode__(self):
        return u"Proyecto: %s" % self.name