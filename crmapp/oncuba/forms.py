#-*- coding: utf8 -*-
from django import forms

from .models import Persona, Entidad


class CreateContactForm(forms.ModelForm):
    YEARS = range(1900,2017)

    fecha_nac = forms.DateField(widget=forms.SelectDateWidget(years=tuple(YEARS[-1::-1])))
    # fecha_nac = forms.DateField(widget = forms.widgets.DateInput())
    
    class Meta:
        model = Persona
        # exclude = ('hijos',)
        fields = ('nombre', 'apellidos',
                  'lugar_de_trabajo', 'ocupacion', 'pais', 'fecha_de_nacimiento',
                  'sexo', 'estado_civil', 'hijos'
        )

    # nombre = models.CharField(max_length = 100,  verbose_name='Nombre(s)', default = " ")
    # apellidos = models.CharField(max_length = 100, verbose_name='Apellido(s)', default = " ")
    # lugar_de_trabajo = models.CharField(max_length=50, verbose_name='Lugar de Trabajo')
    # ocupacion = models.CharField(max_length = 50,verbose_name='Ocupación')    
    # pais = models.CharField(max_length=50,  verbose_name='País', default="Cuba")

    # fecha_de_nacimiento = models.DateField(verbose_name = 'Fecha de Nacimiento',blank = True)
    # sexo = models.CharField(max_length = 1, choices = SEXO,blank = True)
    # estado_civil = models.CharField(max_length = 1, choices=ESTADO_CIVIL,blank = True)
    # hijos = models.BooleanField()

    # sitio_web = models.URLField( verbose_name='Sitio Web', blank = True)
    # categoria = models.ManyToManyField(Categoria)
    # proyecto = models.ManyToManyField(Proyecto)
    # observaciones = models.TextField(blank = True)
    # created_by = models.ForeignKey(OnCubaUser, verbose_name = 'Creado por',default = 1)
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