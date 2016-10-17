from django.contrib import admin
from .models import Categoria, Proyecto,Role, Persona, Entidad, PhoneNumberEntidad, PhoneNumberPerson,\
EmailEntidad, EmailPerson, AddressEntidad, AddressPerson, OnCubaUser, Staff
from django.contrib.auth.models import User

admin.site.register(Categoria)
admin.site.register(Proyecto)
admin.site.register(Role)

# class InlineUser(admin.StackedInline):
    # model = User

class OnCubaUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo')
    search_fields = ['user__username', 'cargo']
    # inlines = (InlineUser,)

admin.site.register(OnCubaUser, OnCubaUserAdmin)


class InlinePhone(admin.StackedInline):
    model = PhoneNumberEntidad
    extra = 0

class InlineEmail(admin.StackedInline):
    model = EmailEntidad
    extra = 0

class InlineAddress(admin.StackedInline):
    model = AddressEntidad
    extra = 0

class EntidadAdmin(admin.ModelAdmin):
    inlines = (InlinePhone, InlineEmail, InlineAddress )
    list_filter = ('proyecto', 'categoria')
    search_fields = ['nombre', 'servicios','persona','cargo', 'proyecto__name', 'categoria__name']

admin.site.register(Entidad, EntidadAdmin)

class InlinePhoneP(admin.StackedInline):
    model = PhoneNumberPerson
    extra = 0

class InlineEmailP(admin.StackedInline):
    model = EmailPerson
    extra = 0

class InlineAddressP(admin.StackedInline):
    model = AddressPerson
    extra = 0

class PersonaAdmin(admin.ModelAdmin):
    inlines = (InlinePhoneP, InlineEmailP, InlineAddressP )
    list_filter = ('proyecto', 'categoria')
    search_fields = ['nombre', 'apellidos','lugar_de_trabajo','ocupacion', 'proyecto__name', 'categoria__name']

admin.site.register(Persona, PersonaAdmin)

admin.site.register(Staff)