#-*- coding: utf8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import UpdateView
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import django.utils.timezone as t
from django.core.mail import send_mail
from django.core.validators import validate_email
from .forms import CreateContactForm, CreateAddressForm, CreatePhoneForm, CreateEmailForm, OnCubaUserForm,\
                   CreateContactFormEntidad, InvitationForm, CrearUsuario,\
                   PhoneFormSet, EmailFormSet, AddressFormSet,  ContactPersonFormSet, ActivateUser
from .models import PhoneNumberPerson, EmailPerson, AddressPerson,Persona,ContactPerson,\
                PhoneNumberEntidad, EmailEntidad, AddressEntidad, Entidad, OnCubaUser, UserTracker, Invitacion, Role
from .utils import check_credentials


def save_person(form_contact, user=None, person = None):
    p = person or Persona()
    p.nombre = form_contact.cleaned_data['nombre']
    p.lugar_de_trabajo = form_contact.cleaned_data['lugar_de_trabajo']
    p.ocupacion = form_contact.cleaned_data['ocupacion']
    p.nacionalidad = form_contact.cleaned_data['nacionalidad']
    p.fecha_de_nacimiento = form_contact.cleaned_data['fecha_nac']
    p.sexo = form_contact.cleaned_data['sexo']
    p.estado_civil = form_contact.cleaned_data['estado_civil']
    p.hijos = form_contact.cleaned_data['hijos']
    p.sitio_web = form_contact.cleaned_data['sitio_web']
    p.observaciones = form_contact.cleaned_data['observaciones']
    
    if user:
        p.created_by = OnCubaUser.objects.get(user=user)
    
    p.save()   
    for categoria in form_contact.cleaned_data['categoria']:
        p.categoria.add(categoria)

    for proyecto in form_contact.cleaned_data['proyecto']:
        p.proyecto.add(proyecto) 
    
    p.save()
    return p

def update_phone_numbers(formset, persona, phones = None, PhoneClass=PhoneNumberPerson):    
    if phones:
        phones.delete()

    for phone_form in formset: 
        number = phone_form.cleaned_data['number']
        phone_number = PhoneClass(contact = persona, number =number)
        phone_number.save()

def update_emails(email_formset, persona, emails= None, EmailClass = EmailPerson):
    if emails:
        emails.delete()
    for email_form in email_formset:
        EmailClass.objects.create(contact = persona, email= email_form.cleaned_data['email'])

def update_address(addr_formset, persona, address = None, AddrClass=AddressPerson):
    if address:
        address.delete()
    for addr_form in addr_formset:
        address = addr_form.cleaned_data['address']
        new_address = AddrClass(contact = persona, address = address)
        new_address.pais = addr_form.cleaned_data['pais']
        new_address.save()
    
@login_required()
def create_persona(request, template="oncuba/persona/create_contact_persona.html"):  
    if request.method == 'POST':
        form_contact = CreateContactForm(request.POST)
        formset = PhoneFormSet(data=request.POST)
        email_formset= EmailFormSet(data=request.POST)
        addr_formset = AddressFormSet(data=request.POST)

        if form_contact.is_valid() and formset.is_valid() and email_formset.is_valid() and addr_formset.is_valid():
            persona = save_person(form_contact, request.user) 
            update_phone_numbers(formset, persona)
            update_emails(email_formset, persona)
            update_address(addr_formset, persona)           
            
            history = UserTracker(user = request.user, action= 'C', persona = persona, fecha = t.now() )
            history.save()
            return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactForm()         
        formset = PhoneFormSet()
        email_formset= EmailFormSet()
        addr_formset = AddressFormSet()

    return render(request, template, {'form':form_contact, 'formset': formset, 'email_formset':email_formset, 'addr_formset': addr_formset})

@login_required()
def view_persona(request, contact_id, template="oncuba/persona/view_persona.html"):
    # Si tienes los permisos
    contact = Persona.objects.get(pk=contact_id)
    email = EmailPerson.objects.filter(contact__pk = contact_id)
    phone = PhoneNumberPerson.objects.filter(contact__pk= contact_id)
    address = AddressPerson.objects.filter(contact__pk= contact_id)

    history = UserTracker(user = request.user, action= 'L', persona = contact, fecha = t.now() )
    history.save()

    creator = contact.created_by.user
    is_owner_or_admin = creator == request.user or request.user.is_superuser
    
    return render(request, template, {'contact_id':contact_id , 'can_delete': is_owner_or_admin,'contact': contact, 'email': email , 'phone': phone, 'address': address})

