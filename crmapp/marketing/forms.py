#-*- coding: utf8 -*-
from django import forms
from crmapp.oncuba.models import Proyecto, Categoria

class FilterForm(forms.Form):
    choices_tipo = ((u'T' , u'Todos'),(u'P', u'Persona'),(u'E', u'Entidad')  )
    tipos = forms.CharField(label="Tipos de Contacto", initial='T', widget=forms.Select(choices = choices_tipo))

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['proyecto'] =  forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(proyecto.pk, proyecto.name) for proyecto in Proyecto.objects.all()]),
                                         required= False)
        self.fields['categoria'] = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(categoria.pk, categoria.name) for categoria in Categoria.objects.all()]),
                                         required=False)                    

class FilterStaffForm(forms.Form):
    choices_tipo = ((u'A' , u'Todos'),(u'N', u'Nombre y Apellidos'),(u'E', u'Correo Electrónico'), 
                    (u'T', u'Número de Teléfono'),(u'C', u'Cargo'),(u'P', u'Proyectos') )
    campos = forms.MultipleChoiceField(label="Campos a Exportar", initial='A', widget=forms.SelectMultiple,choices = choices_tipo)


class ExportForm(forms.Form):
    choices_tipo = ((u'T' , u'Todos'),(u'P', u'Persona'),(u'E', u'Entidad')  )
    tipos = forms.CharField(label="Tipos de Contacto", initial='T', widget=forms.Select(choices = choices_tipo))
    # choices_persona = ((u'A' , u'Todos'),(u'N', u'Nombre'),(u'E', u'Correo Electrónico'), 
    #                 (u'T', u'Número de Teléfono'),(u'C', u'Cargo'),(u'P', u'Proyectos') )
    # campos_persona = forms.MultipleChoiceField(label="Campos a Exportar", initial='A', widget=forms.SelectMultiple,choices = choices_tipo)

    # choices_entidad = ((u'A' , u'Todos'),(u'N', u'Nombre'),(u'E', u'Correo Electrónico'), 
    #                 (u'T', u'Número de Teléfono'),(u'P', u'Persona de Contacto') )
    # campos_entidad = forms.MultipleChoiceField(label="Campos a Exportar", initial='A', widget=forms.SelectMultiple,choices = choices_tipo)

    def __init__(self, *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['proyecto'] =  forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(proyecto.pk, proyecto.name) for proyecto in Proyecto.objects.all()]),
                                         required= False)
        self.fields['categoria'] = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(categoria.pk, categoria.name) for categoria in Categoria.objects.all()]),
                                         required=False) 