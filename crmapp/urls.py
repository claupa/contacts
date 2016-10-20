"""crmapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from marketing.views import home_page, mis_contactos
from suscribers.views import subscriber_new
import django.contrib.auth.views as djauth
from contact.urls import contact_urls
from contact.views import contact_cru
from oncuba.views import create_persona, create_entidad, view_persona,view_entidad, editar_persona, editar_entidad,\
view_oncuba_user, change_password, edit_oncuba_user, delete_contact, invitar_usuario, aceptar_invitacion

urlpatterns = [
    # Marketing pages
    url(r'^admin/', admin.site.urls),
    # url(r'^admin/oncuba/roles/$', admin.site.urls, name="roles"),
    url(r'^$', home_page, name="home"),

    # Subscriber related URLs
    # url(r'^signup/$', subscriber_new, name='sub_new'),
    url(r'^nueva-persona/$', create_persona, name='create_contact_persona'),
    url(r'^nueva-entidad/$', create_entidad, name='create_contact_entidad'),
    url(r'^editar-persona/(?P<contact_id>.*)/$', editar_persona, name='editar_persona'),
    url(r'^editar-entidad/(?P<contact_id>.*)/$', editar_entidad, name='editar_entidad'),
    url(r'^ver-persona/(?P<contact_id>.*)/$', view_persona, name='view_persona'),
    url(r'^ver-entidad/(?P<contact_id>.*)/$', view_entidad, name='view_entidad'),
    url(r'^mi-perfil/$', view_oncuba_user, name='view_perfil'),
    url(r'^editar-perfil/$', edit_oncuba_user, name='editar-perfil'),
    url(r'^borrar-contacto/(?P<contact_id>.*)/(?P<is_persona>.*)$', delete_contact, name='delete-contact'),
    url(r'^password/$', change_password, name='change_password'),    
    url(r'^mis-contactos/$', mis_contactos, name='mis_contactos'),
    url(r'^invitar-usuario/+$', invitar_usuario, name='invitar-usuario'),
    url(r'^aceptar-invitacion/(?P<o_id>.*)/?$', aceptar_invitacion, name='aceptar-invitacion'),

    url(r'^entrar/$', djauth.login, {'template_name': 'login.html'}, name ='login'),
    url(r'^logout/$',djauth.logout, {'next_page': '/entrar/'}),

]