def editar_persona(request, contact_id, template="oncuba/persona/edit_contact.html"):    
    persona = Persona.objects.get(pk=contact_id)
    address = AddressPerson.objects.filter(contact__pk = contact_id)
    phone = PhoneNumberPerson.objects.filter(contact__pk= contact_id)
    emails = EmailPerson.objects.filter(contact__pk= contact_id)
    

    initial_phones = [{'number': phone_number.number} for phone_number in phone]
    initial_email = [{'email': email.email} for email in emails]
    initial_addr = [{'address': addr.address, 'pais': addr.pais} for addr in address]
    
    if request.method == 'POST':
        form_contact = CreateContactForm(request.POST)
        formset = PhoneFormSet(request.POST, initial=initial_phones, prefix ='phones')
        email_formset= EmailFormSet(request.POST, initial = initial_email, prefix ='email')
        addr_formset = AddressFormSet(request.POST, initial=initial_addr, prefix ='addr')
        
        if form_contact.is_valid() and formset.is_valid() and email_formset.is_valid() and addr_formset.is_valid():
            persona = save_person(form_contact,request.user, persona)
            
            update_phone_numbers(formset, persona, phone)
            update_emails(email_formset,persona, emails)
            update_address(addr_formset, persona, address)
        
            history = UserTracker(user = request.user, action= 'M', persona = persona, fecha = t.now() )
            history.save()
                
            return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactForm(model_to_dict(persona))
        formset = PhoneFormSet(initial =initial_phones, prefix = 'phones')
        email_formset= EmailFormSet(initial=initial_email, prefix = 'email')
        addr_formset = AddressFormSet(initial=initial_addr, prefix = 'addr')

    return render(request, template, {'form':form_contact, 'formset': formset,  'email_formset':email_formset, 'addr_formset': addr_formset,
                                'contact_id': contact_id})

def save_entidad(form_contact,user, entity= None):
    entidad = entity or Entidad()

    entidad.nombre = form_contact.cleaned_data['nombre']
    entidad.servicios = form_contact.cleaned_data['servicios']
    entidad.pais = form_contact.cleaned_data['nacionalidad']
    entidad.aniversario = form_contact.cleaned_data['aniversario']
    entidad.fiesta = form_contact.cleaned_data['fiesta']
    entidad.sitio_web = form_contact.cleaned_data['sitio_web']
    entidad.observaciones = form_contact.cleaned_data['observaciones']
    
    if user:
        entidad.created_by = OnCubaUser.objects.get(user=user)
    
    entidad.save()   
    if entity:
        entidad.categoria.clear()
        entidad.proyecto.clear()

    for categoria in form_contact.cleaned_data['categoria']:
        entidad.categoria.add(categoria)

    for proyecto in form_contact.cleaned_data['proyecto']:
        entidad.proyecto.add(proyecto) 
    
    entidad.save()
    return entidad
        
def update_contactperson(contact_formset, entidad, contacts = None):
    if contacts:
        contacts.delete()
    for contact_form in contact_formset:
        ContactPerson.objects.create(entidad = entidad, 
                                    persona= contact_form.cleaned_data['persona'],
                                    cargo= contact_form.cleaned_data['cargo'],
                                    numbers= contact_form.cleaned_data['numbers'],
                                    emails= contact_form.cleaned_data['emails'])

