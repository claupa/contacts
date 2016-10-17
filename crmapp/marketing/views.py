from django.shortcuts import render
from django.views.generic.base import TemplateView
from crmapp.oncuba.models import Categoria, Proyecto, Persona, Entidad 
from crmapp.oncuba.utils import check_credentials
from django.contrib.auth.decorators import login_required
from crmapp.oncuba.forms import FilterForm
from django.db.models import Q

@login_required()
def home_page(request, template='marketing/home.html'):
    contact_person = Persona.objects.filter(marked_for_deletion = False)
    contact_entidad = Entidad.objects.filter(marked_for_deletion = False)
    s = ''
    if request.GET:
        s =request.GET['s']
         
        contact_person = contact_person.filter(Q(nombre__icontains = s) | Q(apellidos__icontains=s) | Q(lugar_de_trabajo__icontains=s)\
        | Q(ocupacion__icontains=s))
        contact_entidad = contact_entidad.filter(Q(nombre__icontains = s) | Q(servicios__icontains=s) | Q(persona__icontains=s)\
        | Q(cargo__icontains=s))

    if request.POST:
        filter_form = FilterForm(request.POST)
        # print request.POST
        if filter_form.is_valid():
            tipos = filter_form.cleaned_data['tipos']
            categoria = filter_form.cleaned_data['categoria']
            proyecto = filter_form.cleaned_data['proyecto']
            
            if tipos == 'T' or tipos == 'P':
                contact_person = check_list(categoria, proyecto, contact_person)
                if tipos == 'P':
                    contact_entidad = []
            if tipos =='T' or tipos == 'E':
                contact_entidad = check_list(categoria, proyecto, contact_entidad)
                if tipos=='E':
                    contact_person = []
    else:
        filter_form = FilterForm()
    
    contacts = get_contact_info(contact_person, request.user, True)
    contacts.extend(get_contact_info(contact_entidad, request.user, False))

    return render(request, template, {'s': s,
                                    'filter_form':filter_form, 
                                    'categorias' : Categoria.objects.all(),
                                    'proyectos': Proyecto.objects.all(),
                                    'contacts': contacts})

@login_required()
def mis_contactos(request, template= "marketing/mis_contactos.html"):
    db_personas= Persona.objects.filter(created_by__user__username=request.user.username).filter(marked_for_deletion = False)
    db_entidades= Entidad.objects.filter(created_by__user__username=request.user.username).filter(marked_for_deletion = False)

    contacts = get_contact_info(db_personas, request.user)
    contacts.extend(get_contact_info(db_entidades, request.user, False))

    return render(request, template, {'contacts': contacts})

# --------------------------------------------------- Utils -------------------------------------------------
def check_list(categorias, proyectos, contacts):
    possible_contacts = []
    if categorias:
        for categoria in categorias:
            for contact in contacts:
                if contact.categoria.filter(pk=categoria).exists() and not contact in possible_contacts:
                    possible_contacts.append(contact)
        contacts= possible_contacts
        possible_contacts = []
    if proyectos:
        for proyecto in proyectos:
            for contact in contacts:
                if contact.proyecto.filter(pk=proyecto).exists() and not contact in possible_contacts:
                    possible_contacts.append(contact)
        contacts=possible_contacts
    return contacts

def get_contact_info(contacts, user, persona = True):
    new_contacts = []
    index = 0
    if persona:
        fn = get_name_and_ocupation_of_persona
    else:
        fn = get_name_and_ocupation_of_entidad

    for contact in contacts:
        index +=1
        creator = contact.created_by.user
        is_owner_or_admin = creator == user or user.is_superuser
        
        new_contact = {'index' : index,
                    'nombre' : fn(contact)[0],
                    'ocupacion': fn(contact)[1],
                    'created_by': creator.username,
                    'can_read': check_credentials(contact, user),
                    'can_edit': is_owner_or_admin,
                    'can_delete': is_owner_or_admin,
                    'is_persona': persona}
        if new_contact['can_read']:
            new_contact['id'] = contact.pk
        new_contacts.append(new_contact)
    return new_contacts

def get_name_and_ocupation_of_persona(contact):
    return (contact.nombre + ' ' + contact.apellidos , contact.ocupacion+'/'+contact.lugar_de_trabajo)

def get_name_and_ocupation_of_entidad(contact):
    return (contact.nombre, contact.servicios)