#-*- coding: utf8 -*-
from django import forms
from crmapp.oncuba.models import Proyecto, Categoria
from crmapp.oncuba.models import OnCubaUser

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
        self.fields['creado_por'] =  forms.ChoiceField(widget=forms.Select,
                                         choices=tuple([(up.pk, up.user.first_name+' '+ up.user.last_name ) for up in OnCubaUser.objects.all()]),
                                         required= False)                  

class FilterStaffForm(forms.Form):
    choices_tipo = ((u'A' , u'Todos'),(u'N', u'Nombre y Apellidos'),(u'E', u'Correo Electrónico'), 
                    (u'T', u'Número de Teléfono'),(u'C', u'Cargo'),(u'P', u'Proyectos') )
    campos = forms.MultipleChoiceField(label="Campos a Exportar", initial='A', widget=forms.SelectMultiple,choices = choices_tipo)


class ExportForm(forms.Form):
    choices_tipo = ((u'T' , u'Todos'),(u'P', u'Persona'),(u'E', u'Entidad')  )
    tipos = forms.CharField(label="Tipos de Contacto", initial='T', widget=forms.Select(choices = choices_tipo))
    
    def __init__(self, *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['proyecto'] =  forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(proyecto.pk, proyecto.name) for proyecto in Proyecto.objects.all()]),
                                         required= False)
        self.fields['categoria'] = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                         choices=tuple([(categoria.pk, categoria.name) for categoria in Categoria.objects.all()]),
                                         required=False) 
        self.fields['creado_por'] =  forms.ChoiceField(widget=forms.Select,
                                         choices=tuple([(up.pk, up.user.first_name+' '+ up.user.last_name ) for up in OnCubaUser.objects.all()]),
                                         required= False)  

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2