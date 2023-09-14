from users.models import CustomUser, UsersFunctions


def context_user_data(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        user_role = UsersFunctions.objects.get(
            member_id=request.user.id)
        print("Processador de contexto funcionando..",
              user, "Função:", user_role)
        return {
            "user": user,
            "user_role": user_role.function,
        }
    else:
        return {}
