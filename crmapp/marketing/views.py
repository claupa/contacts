from django.shortcuts import render
from django.views.generic.base import TemplateView
from crmapp.oncuba.models import Categoria, Proyecto, Persona, Entidad 
from crmapp.oncuba.utils import check_credentials
from django.contrib.auth.decorators import login_required
from crmapp.oncuba.forms import FilterForm

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

def home_page(request, template='marketing/home.html'):
    contact_person = Persona.objects.all()
    contact_entidad = Entidad.objects.all()
    
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
    contacts =[]
    index = 0
    for persona in contact_person:
        index +=1
        contacts.append({'index' : index,
                        'nombre' : persona.nombre+ ' '+ persona.apellidos,
                        'ocupacion': persona.ocupacion + '/'+ persona.lugar_de_trabajo,
                        'created_by': persona.created_by.user.username,
                        'can_edit': persona.created_by.user.username == request.user.username,
                        'can_read': check_credentials(persona, request.user),
                        'is_persona' : True
                        })
        if contacts[-1]['can_read']:
            contacts[-1]['id'] = persona.pk 
            # print contacts[-1]
    for entidad in contact_entidad:
        index +=1 
        contacts.append({'index' : index,
                        'nombre' : entidad.nombre,
                        'ocupacion': entidad.servicios,
                        'created_by': entidad.created_by.user.username,
                        'can_edit': entidad.created_by.user.username == request.user.username,
                        'can_read': check_credentials(entidad, request.user),
                        'can_delete': entidad.created_by.user.username == request.user.username,
                        'is_persona' : False
                         })
        if contacts[-1]['can_read']:
            contacts[-1]['id'] = entidad.pk 

    return render(request, template, {'filter_form':filter_form, 'categorias' : Categoria.objects.all(),
                                    'proyectos': Proyecto.objects.all(),
                                    'contacts': contacts})
@login_required()
def mis_contactos(request, template= "marketing/mis_contactos.html"):
    
    db_personas= Persona.objects.filter(created_by__user__username=request.user.username)
    db_entidades= Entidad.objects.filter(created_by__user__username=request.user.username)
    print db_personas.count()
    print db_entidades.count()

    contacts =[]
    index = 0
    for persona in db_personas:
        index +=1 
        contacts.append({'index' : index,
                        'nombre' : persona.nombre+ ' '+ persona.apellidos,
                        'ocupacion': persona.ocupacion + '/'+ persona.lugar_de_trabajo,
                        'created_by': persona.created_by.user.username,
                        'can_edit': persona.created_by.user.username == request.user.username,
                        'can_read': check_credentials(persona, request.user),
                        'can_delete': persona.created_by.user.username == request.user.username,
                        'is_persona': True })
        if contacts[-1]['can_read']:
            contacts[-1]['id'] = persona.pk 
            # print contacts[-1]

    for entidad in db_entidades:
        index +=1 
        contacts.append({'index' : index,
                        'nombre' : entidad.nombre,
                        'ocupacion': entidad.servicios,
                        'created_by': entidad.created_by.username,
                        'can_edit': entidad.created_by.user.username == request.user.username,
                        'can_read': check_credentials(entidad, request.user),
                        'can_delete': entidad.created_by.user.username == request.user.username ,
                        'is_persona': False})
        if contacts[-1]['can_read']:
            contacts[-1]['id'] = entidad.pk 

    return render(request, template, {'contacts': contacts})