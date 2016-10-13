#-*- coding: utf8 -*-
from django import forms

from .models import Persona, Entidad


class CreateContactForm(forms.ModelForm):
    YEARS = range(1900,2017)

    fecha_nac = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))
    
    
    class Meta:
        model = Persona
        # exclude = ('hijos',)
        fields = ('nombre', 'apellidos',
                  'lugar_de_trabajo', 'ocupacion', 'pais',
                  'sexo', 'estado_civil', 'hijos', 'observaciones',
                  'sitio_web', 'categoria', 'proyecto')


        # widgets = {
        #     'nombre': forms.TextInput(
        #         attrs={'placeholder':'First Name', 'class':'form-control'}
        #     ),
        #     'apellidos': forms.TextInput(
        #         attrs={'placeholder':'Last Name', 'class':'form-control'}
        #     ),
        #     'lugar_de_trabajo': forms.TextInput(
        #         attrs={'placeholder':'Role', 'class':'form-control'}
        #     ),
        #     'phone': forms.TextInput(
        #         attrs={'placeholder':'Teléfono', 'class':'form-control'}
        #     ),
        #     'fecha_de_nacimiento': forms.DateInput(
        #         attrs={'placeholder':'Fecha de Nacimiento', 'class':'form-control'}
        #     ),
        # }