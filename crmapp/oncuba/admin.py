from django.contrib import admin
from .models import Categoria, Proyecto,Role, Persona, Entidad, PhoneNumberEntidad, PhoneNumberPerson,\
EmailEntidad, EmailPerson, AddressEntidad, AddressPerson, OnCubaUser

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Proyecto)
admin.site.register(Role)
# admin.site.register(OnCubaUser)
class OnCubaUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo', 'proyectos')
    list_filter = ('proyecto',)
    search_fields = ['user__username', 'cargo', 'proyecto__name']

admin.site.register(OnCubaUser, OnCubaUserAdmin)


class InlinePhone(admin.StackedInline):
    model = PhoneNumberEntidad
    extra = 1

class InlineEmail(admin.StackedInline):
    model = EmailEntidad
    extra = 1

class InlineAddress(admin.StackedInline):
    model = AddressEntidad
    extra = 0

class EntidadAdmin(admin.ModelAdmin):
    inlines = (InlinePhone, InlineEmail, InlineAddress )

admin.site.register(Entidad, EntidadAdmin)

class InlinePhoneP(admin.StackedInline):
    model = PhoneNumberPerson
    extra = 1

class InlineEmailP(admin.StackedInline):
    model = EmailPerson
    extra = 1

class InlineAddressP(admin.StackedInline):
    model = AddressPerson
    extra = 0

class PersonaAdmin(admin.ModelAdmin):
    inlines = (InlinePhoneP, InlineEmailP, InlineAddressP )

admin.site.register(Persona, PersonaAdmin)

