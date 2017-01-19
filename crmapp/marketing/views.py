#-*- coding: utf8 -*-
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from crmapp.oncuba.models import Categoria, Proyecto, Persona, Entidad, Staff, PhoneNumberPerson, EmailPerson, PhoneNumberEntidad, EmailEntidad
from crmapp.oncuba.utils import check_credentials
from django.contrib.auth.decorators import login_required
from .forms import FilterForm, FilterStaffForm, ExportForm
from django.db.models import Q
from django.forms.models import model_to_dict
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.http import HttpResponse, HttpResponseRedirect


def home_page(request, template='marketing/home.html'):
    if request.user.is_anonymous():
        return redirect('/entrar/')
    contact_person = Persona.objects.filter(marked_for_deletion = False)
    contact_entidad = Entidad.objects.filter(marked_for_deletion = False)
    creado_por = None
    s = ''
    if request.GET:
        s =request.GET['s']
         
        contact_person = contact_person.filter(Q(nombre__icontains = s) | Q(lugar_de_trabajo__icontains=s)\
        | Q(ocupacion__icontains=s))
        contact_entidad = contact_entidad.filter(Q(nombre__icontains = s) | Q(servicios__icontains=s) )

    if request.POST:
        filter_form = FilterForm(request.POST)
        if filter_form.is_valid():
            tipos = filter_form.cleaned_data['tipos']
            categoria = filter_form.cleaned_data['categoria']
            proyecto = filter_form.cleaned_data['proyecto']
            creado_por = filter_form.cleaned_data['creado_por']

            print(creado_por)

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
    
    contacts = get_contact_info(contact_person, request.user, creado_por, True)
    contacts.extend(get_contact_info(contact_entidad, request.user, creado_por,  False))
    staff = get_staff_info()

    index = 0
    for contact in contacts:
        index += 1
        contact['index'] = index

    return render(request, template, {'s': s,
                                    'filter_form':filter_form, 
                                    'categorias' : Categoria.objects.all(),
                                    'proyectos': Proyecto.objects.all(),
                                    'contacts': contacts,
                                    'staff' : staff,
                                    'staff_count': len(staff)})

@login_required()
def mis_contactos(request, template= "marketing/mis_contactos.html"):
    db_personas= Persona.objects.filter(created_by__user__username=request.user.username).filter(marked_for_deletion = False)
    db_entidades= Entidad.objects.filter(created_by__user__username=request.user.username).filter(marked_for_deletion = False)

    contacts = get_contact_info(db_personas, request.user)
    contacts.extend(get_contact_info(db_entidades, request.user, persona = False))
    index = 0
    for contact in contacts:
        index += 1
        contact['index'] = index

    return render(request, template, {'contacts': contacts})

def get_proyectos(staff):
    prs = ''
    for proyecto in staff.proyectos.all():
        prs += proyecto.name +'-'
    return prs[:-1]

@login_required()
def export_staff(request, template="marketing/export_staff.html"):    
    staff = [model_to_dict(st) for st in Staff.objects.all()]

    if request.POST:
        filter_form = FilterStaffForm(request.POST)

        if filter_form.is_valid():
            campos = filter_form.cleaned_data['campos']
            for st in staff:
                if 'A' in campos:
                    break
                if not 'N' in campos:
                    st.pop('nombre')
                    st.pop('apellidos')
                if not 'E' in campos:
                    st.pop('email')
                if not 'T' in campos:
                    st.pop('phone_number')
                if not 'C' in campos:
                    st.pop('cargo')
                if not 'P' in campos:
                    st.pop('proyectos')
                    
            for st in staff:
                if 'proyectos' in st:
                    st['proyectos'] =[ p.name for p in Proyecto.objects.filter(pk__in = st['proyectos'])]
                else: break

            if 'exportdoc' in request.POST:
                response = HttpResponse(format_staff_doc(staff), content_type='application/vnd.ms-word')
                response['Content-Disposition'] = 'attachment; filename=staff.doc'
                return response  
            else:
            
                
                # Create the HttpResponse object with the appropriate PDF headers.
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="staff.pdf"'


                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response, pagesize = letter)
                width, height = letter
                p.setFont("Helvetica", 12)
                y = height - 50

                for st in staff:
                    if y - len(format_staff(st))*20 < 40:
                        p.showPage()
                        y = height - 50 
                    for field in format_staff(st):                
                        p.drawString(50, y, field)  
                        y -= 20
                    y -= 20
                # Close the PDF object cleanly, and we're done.
                p.showPage()
                p.save()
                return response
            
    else:
        filter_form = FilterStaffForm()

    return render(request, template, {'form': filter_form, 'staff': staff})

