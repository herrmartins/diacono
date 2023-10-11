from users.models import CustomUser
from django.forms.models import model_to_dict


def context_user_data(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)

        user_role = user.user_roles.all()

        print("Processador de contexto funcionando..",
              user, "Função:", user_role, user.type)
        return {
            "user": user,
            "user_roles": user_role,
        }
    else:
        return {}
