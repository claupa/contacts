#-*- coding: utf8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden

from django.views.generic import UpdateView
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import django.utils.timezone as t
from django.core.mail import send_mail

from .forms import CreateContactForm, CreateAddressForm, CreatePhoneForm, CreateEmailForm,OnCubaUserForm,\
                   CreateContactFormEntidad, CreateAddressFormEntidad, CreatePhoneFormEntidad, CreateEmailFormEntidad,\
                   InvitationForm, CrearUsuario
from .models import PhoneNumberPerson, EmailPerson, AddressPerson,Persona,\
                PhoneNumberEntidad, EmailEntidad, AddressEntidad, Entidad, OnCubaUser, UserTracker, Invitacion, Role
from .utils import check_credentials
from django.contrib.auth.models import User




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
            
            history = UserTracker(user = request.user, action= 'C', persona = persona, fecha = t.now() )
            history.save()
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

def editar_persona(request, contact_id, template="oncuba/edit_contact.html"):
    
    persona = Persona.objects.get(pk=contact_id)
    address = AddressPerson.objects.filter(contact__pk = contact_id)[0]
    phone = PhoneNumberPerson.objects.filter(contact__pk= contact_id)[0]
    email = EmailPerson.objects.filter(contact__pk= contact_id)[0]
    
    if request.method == 'POST':
        form_contact = CreateContactForm(request.POST)
        form_address = CreateAddressForm(request.POST)
        form_phone = CreatePhoneForm(request.POST)
        form_email = CreateEmailForm(request.POST)
        form_phone.modification = True
        form_email.modification = True
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']
        

        if form_contact.is_valid() and form_address.is_valid() and form_phone.is_valid() and form_email.is_valid():
            persona.nombre = form_contact.cleaned_data['nombre']
            persona.apellidos = form_contact.cleaned_data['apellidos']
            persona.lugar = form_contact.cleaned_data['lugar_de_trabajo']
            persona.ocupacion = form_contact.cleaned_data['ocupacion']
            persona.pais = form_contact.cleaned_data['pais']
            persona.fecha_de_nacimiento = form_contact.cleaned_data['fecha_nac']
            persona.sexo = form_contact.cleaned_data['sexo']
            persona.estado = form_contact.cleaned_data['estado_civil']
            persona.hijos = form_contact.cleaned_data['hijos']
            persona.sitio_web = form_contact.cleaned_data['sitio_web']
            persona.observaciones = form_contact.cleaned_data['observaciones']
            
            persona.categoria.clear()
            persona.proyecto.clear()

            for categoria in form_contact.cleaned_data['categoria']:
                persona.categoria.add(categoria)

            for proyecto in form_contact.cleaned_data['proyecto']:
                persona.proyecto.add(proyecto)
            persona.save()

            phone.number = form_phone.cleaned_data['number']
            phone.descripcion =  form_phone.cleaned_data['phone_descripcion']
            phone.save()

            email.email = form_email.cleaned_data['email']
            email.descripcion =  form_email.cleaned_data['email_descripcion']
            email.save()
            
            address.address_one = form_address.cleaned_data['address_one']
            address.provincia = form_address.cleaned_data['provincia']
            address.municipio= form_address.cleaned_data['municipio']
            address.descripcion = form_address.cleaned_data['descripcion']
            address.save()
        
        history = UserTracker(user = request.user, action= 'M', persona = persona, fecha = t.now() )
        history.save()
            
        return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactForm(model_to_dict(persona)) 
        form_address = CreateAddressForm(model_to_dict(address))
        # print model_to_dict(email)

        form_email = CreateEmailForm(model_to_dict(email))
        form_phone = CreatePhoneForm(model_to_dict(phone))
        form_phone.modification = True
        form_email.modification = True
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']

    return render(request, template, {'form':form_contact, 'address': form_address, 'phone': form_phone, 'email': form_email,
        'phone_description': phone.descripcion, 'email_description': email.descripcion, 'contact_id': contact_id})