@login_required
def export_contacts(request, template="marketing/export_contact.html"):
    contact_person = Persona.objects.filter(marked_for_deletion = False)
    contact_entidad = Entidad.objects.filter(marked_for_deletion = False)
    
    if request.POST:
        filter_form = ExportForm(request.POST)
        if filter_form.is_valid():
            tipos = filter_form.cleaned_data['tipos']
            categoria = filter_form.cleaned_data['categoria']
            proyecto = filter_form.cleaned_data['proyecto']
            creado_por = filter_form.cleaned_data['creado_por']
            
            
            if tipos == 'T' or tipos == 'P':
                contact_person = check_list(categoria, proyecto, contact_person)
                if tipos == 'P':
                    contact_entidad = []
            if tipos =='T' or tipos == 'E':
                contact_entidad = check_list(categoria, proyecto, contact_entidad)
                if tipos=='E':
                    contact_person = []


            contacts = get_contact_info(contact_person, request.user, creado_por, persona = True)
            contacts.extend(get_contact_info(contact_entidad, request.user,creado_por, persona =  False))  

            if not contacts or 'filtrar' in request.POST:
                return render(request, template, { 'filter_form':filter_form, 
                                                'categorias' : Categoria.objects.all(),
                                                'proyectos': Proyecto.objects.all(),
                                                'contacts': contacts,})
            if 'export' in request.POST:
                
                contacts = [format_persona(x) for x in contact_person]
                contacts.extend([format_entidad(x) for x in contact_entidad])
                # Create the HttpResponse object with the appropriate PDF headers.
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="contactos.pdf"'


                # Create the PDF object, using the response object as its "file."
                p = canvas.Canvas(response, pagesize = letter)
                width, height = letter
                p.setFont("Helvetica", 12)
                y = height - 50

                for st in contacts:
                    if y - len(st)*20 < 40:
                        p.showPage()
                        y = height - 50 
                    for field in st:                
                        p.drawString(50, y, field)  
                        y -= 20
                    y -= 20
                # Close the PDF object cleanly, and we're done.
                p.showPage()
                p.save()
                return response

                    
            if 'exportdoc' in request.POST:
                contacts = [format_persona(x) for x in contact_person]
                contacts.extend([format_entidad(x) for x in contact_entidad])
                text = ""
                for c in contacts:
                    text += '\n'.join(c)
                    text += '\n\n'
                response = HttpResponse(text, content_type='application/vnd.ms-word')
                response['Content-Disposition'] = 'attachment; filename=contactos.doc'
                return response 
    else:
        filter_form = ExportForm()
        contacts = get_contact_info(contact_person, request.user,creado_por,  persona =  True)
        contacts.extend(get_contact_info(contact_entidad, request.user,creado_por, persona  = False))  
        
        return render(request, template, { 'filter_form':filter_form, 
                                                'categorias' : Categoria.objects.all(),
                                                'proyectos': Proyecto.objects.all(),
                                                'contacts': contacts,})
    


# --------------------------------------------------- Utils -------------------------------------------------
def format_persona(contact):
    result = []
    result.append(contact.nombre)
    result.append(contact.ocupacion+'/'+contact.lugar_de_trabajo)
    phones = PhoneNumberPerson.objects.filter(contact_id = contact.pk)
    result.append(', '.join([p.number for p in phones]))
    email = EmailPerson.objects.filter(contact_id = contact.pk)
    result.append(', '.join([e.email for e in email]))
    return result

def format_entidad(contact):
    result = []
    result.append(contact.nombre)
    result.append(contact.servicios)
    phones = PhoneNumberEntidad.objects.filter(contact_id = contact.pk)
    result.append(', '.join([p.number for p in phones]))
    email = EmailEntidad.objects.filter(contact_id = contact.pk)
    result.append(', '.join([e.email for e in email]))
    return result
    

def format_staff_doc(staff):
    result = "\n"
    for st in staff:
        fields = format_staff(st)
        result += '\n'.join(fields) 
        result +='\n\n'
        
    return result

def format_staff(st):
    result = []
    if 'nombre' in st:
        result.append(st['nombre'] + ' '+ st['apellidos'])
    if 'email' in st:
        result.append(st['email'])
    if 'phone_number' in st:
        result.append(st['phone_number'])    
    if 'proyectos' in st:
        result.append(', '.join(st['proyectos']))
    if 'cargo' in st:
        result.append(st['cargo'])
    return result
            

def get_staff_info():
    staff = []
    index = 0
    for s in Staff.objects.all():
        index += 1 
        staff.append({
            'index' : index,
            'nombre' : s.nombre + ' ' + s.apellidos,
            'cargo' : s.cargo + '/' + get_proyectos(s),
            'email' : s.email 
        })
    return staff


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

def get_contact_info(contacts, user, creado_por=[], persona = True):
    new_contacts = []
    index = 0
    print(persona)
    if persona:
        fn = get_name_and_ocupation_of_persona
    else:
        fn = get_name_and_ocupation_of_entidad

    for contact in contacts:
        if creado_por and int(creado_por) != contact.created_by.pk:
            continue
        index +=1
        creator = contact.created_by.user
        is_owner_or_admin = creator == user or user.is_superuser
        
        new_contact = {'index' : index,
                    'nombre' : fn(contact)[0],
                    'ocupacion': fn(contact)[1],
                    'created_by': creator.first_name + ' ' + creator.last_name,
                    'can_read': check_credentials(contact, user),
                    'can_edit': is_owner_or_admin,
                    'can_delete': is_owner_or_admin,
                    'is_persona': persona}
        if new_contact['can_read']:
            new_contact['id'] = contact.pk
        new_contacts.append(new_contact)
    return new_contacts

def get_name_and_ocupation_of_persona(contact):
    return (contact.nombre, contact.ocupacion+'/'+contact.lugar_de_trabajo)

def get_name_and_ocupation_of_entidad(contact):
    return (contact.nombre, contact.servicios)