@login_required()
def create_entidad(request, template="oncuba/entidad/create_contact_entidad.html"):
    if request.method == 'POST':
        form_contact = CreateContactFormEntidad(request.POST)
        phone_formset = PhoneFormSet(request.POST, prefix="phones")
        email_formset = EmailFormSet(request.POST, prefix="email")
        addr_formset = AddressFormSet(request.POST, prefix = "addr")
        contact_formset = ContactPersonFormSet(request.POST, prefix = "contact")
        

        if form_contact.is_valid() and phone_formset.is_valid() and email_formset.is_valid() and addr_formset.is_valid() and contact_formset.is_valid():            
            entidad = save_entidad(form_contact, request.user)
            update_phone_numbers(phone_formset, entidad, PhoneClass=PhoneNumberEntidad)
            update_emails(email_formset, entidad, EmailClass=EmailEntidad)
            update_address(addr_formset, entidad,AddrClass=AddressEntidad)
            update_contactperson(contact_formset, entidad)
            history = UserTracker(user = request.user, action= 'C', entidad = entidad, fecha = t.now() )
            history.save()
                       
            return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactFormEntidad() 
        phone_formset = PhoneFormSet( prefix="phones")
        email_formset = EmailFormSet(prefix="email")
        addr_formset = AddressFormSet(prefix="addr")    
        contact_formset = ContactPersonFormSet(prefix = "contact")

    return render(request, template, {'form':form_contact, 
                                      'addr_formset': addr_formset, 
                                      'formset': phone_formset, 
                                      'email_formset': email_formset,
                                      'contact_formset': contact_formset})

def editar_entidad(request, contact_id, template="oncuba/entidad/edit_entidad.html"):        
    contacto = Entidad.objects.get(pk=contact_id)
    address = AddressEntidad.objects.filter(contact__pk = contact_id)
    phone = PhoneNumberEntidad.objects.filter(contact__pk= contact_id)
    email = EmailEntidad.objects.filter(contact__pk= contact_id)
    contacts = ContactPerson.objects.filter(entidad = contacto)
    
    
    initial_phones = [{'number': phone_number.number} for phone_number in phone]
    initial_email = [{'email': e.email} for e in email]
    initial_addr = [{'address': addr.address, 'pais': addr.pais} for addr in address]
    initial_contact = [model_to_dict(cp) for cp in contacts]

    if request.method == 'POST':
        form_contact = CreateContactFormEntidad(request.POST)
        phone_formset = PhoneFormSet(request.POST, initial = initial_phones, prefix ='phones')
        email_formset = EmailFormSet(request.POST, initial= initial_email, prefix = 'email' )
        addr_formset = AddressFormSet(request.POST, initial = initial_addr, prefix= 'addr')
        contact_formset = ContactPersonFormSet(request.POST, initial = initial_contact, prefix = 'contact')
        
        if form_contact.is_valid() and phone_formset.is_valid() and email_formset.is_valid() and addr_formset.is_valid() and contact_formset.is_valid():
            entidad = save_entidad(form_contact, request.user, contacto)

            update_phone_numbers(phone_formset, entidad, phone, PhoneClass=PhoneNumberEntidad)
            update_emails(email_formset, entidad,email, EmailClass=EmailEntidad)
            update_address(addr_formset, entidad, address,AddrClass=AddressEntidad)
            update_contactperson(contact_formset, entidad, contacts)
           
        history = UserTracker(user = request.user, action= 'M', entidad = contacto, fecha = t.now() )
        history.save()
        
        return HttpResponseRedirect('/')
    else:
        form_contact = CreateContactFormEntidad(model_to_dict(contacto)) 
        phone_formset = PhoneFormSet(initial = initial_phones, prefix = 'phones')
        email_formset = EmailFormSet(initial= initial_email, prefix = 'email' )
        addr_formset = AddressFormSet(initial = initial_addr, prefix= 'addr')
        contact_formset = ContactPersonFormSet(initial = initial_contact, prefix = 'contact')
        

    return render(request, template, {'form':form_contact, 
                                    'formset': phone_formset, 
                                    'email_formset': email_formset,
                                    'addr_formset': addr_formset,
                                    'contact_formset': contact_formset,
                                    'contact_id': contact_id})


