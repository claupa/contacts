#-*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from select_multiple_field.models import SelectMultipleField
from django.contrib.auth.models import User
# from datetime import datetime
from django.utils.timezone import now

class Categoria(models.Model):
    name = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, default=" ")
    

    class Meta:
        verbose_name_plural = 'categorias'

    def __unicode__(self):
        return u"%s" % self.name

class Proyecto(models.Model):
    name = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, default=" ")
    

    class Meta:
        verbose_name_plural = 'proyectos'

    def __unicode__(self):
        return u"%s" % self.name

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    categories = models.ManyToManyField(Categoria)
    proyectos = models.ManyToManyField(Proyecto)

    class Meta:
        verbose_name_plural = 'roles'

    def __unicode__(self):
        return u"%s" % self.name

class OnCubaUser(models.Model):
    user = models.ForeignKey(User, verbose_name = 'Usuario')
    cargo = models.CharField(max_length= 200)
    proyecto = models.ManyToManyField(Proyecto)
    role = models.ForeignKey(Role, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Usuarios OnCuba'
        verbose_name = 'Usuario OnCuba'
    
    def username(self):
        return self.user.username

    def proyectos(self):
        proyectos = ''
        for proyecto in self.proyecto.all():
            proyectos+= ', ' + proyecto.name
        return proyectos[2:]

    def __unicode__(self):
        return u"%s" % (self.user.username) 

class Persona(models.Model):
    SEXO =(('F', 'Femenino'), ('M', 'Masculino'))
    ESTADO_CIVIL = (('S', 'Solter'),('C','Casad'), ('V', 'Viud'), ('D', 'Divorciad'))

    nombre = models.CharField(max_length = 100,  verbose_name='Nombre(s)', default = " ")
    apellidos = models.CharField(max_length = 100, verbose_name='Apellido(s)', default = " ")
    lugar_de_trabajo = models.CharField(max_length=50, verbose_name='Lugar de Trabajo')
    ocupacion = models.CharField(max_length = 50,verbose_name='Ocupación')    
    pais = models.CharField(max_length=50,  verbose_name='País', default="Cuba")

    fecha_de_nacimiento = models.DateField(verbose_name = 'Fecha de Nacimiento',blank = True)
    sexo = models.CharField(max_length = 1, choices = SEXO,blank = True)
    estado_civil = models.CharField(max_length = 1, choices=ESTADO_CIVIL,blank = True)
    hijos = models.BooleanField()

    sitio_web = models.URLField( verbose_name='Sitio Web', blank = True)
    categoria = models.ManyToManyField(Categoria)
    proyecto = models.ManyToManyField(Proyecto)
    observaciones = models.TextField(blank = True)
    created_by = models.ForeignKey(OnCubaUser, verbose_name = 'Creado por',default = 1)
    marked_for_deletion = models.BooleanField(default=False)
    date_marked = models.DateTimeField(blank = True, default =now())


    def __unicode__(self):
        return u"%s %s" % (self.nombre, self.apellidos) 


class PhoneNumberPerson(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name= 'Número de Teléfono')
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name = 'Descripción')
    contact = models.ForeignKey(Persona, on_delete= models.CASCADE)
    class Meta:
        verbose_name_plural = 'Números de Teléfono'
        verbose_name =  "Número de Teléfono"

class EmailPerson(models.Model):
    email = models.EmailField(unique= True, verbose_name = 'Correo Electrónico')
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name = 'Descripción')
    contact = models.ForeignKey(Persona, on_delete= models.CASCADE)
    class Meta:
        verbose_name_plural = 'Listado de Correos'
        verbose_name =  "Correo Electrónico"

class AddressPerson(models.Model):
    address_one = models.CharField(max_length=200, verbose_name= 'Dirección')
    provincia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name='Descripción')
    contact = models.ForeignKey(Persona, on_delete= models.CASCADE)
    class Meta:
        verbose_name_plural = 'Direcciones Disponibles'
        verbose_name =  "Dirección"
    
class Entidad(models.Model):
    SEXO =(('F', 'Femenino'), ('M', 'Masculino'))
    ESTADO_CIVIL = (('S', 'Solter'),('C','Casad'), ('V', 'Viud'), ('D', 'Divorciad'))

    nombre = models.CharField(max_length = 100,  verbose_name='Nombre', default = " ")
    servicios = models.CharField(max_length=100, verbose_name='Servicios/Productos')
    persona = models.CharField(max_length = 200 , verbose_name = 'Nombre de Persona de Contacto')
    cargo = models.CharField(max_length = 100 , verbose_name = 'Cargo de Persona de Contacto')   

    pais = models.CharField(max_length=50,  verbose_name='País', default="Cuba")
    
    aniversario = models.DateField(blank = True)
    fiesta = models.DateField(verbose_name='Fiesta Nacional',blank = True)
    
    sitio_web = models.URLField( verbose_name='Sitio Web',blank = True)
    categoria = models.ManyToManyField(Categoria)
    proyecto = models.ManyToManyField(Proyecto)    
    observaciones = models.TextField(blank = True)

    created_by = models.ForeignKey(OnCubaUser, verbose_name = 'Creado por',default = 1)
    marked_for_deletion = models.BooleanField(default = False)
    date_marked = models.DateTimeField(blank = True, default =now())
    

    class Meta:
        verbose_name_plural = 'entidades'

    def __unicode__(self):
        return u"%s" % (self.nombre) 
        

class PhoneNumberEntidad(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name= 'Número de Teléfono')
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name = 'Descripción')
    contact = models.ForeignKey(Entidad, on_delete= models.CASCADE)

    class Meta:
        verbose_name_plural = 'Números de Teléfono'
        verbose_name =  "Número de Teléfono"


    def __unicode__(self):
        return u"%s" % (self.number) 


class EmailEntidad(models.Model):
    email = models.EmailField(unique= True, verbose_name = 'Correo Electrónico')
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name = 'Descripción')
    contact = models.ForeignKey(Entidad, on_delete= models.CASCADE)
    class Meta:
        verbose_name_plural = 'Listado de Correos'
        verbose_name =  "Correo Electrónico"
    

class AddressEntidad(models.Model):
    address_one = models.CharField(max_length=200, verbose_name= 'Dirección')
    provincia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name='Descripción')
    contact = models.ForeignKey(Entidad, on_delete= models.CASCADE)
    class Meta:
        verbose_name_plural = 'Direcciones Disponibles'
        verbose_name =  "Dirección"
    
    
    
    

# Persona:
# Lugar de Trabajo
# Ocupacion
# Fecha de Nacimiento
# Sexo
# Hijos
# Estado Civil


# Entidad:
# Servicios/Productos
# Aniversario
# FIesta Nacional
#     Nombre
# List - Telefonos (Numeros y descripción)
# List - Email (Numeros y descripcion) 
# País
# List - Direcion +  Descripcion
# Sitio Web
# Categoría
# Relación con OnCuba
# Observaciones