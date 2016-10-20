#-*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from select_multiple_field.models import SelectMultipleField
from django.contrib.auth.models import User
import django.utils.timezone as t

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
    role = models.ForeignKey(Role, blank=True, null=True)
    phone_number = models.CharField(max_length = 15, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Usuarios OnCuba'
        verbose_name = 'Usuario OnCuba'
    
    def username(self):
        return self.user.username

    def __unicode__(self):
        return u"%s" % (self.user.username) 

    def nombre_completo(self):
        return self.user.first_name + ' ' + self.user.last_name

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
    date_marked = models.DateTimeField(blank = True, default =t.now)

    def nombre_completo(self):
        return u"%s %s" % (self.nombre, self.apellidos) 

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
    date_marked = models.DateTimeField(blank = True, default =t.now)

    def nombre_completo(self):
        return u"%s" % (self.nombre) 
    

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


class Invitacion(models.Model):
    username = models.CharField(max_length = 50, verbose_name='Nombre de Usuario', blank=True, null=True)
    first_name = models.CharField(max_length = 100,  verbose_name='Nombre(s)', default = " ", blank=True, null=True)
    last_name = models.CharField(max_length = 100, verbose_name='Apellido(s)', default = " ", blank=True, null=True)
    email = models.EmailField(unique= True, verbose_name = 'Correo Electrónico')
    phone_number = models.CharField(max_length = 15, blank=True, null=True)
    cargo = models.CharField(max_length= 200, blank=True, null=True)
    role = models.ForeignKey(Role)
    usada = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Invitaciones'

    def __unicode__(self):
        return u"%s" % (self.email) 

class UserTracker(models.Model):
    ACTIONS = (('C', 'Creado'),('M', 'Modificado'),('B', 'Borrado'), ('I','Invitado'), ('L', 'Leido'),('A', 'Accedido'))
    user = models.ForeignKey(User)
    action = models.CharField(max_length=1, choices = ACTIONS)
    fecha = models.DateTimeField(default =t.now)
    entidad = models.ForeignKey(Entidad, null=True, blank = True)
    persona = models.ForeignKey(Persona, null = True, blank= True)
    created_user = models.ForeignKey(Invitacion, null = True, blank= True, verbose_name = 'Usuario Invitado')

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = "Historial"

    def __unicode__(self):
        acciones ={ 'C' : 'creó', 'M':'modificó', 'L': 'consultó', 'B':'borró' }
        if self.action == 'C' or self.action=='M' or self.action=='L' or self.action=='B':
            a = acciones[self.action]
            return u'El usuario %s %s el contacto %s el día %s.' % \
            ( self.user.username,a, self.entidad.nombre_completo() if self.entidad else self.persona.nombre_completo(),
            self.fecha.strftime('%d/%m/%Y'))
        if self.action =="A":
            return u'El usuario %s accedió al sitio el día %s.' % ( self.user.username,  self.fecha.strftime('%d/%m/%Y'))
        else:
            return u'El usuario %s invitó al usuario %s el día %s.' % ( self.user.username, self.created_user.email, self.fecha.strftime('%d/%m/%Y'))

class Staff(models.Model):
    nombre = models.CharField(max_length = 100,  verbose_name='Nombre(s)', default = " ")
    apellidos = models.CharField(max_length = 100, verbose_name='Apellido(s)', default = " ")
    email = models.EmailField(unique= True, verbose_name = 'Correo Electrónico')
    phone_number = models.CharField(max_length = 15, blank=True, null=True)
    cargo = models.CharField(max_length= 200)
    proyectos = models.ManyToManyField(Proyecto)

    class Meta:
        verbose_name_plural = 'Staff'

    def __unicode__(self):
        return u"%s %s" % (self.nombre, self.apellidos) 


    