from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .forms import CreateContactForm

# Create your views here.
def create_contact(request, template="oncuba/create_contact_persona.html"):
    if not request.user.is_authenticated():
        raise PermissionDenied   
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