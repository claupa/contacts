from .models import Persona, Entidad, OnCubaUser

def check_credentials(contact, user):
    oncubauser = OnCubaUser.objects.get(user=user)
    if contact.created_by.user.username == user.username :
        return True
    if not oncubauser.role:
        return False
    role = oncubauser.role
    for categoria in role.categoria.all():
        if categoria in contact.categoria:
            return True
    for proyecto in role.proyecto.all():
        if proyecto in contact.proyecto.all():
            return True
    return False