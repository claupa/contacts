#-*- coding: utf8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from select_multiple_field.models import SelectMultipleField
from django.contrib.auth.models import User
import django.utils.timezone as t

class Categoria(models.Model):
    name = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name="Descripción")
    

    class Meta:
        verbose_name_plural = 'categorias'

    def __unicode__(self):
        return u"%s" % self.name

class Proyecto(models.Model):
    name = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True, default=" ", verbose_name="Descripción")
    

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

# ---------------- PERSONA -------------------------------------------------
class Persona(models.Model):
    SEXO =(('F', 'Femenino'), ('M', 'Masculino'))
    ESTADO_CIVIL = (('S', 'Solter'),('C','Casad'), ('V', 'Viud'), ('D', 'Divorciad'))
    nombre = models.CharField(max_length = 200,  verbose_name='Nombre(s) y Apellido(s)', default = " ")
    lugar_de_trabajo = models.CharField(max_length=50, verbose_name='Lugar de Trabajo')
    ocupacion = models.CharField(max_length = 50,verbose_name='Ocupación')    
    nacionalidad = models.CharField(max_length=50,  verbose_name='nacionalidad', default="Cubana")
    fecha_de_nacimiento = models.DateField(verbose_name = 'Fecha de Nacimiento',blank = True, null=True)
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
        return u"%s" % (self.nombre) 

    def __unicode__(self):
        return u"%s" % (self.nombre) 


class PhoneNumberPerson(models.Model):
    number = models.CharField(max_length=100, verbose_name= 'Número de Teléfono')
    contact = models.ForeignKey(Persona, on_delete= models.CASCADE)

    class Meta:
        verbose_name_plural = 'Listado de Teléfonos'
        verbose_name =  "Número de Teléfono"
        unique_together =('number', 'contact')

    def __unicode__(self):
        return u"%s" % (self.number) 

class EmailPerson(models.Model):
    email = models.EmailField(verbose_name = 'Correo Electrónico')
    contact = models.ForeignKey(Persona, on_delete= models.CASCADE)

    class Meta:
        verbose_name_plural = 'Listado de Correos'
        verbose_name =  "Correo Electrónico"
        unique_together = ("email", "contact")
    
    def __unicode__(self):
        return u"%s" % (self.email) 


class AddressPerson(models.Model):
    address = models.CharField(max_length=300, verbose_name= 'Dirección', default ='')   
    pais = models.CharField(max_length=50,  verbose_name='País', default="Cuba")
    contact = models.ForeignKey(Persona, on_delete= models.CASCADE)

    class Meta:
        verbose_name_plural = 'Listado de Direcciones'
        verbose_name =  "Dirección"
        unique_together = ('address', 'pais', 'contact')
    
    def __unicode__(self):
        return u"%s/%s" % (self.address, self.pais) 

# ---------------- END PERSONA -------------------------------------------------

# ---------------- ENTIDAD -----------------------------------------------------
class Entidad(models.Model):
    SEXO =(('F', 'Femenino'), ('M', 'Masculino'))
    ESTADO_CIVIL = (('S', 'Solter'),('C','Casad'), ('V', 'Viud'), ('D', 'Divorciad'))
    nombre = models.CharField(max_length = 100,  verbose_name='Nombre', default = " ")
    servicios = models.CharField(max_length=100, verbose_name='Servicios/Productos')
    nacionalidad = models.CharField(max_length=50,  verbose_name='Nacionalidad', default="Cubana")
    aniversario = models.DateField(blank = True, null=True)
    fiesta = models.DateField(verbose_name='Fiesta Nacional',blank = True, null=True)
    sitio_web = models.URLField( verbose_name='Sitio Web',blank = True)
    categoria = models.ManyToManyField(Categoria)
    proyecto = models.ManyToManyField(Proyecto)    
    observaciones = models.TextField(blank = True)
    created_by = models.ForeignKey(OnCubaUser, verbose_name = 'Creado por', default = 1)
    marked_for_deletion = models.BooleanField(default = False)
    date_marked = models.DateTimeField(blank = True, default =t.now)

    def nombre_completo(self):
        return u"%s" % (self.nombre)    

    class Meta:
        verbose_name_plural = 'Entidades'
        verbose_name = 'Entidad'

    def __unicode__(self):
        return u"%s" % (self.nombre) 

class ContactPerson(models.Model):
    persona = models.CharField(max_length = 200 , verbose_name = 'Persona de Contacto')
    cargo = models.CharField(max_length = 100 , verbose_name = 'Cargo')
    numbers = models.CharField(max_length=100, verbose_name= 'Número(s) de Teléfono', null=True, blank=True)
    emails = models.CharField(max_length=400, verbose_name= 'Correo(s) Electrónico(s)', null=True, blank=True)
    entidad = models.ForeignKey(Entidad)

    class Meta:
        verbose_name = 'Persona de Contacto'
        verbose_name_plural = 'Personas de Contacto'
        unique_together = ('persona', 'cargo', 'entidad')

    def __unicode__(self):
        return u"%s %s" % (self.persona, self.cargo)         

class PhoneNumberEntidad(models.Model):
    number = models.CharField(max_length=50, verbose_name= 'Número de Teléfono')
    contact = models.ForeignKey(Entidad, on_delete= models.CASCADE)

    class Meta:
        verbose_name_plural = 'Listado de Teléfonos'
        verbose_name =  "Número de Teléfono"
        unique_together =('number', 'contact')

    def __unicode__(self):
        return u"%s" % (self.number) 

class EmailEntidad(models.Model):
    email = models.EmailField(verbose_name = 'Correo Electrónico')
    contact = models.ForeignKey(Entidad, on_delete= models.CASCADE)

    class Meta:
        verbose_name_plural = 'Listado de Correos'
        verbose_name =  "Correo Electrónico"
        unique_together = ("email", "contact")   

    def __unicode__(self):
        return u"%s" % (self.email) 
    

class AddressEntidad(models.Model):
    address = models.CharField(max_length=300, verbose_name= 'Dirección', default ='')
    pais = models.CharField(max_length=50,  verbose_name='País', default='Cuba')    
    contact = models.ForeignKey(Entidad, on_delete= models.CASCADE)

    class Meta:
        verbose_name_plural = 'Listado de Direcciones'
        verbose_name =  'Dirección'
        unique_together = ('address', 'pais', 'contact')

# ---------------- END ENTIDAD -------------------------------------------------


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