def editar_entidad(request, contact_id, template="oncuba/edit_entidad.html"):
        
    entidad = Entidad.objects.get(pk=contact_id)
    address = AddressEntidad.objects.filter(contact__pk = contact_id)[0]
    phone = PhoneNumberEntidad.objects.filter(contact__pk= contact_id)[0]
    email = EmailEntidad.objects.filter(contact__pk= contact_id)[0]
    
    if request.method == 'POST':
        form_contact = CreateContactFormEntidad(request.POST)
        form_address = CreateAddressFormEntidad(request.POST)
        form_phone = CreatePhoneFormEntidad(request.POST)
        form_email = CreateEmailFormEntidad(request.POST)
        form_phone.modification = True
        form_email.modification = True
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']
        

        if form_contact.is_valid() and form_address.is_valid() and form_phone.is_valid() and form_email.is_valid():
            entidad.nombre = form_contact.cleaned_data['nombre']
            entidad.servicios = form_contact.cleaned_data['servicios']
            entidad.persona = form_contact.cleaned_data['persona']
            entidad.cargo = form_contact.cleaned_data['cargo']
            entidad.pais = form_contact.cleaned_data['pais']
            entidad.aniversario = form_contact.cleaned_data['aniversario']
            entidad.fiesta = form_contact.cleaned_data['fiesta']
            entidad.sitio_web = form_contact.cleaned_data['sitio_web']
            entidad.observaciones = form_contact.cleaned_data['observaciones']
            
            entidad.categoria.clear()
            entidad.proyecto.clear()

            for categoria in form_contact.cleaned_data['categoria']:
                entidad.categoria.add(categoria)

            for proyecto in form_contact.cleaned_data['proyecto']:
                entidad.proyecto.add(proyecto)
            entidad.save()

            phone.number = form_phone.cleaned_data['number']
            phone.descripcion =  form_phone.cleaned_data['phone_descripcion']
            phone.save()

            email.email = form_email.cleaned_data['email']
            email.descripcion =  form_email.cleaned_data['email_descripcion']
            email.save()
            
            address.address_one = form_address.cleaned_data['address_one']
            address.provincia = form_address.cleaned_data['provincia']
            address.municipio= form_address.cleaned_data['municipio']
            address.descripcion = form_address.cleaned_data['descripcion']
            address.save()
        history = UserTracker(user = request.user, action= 'M', entidad = entidad, fecha = t.now() )
        history.save()
        
        return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactFormEntidad(model_to_dict(entidad)) 
        form_address = CreateAddressFormEntidad(model_to_dict(address))
        # print model_to_dict(email)

        form_email = CreateEmailFormEntidad(model_to_dict(email))
        form_phone = CreatePhoneFormEntidad(model_to_dict(phone))
        form_phone.modification = True
        form_email.modification = True
        form_phone.fields['phone_descripcion'] = form_phone.fields['descripcion']
        del form_phone.fields['descripcion']
        form_email.fields['email_descripcion'] = form_email.fields['descripcion']
        del form_email.fields['descripcion']

    return render(request, template, {'form':form_contact, 'address': form_address, 'phone': form_phone, 'email': form_email,
        'phone_description': phone.descripcion, 'email_description': email.descripcion, 'contact_id': contact_id})

def view_persona(request, contact_id, template="oncuba/view_persona.html"):
    # Si tienes los permisos
    contact = Persona.objects.get(pk=contact_id)
    email = EmailPerson.objects.get(contact__pk = contact_id)
    phone = PhoneNumberPerson.objects.get(contact__pk= contact_id)
    address = AddressPerson.objects.get(contact__pk= contact_id)
    history = UserTracker(user = request.user, action= 'L', persona = contact, fecha = t.now() )
    history.save()
    
    return render(request, template, {'contact': contact, 'email': email , 'phone': phone, 'address': address})

def view_entidad(request, contact_id, template="oncuba/view_entidad.html"):
    # Si tienes los permisos
    contact = Entidad.objects.get(pk=contact_id)
    email = EmailEntidad.objects.get(contact__pk = contact_id)
    phone = PhoneNumberEntidad.objects.get(contact__pk= contact_id)
    address = AddressEntidad.objects.get(contact__pk= contact_id)
    history = UserTracker(user = request.user, action= 'L', entidad = contact, fecha = t.now() )
    history.save()
    
    return render(request, template, {'contact': contact, 'email': email , 'phone': phone, 'address': address})
        
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
            history = UserTracker(user = request.user, action= 'C', entidad = entidad, fecha = t.now() )
            history.save()
            
            
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


def create_oncuba_user(render, template="oncuba/create_oncuba_user.html"):
    pass

