#-*- coding: utf8 -*-
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import CreateContactForm
from django.contrib.auth.decorators import login_required
from crmapp.oncuba.models import Persona, Entidad, OnCubaUser
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView

# Create your views here.
@login_required()
def create_persona(request, template="oncuba/create_contact_persona.html"):
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
def create_entidad(request, template="oncuba/create_contact_persona.html"):
    if request.method == 'POST':
        form = CreateContactForm(request.POST)
        if form.is_valid():
            # Unpack form values
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            # Create the User record
            user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            # Create Subscriber Record
            address_one = form.cleaned_data['address_one']
            address_two = form.cleaned_data['address_two']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            sub = Subscriber(address_one=address_one, address_two=address_two,
                            city=city, state=state, user_rec=user)
            sub.save()
            return HttpResponseRedirect('/home/')
    else:
        form = CreateContactForm()

    return render(request, template, {'form':form})