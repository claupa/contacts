from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from crmapp.oncuba.models import Categoria, Proyecto

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

    return render(request, template, {'categorias' : Categoria.objects.all(),
                                        'proyectos': Proyecto.objects.all()})