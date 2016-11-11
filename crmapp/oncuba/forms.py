#-*- coding: utf8 -*-
from django import forms
from django.forms import  formsets

from .models import Persona, AddressPerson, PhoneNumberPerson, EmailPerson
from .models import Entidad, AddressEntidad, PhoneNumberEntidad, EmailEntidad
from .models import Proyecto, Categoria, OnCubaUser,Role, ContactPerson
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core import validators
from django.core.exceptions import ValidationError



class CreateContactForm(forms.ModelForm):
    YEARS = range(1900,2017)
    fecha_nac = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))  

    class Meta:
        model = Persona
        fields = ('nombre', 'lugar_de_trabajo', 'ocupacion', 'nacionalidad',
                  'sexo', 'estado_civil', 'hijos', 'observaciones',
                  'sitio_web', 'categoria', 'proyecto')

class MinLengthValidator(validators.MinLengthValidator):
    message = 'Ensure this value has at least %(limit_value)d elements (it has %(show_value)d).'

class MaxLengthValidator(validators.MaxLengthValidator):
    message = 'Ensure this value has at most %(limit_value)d elements (it has %(show_value)d).'

class CommaSeparatedCharField(forms.Field):
    def __init__(self, dedup=True, max_length=None, min_length=None, *args, **kwargs):
        self.dedup, self.max_length, self.min_length = dedup, max_length, min_length
        super(CommaSeparatedCharField, self).__init__(*args, **kwargs)
        if min_length is not None:
            self.validators.append(MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(MaxLengthValidator(max_length))

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(',') if item.strip()]
        if self.dedup:
            value = list(set(value))

        return value

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value

class CreateAddressForm(forms.Form):
    address = CommaSeparatedCharField()
    pais = forms.CharField(required=False, widget=forms.TextInput(), label="País")

    def __init__(self , *args, **kwargs):
        super(CreateAddressForm, self).__init__( *args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Calle 0 e/ 0 y 0 #000, Municipio, Provincia'


AddressFormSet = formsets.formset_factory(CreateAddressForm, extra=0, min_num=0)


class CreatePhoneForm(forms.Form):
    number = forms.CharField(label="Número de teléfono",
                                widget=forms.TextInput()
                                )

    def __init__(self , *args, **kwargs):
        super(CreatePhoneForm, self).__init__( *args, **kwargs)
        self.fields['number'].widget.attrs.update({
                'placeholder': '+53 55555555 (casa)',
            })

PhoneFormSet = formsets.formset_factory(CreatePhoneForm, min_num=1, extra=0)


class CreateEmailForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico"
                                )

    def __init__(self, *args, **kwargs):
        super(CreateEmailForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs.update({'placeholder':'correo@algo.com'})

EmailFormSet = formsets.formset_factory(CreateEmailForm, min_num =1, extra= 0)

class CreateContactFormEntidad(forms.ModelForm):
    YEARS = range(1900,2017)

    aniversario = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))  
    fiesta =  forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))
    
    class Meta:
        model = Entidad
        fields = ('nombre', 'servicios', 'nacionalidad',  'observaciones','sitio_web', 'categoria', 'proyecto')

class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ('persona', 'cargo', 'numbers', 'emails')

ContactPersonFormSet = formsets.formset_factory(ContactPersonForm, min_num =1, extra= 0)

class FilterForm(forms.Form):
    choices_tipo = ((u'T' , u'Todos'),(u'P', u'Persona'),(u'E', u'Entidad')  )
    proyecto_choices = tuple([(proyecto.pk, proyecto.name) for proyecto in Proyecto.objects.all()])
    categoria_choices= tuple([(categoria.pk, categoria.name) for categoria in Categoria.objects.all()])
    proyecto = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=proyecto_choices,
                                         required= False)
    categoria = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=categoria_choices,
                                         required=False)
    tipos = forms.CharField(label="Tipos de Contacto",
                                initial='T',
                                widget=forms.Select(choices = choices_tipo)
                                )
    def __init__(self):
        super(FilterForm, self).__init__()
        self.fields['proyecto'] =  forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(proyecto.pk, proyecto.name) for proyecto in Proyecto.objects.all()]),
                                         required= False)
        self.fields['categoria'] = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(categoria.pk, categoria.name) for categoria in Categoria.objects.all()]),
                                         required=False)                            

class CrearUsuario(UserCreationForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
    password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
    cargo = forms.CharField(required= False, widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(required= False, widget=forms.TextInput(attrs={'class':'form-control'}))
        
class OnCubaUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    first_name = forms.CharField(required=False, widget=forms.TextInput())
    last_name = forms.CharField(required=False, widget=forms.TextInput())
    email = forms.EmailField(required=True, widget=forms.TextInput())
    phone_number = forms.CharField(required= False, widget=forms.TextInput())

    class Meta:
        model = OnCubaUser
        fields = ('cargo',)

from django import forms
from authtools.forms import UserCreationForm

class UserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

class InvitationForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput())
    last_name = forms.CharField(required=False, widget=forms.TextInput())
    email = forms.EmailField(required=True, widget=forms.TextInput())
    username = forms.CharField(required= False, widget=forms.TextInput())
    cargo = forms.CharField(required= True, widget=forms.TextInput())
    phone_number = forms.CharField(required= False, widget=forms.TextInput())
    
    role_choices =tuple([(x.pk,x.name) for x in Role.objects.all()])
    role = forms.ChoiceField(widget=forms.Select(),
                                         choices=role_choices,
                                         required= True)
    def __init__(self):
        super(InvitationForm, self).__init__()
        role = forms.ChoiceField(widget=forms.Select(),
                                         choices=tuple([(x.pk,x.name) for x in Role.objects.all()]),
                                         required= True)