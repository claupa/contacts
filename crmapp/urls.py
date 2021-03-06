from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views as djauth
from marketing.views import home_page, mis_contactos, export_staff, export_contacts, get_count, ResetPasswordRequestView, PasswordResetConfirmView
from oncuba.views import create_persona, create_entidad, view_persona,view_entidad, editar_persona, editar_entidad,\
view_oncuba_user, change_password, edit_oncuba_user, delete_contact, invitar_usuario, aceptar_invitacion, solicitar_usuario,\
get_solicitudes, activar_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_page, name="home"),
    url(r'^reset-passwd/$', ResetPasswordRequestView.as_view(), {}, name="reset"),
    url(r'^password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='reset_password_confirm'), 
    url(r'^num-solicitud/?$', get_count , name="counting"),
    url(r'^nueva-persona/?$', create_persona, name='create_contact_persona'),
    url(r'^nueva-entidad/?$', create_entidad, name='create_contact_entidad'),
    url(r'^editar-persona/(?P<contact_id>.*)/?$', editar_persona, name='editar_persona'),
    url(r'^editar-entidad/(?P<contact_id>.*)/?$', editar_entidad, name='editar_entidad'),
    url(r'^ver-persona/(?P<contact_id>.*)/?$', view_persona, name='view_persona'),
    url(r'^ver-entidad/(?P<contact_id>.*)/?$', view_entidad, name='view_entidad'),
    url(r'^mi-perfil/?$', view_oncuba_user, name='view_perfil'),
    url(r'^editar-perfil/?$', edit_oncuba_user, name='editar-perfil'),
    url(r'^borrar-contacto/(?P<contact_id>.*)/(?P<is_persona>.*)/?$', delete_contact, name='delete-contact'),
    url(r'^password/?$', change_password, name='change_password'),    
    url(r'^mis-contactos/?$', mis_contactos, name='mis_contactos'),
    url(r'^invitar-usuario/?$', invitar_usuario, name='invitar-usuario'),
    url(r'^solicitar-usuario/?$', solicitar_usuario, name='solicitar-usuario'),
    url(r'^aceptar-invitacion/(?P<o_id>.*)/?$', aceptar_invitacion, name='aceptar-invitacion'),
    url(r'^entrar/?$', djauth.login, {'template_name': 'login.html'}, name = 'entrar'),
    url(r'^logout/?$', djauth.logout, {'next_page': '/entrar/'}),
    url(r'^exportar-staff/?$', export_staff,name='filter-staff-export'),
    url(r'^exportar-contactos/?$', export_contacts, name='filter-contact-export'),
    
    url(r'^solicitudes/?$', get_solicitudes, name='get-solicitudes'),
    url(r'^activar-usuario/(?P<contact_id>.*)/?$', activar_user, name = 'activar-user'),
]
