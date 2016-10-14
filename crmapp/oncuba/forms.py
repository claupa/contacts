#-*- coding: utf8 -*-
from django import forms

from .models import Persona, AddressPerson, PhoneNumberPerson, EmailPerson
from .models import Entidad, AddressEntidad, PhoneNumberEntidad, EmailEntidad
from .models import Proyecto, Categoria


class CreateContactForm(forms.ModelForm):
    YEARS = range(1900,2017)
    fecha_nac = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))   
     

    class Meta:
        model = Persona
        fields = ('nombre', 'apellidos',
                  'lugar_de_trabajo', 'ocupacion', 'pais',
                  'sexo', 'estado_civil', 'hijos', 'observaciones',
                  'sitio_web', 'categoria', 'proyecto')

class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = AddressPerson
        fields = ('address_one', 'provincia', 'municipio', 'descripcion')

class CreatePhoneForm(forms.ModelForm):
    modification = False

    def validate_unique(self):
        if self.modification:
            return True
        else: 
            return super(CreatePhoneForm, self).validate_unique()
    
    class Meta:
        model = PhoneNumberPerson
        fields = ('number', 'descripcion')

class CreateEmailForm(forms.ModelForm):
    modification = False

    def validate_unique(self):
        if self.modification:
            return True
        else: 
            return super(CreateEmailForm, self).validate_unique()
            
    class Meta:
        model = EmailPerson
        fields = ('email', 'descripcion')

class CreateAddressFormEntidad(forms.ModelForm):
    class Meta:
        model = AddressEntidad
        fields = ('address_one', 'provincia', 'municipio', 'descripcion')

class CreatePhoneFormEntidad(forms.ModelForm):
    modification = False
    def validate_unique(self):
        if self.modification:
            return True
        else: 
            return super(CreatePhoneFormEntidad, self).validate_unique()
    class Meta:
        model = PhoneNumberEntidad
        fields = ('number', 'descripcion')

class CreateEmailFormEntidad(forms.ModelForm):
    modification = False

    def validate_unique(self):
        if self.modification:
            return True
        else: 
            return super(CreateEmailFormEntidad, self).validate_unique()
    class Meta:
        model = EmailEntidad
        fields = ('email', 'descripcion')

class CreateContactFormEntidad(forms.ModelForm):
    YEARS = range(1900,2017)

    aniversario = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))  
    fiesta =  forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))

    class Meta:
        model = Entidad
        fields = ('nombre', 'servicios', 'persona' , 'cargo',
                 'pais',  'observaciones','sitio_web', 'categoria', 'proyecto')

class FilterForm(forms.Form):
    choices_tipo = ((u'T' , u'Todos'),(u'P', u'Persona'),(u'E', u'Entidad')  )
    tipos = forms.CharField(label="Tipos de Contacto",
                                initial='T',
                                widget=forms.Select(choices = choices_tipo),
                                )
    proyecto_choices = tuple([(proyecto.pk, proyecto.name) for proyecto in Proyecto.objects.all()])
    categoria_choices = tuple([(categoria.pk, categoria.name) for categoria in Categoria.objects.all()])
    
    proyecto = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple(proyecto_choices),
                                         required= False)
    categoria = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple(categoria_choices),
                                         required=False)
        