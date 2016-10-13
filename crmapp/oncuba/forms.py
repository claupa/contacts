#-*- coding: utf8 -*-
from django import forms

from .models import Persona, AddressPerson, PhoneNumberPerson, EmailPerson
from .models import Entidad, AddressEntidad, PhoneNumberEntidad, EmailEntidad


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
    
    class Meta:
        model = PhoneNumberPerson
        fields = ('number', 'descripcion')

class CreateEmailForm(forms.ModelForm):
    class Meta:
        model = EmailPerson
        fields = ('email', 'descripcion')

class CreateAddressFormEntidad(forms.ModelForm):
    class Meta:
        model = AddressEntidad
        fields = ('address_one', 'provincia', 'municipio', 'descripcion')

class CreatePhoneFormEntidad(forms.ModelForm):
    class Meta:
        model = PhoneNumberEntidad
        fields = ('number', 'descripcion')

class CreateEmailFormEntidad(forms.ModelForm):
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