#-*- coding: utf8 -*-
from .models import Persona, Entidad, OnCubaUser

def check_credentials(contact, user):
    oncubauser = OnCubaUser.objects.get(user=user)
    if user.is_superuser:
        return True
    if contact.created_by.user.username == user.username :
        return True
    if not oncubauser.role:
        return False
    role = oncubauser.role
    for categoria in role.categories.all():
        if categoria in contact.categoria.all():
            return True
    for proyecto in role.proyectos.all():
        if proyecto in contact.proyecto.all():
            return True
    return False

import datetime as dt
from datetime import datetime, timedelta
def get_notifications():
    contacts = []
    persons = Persona.objects.filter(marked_for_deletion = True)
    entidades = Entidad.objects.filter(marked_for_deletion = True)
    notifications = get_dates_from(persons)
    notifications.extend(get_dates_from(entidades , False))
    messages = merge_notifications(notifications)
    print messages
    


def get_dates_from(contacts, persona=True):
    contacts_to_notify = []    
    fn = get_message_for_person if persona else get_message_for_entidad
    for contact in contacts:
        celebrate = fn(contact)
        if celebrate:
            print contact.created_by.user.email
            email =contact.created_by.user.email            
            contacts_to_notify.append((contact.created_by.user.email, celebrate))
    return contacts_to_notify

def merge_notifications(contacts):
    messages = {}
    for email,message in contacts:
        if messages.has_key(email):
            messages[email].append(message)
        else:
            messages[email] = [message]
    return messages

def get_message_for_person(contact):
    if contact.fecha_de_nacimiento  - timedelta(days=7) == dt.date.today():        
        name =  u'%s %s' % (contact.nombre , contact.apellidos)
        date = contact.fecha_de_nacimiento.strftime('%d/%m/%Y')
        message = u'En una semana es el cumpleaños de %s (%s).' % (name, date)
        return message
    else:
        return ''

def get_message_for_entidad(contact):
    name =  '%s' % (contact.nombre)    
    if contact.aniversario - timedelta(days=7) == dt.date.today():        
        date = contact.aniversario.strftime('%d/%m/%Y')
        message = u'En una semana es el aniversario de %s (%s).' % (name, date)
        return message
    if contact.fiesta - timedelta(days=7) == dt.date.today():
        date = contact.fiesta.strftime('%d/%m/%Y')
        message = u'En una semana es la fiesta nacional de %s (%s).' % (name, date)
        return message
    else:
        return ''




# import cStringIO as StringIO
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# from cgi import escape


# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     context = Context(context_dict)
#     html  = template.render(context)
#     result = StringIO.StringIO()

#     pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