@login_required
def view_entidad(request, contact_id, template="oncuba/entidad/view_entidad.html"):
    # Si tienes los permisos
    contact = Entidad.objects.get(pk=contact_id)
    email = EmailEntidad.objects.filter(contact__pk = contact_id)
    phone = PhoneNumberEntidad.objects.filter(contact__pk= contact_id)
    address = AddressEntidad.objects.filter(contact__pk= contact_id)
    contacts = ContactPerson.objects.filter(entidad = contact)

    history = UserTracker(user = request.user, action= 'L', entidad = contact, fecha = t.now() )
    history.save()    
    creator = contact.created_by.user
    is_owner_or_admin = creator == request.user or request.user.is_superuser
    
    return render(request, template, {'contact_id':contact_id , 'can_delete': is_owner_or_admin ,
                                    'contact': contact, 
                                    'email': email , 
                                    'phone': phone, 
                                    'address': address,
                                    'contacts': contacts})


def create_oncuba_user(render, template="oncuba/create_oncuba_user.html"):
    pass

def edit_oncuba_user(request, template="oncuba/oncuba-user/oncuba_user_form.html"):
    oncubauser = OnCubaUser.objects.get(user__pk = request.user.pk)
    if request.POST:
        form = OnCubaUserForm(request.POST)
        if form.is_valid():
            oncubauser.user.first_name = form.cleaned_data['first_name']
            oncubauser.user.last_name = form.cleaned_data['last_name']
            oncubauser.user.email = form.cleaned_data['email']
            oncubauser.user.save()
            oncubauser.cargo = form.cleaned_data['cargo']
            oncubauser.phone_number = form.cleaned_data['phone_number']
            oncubauser.save()
            return redirect('/mi-perfil/')
    else:
        form = OnCubaUserForm({
            'first_name' : oncubauser.user.first_name,
            'last_name' : oncubauser.user.last_name, 
            'email' : oncubauser.user.email,
            'cargo' : oncubauser.cargo,
            'phone_number': oncubauser.phone_number,
        })
    return render(request, template, {'form': form})

@login_required()
def view_oncuba_user(request, template="oncuba/oncuba-user/view_oncuba_user.html"):
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
    return render(request, 'oncuba/oncuba-user/change_password.html', {
        'form': form
    })

@login_required()
def delete_contact(request, contact_id, is_persona):
    contact = Persona.objects.get(pk = contact_id) if is_persona == 'True' else Entidad.objects.get(pk = contact_id)

    if check_credentials(contact, request.user):
        contact.marked_for_deletion = True;
        contact.date_marked = t.now()
        contact.save()
        if is_persona == 'True':
            history = UserTracker(user = request.user, action= 'B', persona = contact,fecha = t.now() )
            history.save()
        else:
            history = UserTracker(user = request.user, action= 'B', entidad = contact, fecha = t.now() )
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
            url =  request.build_absolute_uri('/aceptar-invitacion/' + str(invitacion.pk))
            text = "Hola, has recibido una invitación para acceder al sitio de contactos de OnCuba. Para crear tu cuenta de usuario accede a: %s" % url
            
            send_mail('Invitacion Sitio de Contacto OnCuba', text,'crmoncuba@gmail.com',[email], fail_silently=False)
            
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

def solicitar_usuario(request, template="oncuba/solicitar_usuario.html"):
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
            oncubauser = OnCubaUser(user = user, cargo = cargo, phone_number = phone_number)
            oncubauser.save()
            user.is_active = False
            user.save()
            return redirect('/')
    else:
        form = CrearUsuario()
    
    return render(request, template, {'form': form})
    
@login_required
def get_solicitudes(request, template = "oncuba/oncuba-user/oncuba_user_request.html"):
    oncubausers = OnCubaUser.objects.filter(user__is_active=False)
    solicitudes = [{'oncubauser': oncubauser, 'form': ActivateUser(), 'pk': oncubauser.user.pk} for oncubauser in oncubausers]
    return render(request, template, {'solicitudes': solicitudes})

@login_required
def activar_user(request, contact_id):
    if request.POST:
        form = ActivateUser(request.POST)
        role = request.POST['role']
        user = OnCubaUser.objects.get(user__pk = contact_id)
        user.role = Role.objects.get(pk = role)
        user.user.is_active = True
        user.user.save()
        user.save()
        send_mail('Sitio de Contacto OnCuba', "Su solicitud ha sido aceptada, para acceder al sitio vaya a: http://contactos.oncubamagazine.com/entrar/",'crmoncuba@gmail.com',[email], fail_silently=False)
    return redirect('/solicitudes/')


    