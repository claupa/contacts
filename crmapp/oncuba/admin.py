from django.contrib import admin
from .models import Categoria, Proyecto,Role, Persona, Entidad, PhoneNumberEntidad, PhoneNumberPerson,\
EmailEntidad, EmailPerson, AddressEntidad, AddressPerson, OnCubaUser, Staff, UserTracker, Invitacion
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Categoria)
admin.site.register(Proyecto)
admin.site.register(Role)

class InlineOnCubaUser(admin.StackedInline):
    model = OnCubaUser
    extra = 0
    max_num =1
    min_num = 1
    can_delete= False

# class OnCubaUserAdmin(admin.ModelAdmin):
#     list_display = ('username',)
#     # search_fields = ['user__username', 'cargo']
#     inlines = (InlineOnCubaUser,)

UserAdmin.inlines = (InlineOnCubaUser,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

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
admin.site.register(Invitacion)

class UserTrackerAdmin(admin.ModelAdmin):
    list_filter =('action',)
admin.site.register(UserTracker, UserTrackerAdmin)