def edit_oncuba_user(request, template="oncuba/oncuba_user_form.html"):
    oncubauser = OnCubaUser.objects.get(user__pk = request.user.pk)
    if request.POST:
        form = OnCubaUserForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
            oncubauser.user.username = form.cleaned_data['username']
            oncubauser.user.first_name = form.cleaned_data['first_name']
            oncubauser.user.last_name = form.cleaned_data['last_name']
            oncubauser.user.email = form.cleaned_data['email']
            oncubauser.user.save()
            oncubauser.cargo = form.cleaned_data['cargo']
            # oncubauser.proyecto.clear()
            
            # for proyecto in form.cleaned_data['proyecto']:
            #     oncubauser.proyecto.add(proyecto)
            oncubauser.save()
            return redirect('/mi-perfil/')
    else:
        form = OnCubaUserForm({
            'username': oncubauser.user.username,
            'first_name' : oncubauser.user.first_name,
            'last_name' : oncubauser.user.last_name, 
            'email' : oncubauser.user.email,
            'cargo' : oncubauser.cargo,
            # 'proyecto' : oncubauser.proyecto
        })
    return render(request, template, {'form': form})

@login_required()
def view_oncuba_user(request, template="oncuba/view_oncuba_user.html"):
    oncubauser= OnCubaUser.objects.get(user = request.user)
    return render(request, template, {'oncubauser': oncubauser})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/mi-perfil/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'oncuba/change_password.html', {
        'form': form
    })

@login_required()
def delete_contact(request, contact_id, is_persona):
    contact = Persona.objects.get(pk = contact_id) if is_persona == 'True' else Entidad.objects.get(pk = contact_id)

    if check_credentials(contact, request.user):
        contact.marked_for_deletion = True;
        contact.date_marked = t.now()
        contact.save()
        if is_persona:
            history = UserTracker(user = request.user, action= 'L', persona = contact,fecha = t.now() )
            history.save()
        else:
            history = UserTracker(user = request.user, action= 'L', entidad = contact, fecha = t.now() )
            history.save()
            
        
    else:
        return HttpResponseForbidden()
    
    return redirect('/')

@login_required()
def invitar_usuario(request, template="oncuba/invitar_usuarios.html"):
    if request.POST:
        form = InvitationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            cargo = form.cleaned_data['cargo']
            role = Role.objects.get(pk = form.cleaned_data['role'])
            
            invitacion = Invitacion(username = username, first_name = first_name, last_name=last_name,
                                    email = email, phone_number = phone_number, cargo = cargo, role = role)
            invitacion.save()
            
            url =  request.build_absolute_uri('../aceptar-invitacion/' + str(invitacion.pk))
            text = """Hola,
  Has recibido una invitación para acceder al sitio de contactos de OnCuba. Para crear tu cuenta de usuario accede a:
  %s
            """ % url
            try:
                send_mail('Invitacion Sitio de Contacto OnCuba', text,'crmoncuba@gmail.com',[email], fail_silently=False)
            except:
                return render(request, template,{'form':form, 'error': 'El correo electrónico no funcionó'})                
            history = UserTracker(user = request.user, action= 'I', created_user = invitacion, fecha = t.now() )
            history.save()   
            
            return redirect('/')
    else:
        form = InvitationForm()
    
    return render(request, template, {'form': form})

from django.contrib.auth import logout
def aceptar_invitacion(request, o_id, template="oncuba/aceptar_invitacion.html"):
    invitacion = Invitacion.objects.get(pk=o_id)
    if invitacion.usada:
        return render(request, "oncuba/solicitar_usuario.html", {'error': error})
    if request.POST:
        form = CrearUsuario(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()

            cargo = form.cleaned_data['cargo']
            phone_number = form.cleaned_data['phone_number']
            role = invitacion.role
            oncubauser = OnCubaUser(user = user, cargo = cargo, phone_number = phone_number, role = role)
            oncubauser.save()

            invitacion.usada = True
            invitacion.save() 
            if request.user.is_authenticated:
                logout(request)
            return redirect('/entrar/')
    else:        
        form_dict = model_to_dict(invitacion)
        form_dict.pop('role')
        form = CrearUsuario(form_dict)       

    return render(request, template, {'form': form, 'id': o_id})
