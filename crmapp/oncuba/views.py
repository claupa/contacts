#-*- coding: utf8 -*-
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import CreateContactForm, CreateAddressForm, CreatePhoneForm, CreateEmailForm
from .forms import CreateContactFormEntidad, CreateAddressFormEntidad, CreatePhoneFormEntidad, CreateEmailFormEntidad
from .models import PhoneNumberPerson, EmailPerson, AddressPerson
from .models import PhoneNumberEntidad, EmailEntidad, AddressEntidad

from django.contrib.auth.decorators import login_required
from crmapp.oncuba.models import Persona, Entidad, OnCubaUser
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView

# Create your views here.
@login_required()
def create_persona(request, template="oncuba/create_contact_persona.html"):
    if request.method == 'POST':
        form_contact = CreateContactForm(request.POST)
        form_address = CreateAddressForm(request.POST)
        form_phone = CreatePhoneForm(request.POST)
        form_email = CreateEmailForm(request.POST)
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']
        

        if form_contact.is_valid() and form_address.is_valid() and form_phone.is_valid() and form_email.is_valid():
            nombre = form_contact.cleaned_data['nombre']
            apellidos = form_contact.cleaned_data['apellidos']
            lugar = form_contact.cleaned_data['lugar_de_trabajo']
            ocupacion = form_contact.cleaned_data['ocupacion']
            pais = form_contact.cleaned_data['pais']
            fecha_nac = form_contact.cleaned_data['fecha_nac']
            sexo = form_contact.cleaned_data['sexo']
            estado = form_contact.cleaned_data['estado_civil']
            hijos = form_contact.cleaned_data['hijos']
            sitio_web = form_contact.cleaned_data['sitio_web']
            categorias = form_contact.cleaned_data['categoria']
            proyectos = form_contact.cleaned_data['proyecto']
            observaciones = form_contact.cleaned_data['observaciones']
            
            # Create the User record
            persona = Persona(nombre= nombre, apellidos = apellidos, lugar_de_trabajo = lugar,
            ocupacion = ocupacion, pais=pais, fecha_de_nacimiento=fecha_nac, sexo = sexo, estado_civil = estado,
            hijos= hijos, sitio_web=sitio_web, observaciones = observaciones,
            created_by= OnCubaUser.objects.get(user= request.user))
            persona.save()

            for categoria in categorias:
                persona.categoria.add(categoria)

            for proyecto in proyectos:
                persona.proyecto.add(proyecto)

            persona.save()

            phone_number = PhoneNumberPerson(contact = persona, number = form_phone.cleaned_data['number'],
                             descripcion = form_phone.cleaned_data['phone_descripcion'] )
            phone_number.save()
            email = EmailPerson(contact = persona, email = form_email.cleaned_data['email'],
                             descripcion = form_email.cleaned_data['email_descripcion'] )
            email.save()
            
            address = AddressPerson(contact = persona, address_one= form_address.cleaned_data['address_one'],
                                    provincia = form_address.cleaned_data['provincia'], municipio= form_address.cleaned_data['municipio']
                                    , descripcion = form_address.cleaned_data['descripcion']) 
            address.save()
            
            return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactForm() 
        form_address = CreateAddressForm()

        form_email = CreateEmailForm()
        form_phone = CreatePhoneForm()
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']       

    return render(request, template, {'form':form_contact, 'address': form_address, 'phone': form_phone, 'email': form_email})

def edit_persona(request, template="oncuba/create_contact_persona.html"):
    if request.method == 'POST':
        form = CreateContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            lugar = form.cleaned_data['lugar_de_trabajo']
            ocupacion = form.cleaned_data['ocupacion']
            pais = form.cleaned_data['pais']
            fecha_nac = form.cleaned_data['fecha_nac']
            sexo = form.cleaned_data['sexo']
            estado = form.cleaned_data['estado_civil']
            hijos = form.cleaned_data['hijos']
            sitio_web = form.cleaned_data['sitio_web']
            categorias = form.cleaned_data['categoria']
            proyectos = form.cleaned_data['proyecto']
            observaciones = form.cleaned_data['observaciones']
            
            # Create the User record
            persona = Persona(nombre= nombre, apellidos = apellidos, lugar_de_trabajo = lugar,
            ocupacion = ocupacion, pais=pais, fecha_de_nacimiento=fecha_nac, sexo = sexo, estado_civil = estado,
            hijos= hijos, sitio_web=sitio_web, observaciones = observaciones,
            created_by= OnCubaUser.objects.get(user= request.user))
            persona.save()

            for categoria in categorias:
                persona.categoria.add(categoria)

            for proyecto in proyectos:
                persona.proyecto.add(proyecto)

            persona.save()
            
            return HttpResponseRedirect('/')
        else:
            form = CreateContactForm()

        return render(request, template, {'form':form})

def view_contact(request, contact_id, template=""):
    print  "View Contact"
    return HttpResponseRedirect('/mis-contactos/')
        
@login_required()
def create_entidad(request, template="oncuba/create_contact_entidad.html"):
    if request.method == 'POST':
        form_contact = CreateContactFormEntidad(request.POST)
        form_address = CreateAddressFormEntidad(request.POST)
        form_phone = CreatePhoneFormEntidad(request.POST)
        form_email = CreateEmailFormEntidad(request.POST)
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']
        

        if form_contact.is_valid() and form_address.is_valid() and form_phone.is_valid() and form_email.is_valid():
            nombre = form_contact.cleaned_data['nombre']
            servicios = form_contact.cleaned_data['servicios']
            persona = form_contact.cleaned_data['persona']
            cargo = form_contact.cleaned_data['cargo']
            pais = form_contact.cleaned_data['pais']
            aniv = form_contact.cleaned_data['aniversario']
            fiesta = form_contact.cleaned_data['fiesta']
            sitio_web = form_contact.cleaned_data['sitio_web']
            categorias = form_contact.cleaned_data['categoria']
            proyectos = form_contact.cleaned_data['proyecto']
            observaciones = form_contact.cleaned_data['observaciones']
            
            entidad = Entidad(nombre= nombre, servicios = servicios, persona = persona, cargo=cargo, pais=pais, aniversario=aniv,
                fiesta= fiesta, sitio_web=sitio_web, observaciones = observaciones,
            created_by= OnCubaUser.objects.get(user= request.user))
            entidad.save()

            for categoria in categorias:
                entidad.categoria.add(categoria)

            for proyecto in proyectos:
                entidad.proyecto.add(proyecto)

            entidad.save()

            phone_number = PhoneNumberEntidad(contact = entidad, number = form_phone.cleaned_data['number'],
                             descripcion = form_phone.cleaned_data['phone_descripcion'] )
            phone_number.save()
            email = EmailEntidad(contact = entidad, email = form_email.cleaned_data['email'],
                             descripcion = form_email.cleaned_data['email_descripcion'] )
            email.save()
            
            address = AddressEntidad(contact = entidad, address_one= form_address.cleaned_data['address_one'],
                                    provincia = form_address.cleaned_data['provincia'], municipio= form_address.cleaned_data['municipio']
                                    , descripcion = form_address.cleaned_data['descripcion']) 
            address.save()
            
            return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactFormEntidad() 
        form_address = CreateAddressFormEntidad()

        form_email = CreateEmailFormEntidad()
        form_phone = CreatePhoneFormEntidad()
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']       

    return render(request, template, {'form':form_contact, 'address': form_address, 'phone': form_phone, 'email': form_email})