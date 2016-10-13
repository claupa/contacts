from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from crmapp.oncuba.models import Categoria, Proyecto, Persona, Entidad 
from crmapp.oncuba.utils import check_credentials
from django.contrib.auth.decorators import login_required

# class HomePage(TemplateView):
#     """
#     Because our needs are so simple, all we have to do is
#     assign one value; template_name. The home.html file will be created
#     in the next lesson.
#     """
#     template_name = 'marketing/home.html'

def home_page(request, template='marketing/home.html'):
    # if request.method == 'POST':
    #     form = SubscriberForm(request.POST)
    #     if form.is_valid():
            # Unpack form values
     
            # Create Subscriber Record
            # Process payment (via Stripe)
            # Auto login the user
            # return HttpResponseRedirect('/success/')
    # else:
        # form = SubscriberForm()
    db_personas= Persona.objects.all()
    
    contacts =[]
    index = 0
    for persona in db_personas:
        index +=1
        contacts.append({'index' : index,
                        'nombre' : persona.nombre+ ' '+ persona.apellidos,
                        'ocupacion': persona.ocupacion + '/'+ persona.lugar_de_trabajo,
                        'created_by': persona.created_by.username,
                        'can_edit': persona.created_by.username == request.user.username,
                        'can_read': check_credentials(persona, request.user),
                        })
        if contacts[-1]['can_read']:
            contacts[-1]['id'] = persona.pk 
            # print contacts[-1]
        

    return render(request, template, {'categorias' : Categoria.objects.all(),
                                    'proyectos': Proyecto.objects.all(),
                                    'contacts': contacts})
@login_required()
def mis_contactos(request, template= "marketing/mis_contactos.html"):
    
    db_personas= Persona.objects.filter(created_by__user__username=request.user.username)
    
    contacts =[]
    index = 0
    for persona in db_personas:
        index +=1 
        contacts.append({'index' : index,
                        'nombre' : persona.nombre+ ' '+ persona.apellidos,
                        'ocupacion': persona.ocupacion + '/'+ persona.lugar_de_trabajo,
                        'created_by': persona.created_by.username,
                        'can_edit': persona.created_by.user.username == request.user.username,
                        'can_read': check_credentials(persona, request.user),
                        'can_delete': persona.created_by.user.username == request.user.username })
        if contacts[-1]['can_read']:
            contacts[-1]['id'] = persona.pk 
            # print contacts[-1]

    return render(request, template, {'contacts': contacts})