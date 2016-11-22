#-*- coding: utf8 -*-
from django import forms
from django.forms import  formsets

from .models import Persona, AddressPerson, PhoneNumberPerson, EmailPerson
from .models import Entidad, AddressEntidad, PhoneNumberEntidad, EmailEntidad
from .models import Categoria, OnCubaUser, Role, ContactPerson
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core import validators
from django.core.exceptions import ValidationError
from authtools.forms import UserCreationForm

class CreateContactForm(forms.ModelForm):
    YEARS = range(1900,2017)
    fecha_nac = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])), required = False) 

    def __init__(self , *args, **kwargs):
        super(CreateContactForm, self).__init__( *args, **kwargs)
        self.fields['sitio_web'].widget.attrs['placeholder'] = 'http://www.example.com'

    class Meta:
        model = Persona
        fields = ('nombre', 'lugar_de_trabajo', 'ocupacion', 'nacionalidad',
                  'sexo', 'estado_civil', 'hijos', 'observaciones',
                  'sitio_web', 'categoria', 'proyecto')
                  

class CreateContactFormEntidad(forms.ModelForm):
    YEARS = range(1900,2017)
    aniversario = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])), required = False)  
    fiesta =  forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])), required = False)
    
    class Meta:
        model = Entidad
        fields = ('nombre', 'servicios', 'nacionalidad',  'observaciones','sitio_web', 'categoria', 'proyecto')

    def __init__(self , *args, **kwargs):
        super(CreateContactFormEntidad, self).__init__( *args, **kwargs)
        self.fields['sitio_web'].widget.attrs['placeholder'] = 'http://www.example.com'

class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ('persona', 'cargo', 'numbers', 'emails')

    def __init__(self , *args, **kwargs):
        super(ContactPersonForm, self).__init__( *args, **kwargs)
        self.fields['persona'].widget.attrs['placeholder'] = 'Nombre y Apellidos'
        self.fields['cargo'].widget.attrs['placeholder'] = 'Cargo'
        self.fields['numbers'].widget.attrs['placeholder'] = '+555 5555 (casa), +555 5555 (movil), ...'
        self.fields['emails'].widget.attrs['placeholder'] = 'correo1@correo.com, correo2@correo.com, ...'
        
class CreateAddressForm(forms.Form):
    address = forms.CharField(required=False, widget=forms.TextInput(), label="Dirección")
    pais = forms.CharField(required=False, widget=forms.TextInput(), label="País")

    def __init__(self , *args, **kwargs):
        super(CreateAddressForm, self).__init__( *args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Calle 0 e/ 0 y 0 #000, Municipio, Provincia'

class CreatePhoneForm(forms.Form):
    number = forms.CharField(label="Número de teléfono", widget=forms.TextInput())

    def __init__(self , *args, **kwargs):
        super(CreatePhoneForm, self).__init__( *args, **kwargs)
        self.fields['number'].widget.attrs.update({
                'placeholder': '+53 55555555 (casa)',
            })

class CreateEmailForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico")

    def __init__(self, *args, **kwargs):
        super(CreateEmailForm, self).__init__(*args, **kwargs)        
        self.fields['email'].widget.attrs.update({'placeholder':'correo@algo.com'})

AddressFormSet = formsets.formset_factory(CreateAddressForm, extra=0, min_num=0)
PhoneFormSet = formsets.formset_factory(CreatePhoneForm, min_num=1, extra=0)
EmailFormSet = formsets.formset_factory(CreateEmailForm, min_num =1, extra= 0)
ContactPersonFormSet = formsets.formset_factory(ContactPersonForm, min_num =1, extra= 0)        


class CrearUsuario(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(required= True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
    password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
    cargo = forms.CharField(required= True, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(required= True, widget=forms.TextInput(attrs={'class':'form-control'}))
        
class OnCubaUserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput())
    last_name = forms.CharField(required=False, widget=forms.TextInput())
    email = forms.EmailField(required=True, widget=forms.TextInput())
    phone_number = forms.CharField(required= False, widget=forms.TextInput())

    class Meta:
        model = OnCubaUser
        fields = ('cargo',)

class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

class InvitationForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput())
    last_name = forms.CharField(required=True, widget=forms.TextInput())
    email = forms.EmailField(required=True, widget=forms.TextInput())
    username = forms.CharField(required= True, widget=forms.TextInput())
    cargo = forms.CharField(required= True, widget=forms.TextInput())
    phone_number = forms.CharField(required= True, widget=forms.TextInput())
    
    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__()
        self.role_choices =tuple([(x.pk,x.name) for x in Role.objects.all()])
        self.fields['role'] = forms.ChoiceField(widget=forms.Select(),
                                         choices=tuple([(x.pk,x.name) for x in Role.objects.all()]),
                                         required= True)

class ActivateUser(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ActivateUser, self).__init__()
        self.fields['role']= forms.ChoiceField(widget=forms.Select(),
                                         choices=tuple([(x.pk,x.name) for x in Role.objects.all()]),
                                         required= True)
        self.fields['role'].widget.attrs['class'] = "dropdown"