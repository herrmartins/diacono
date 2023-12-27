from django.contrib.staticfiles.finders import find
from users.models import CustomUser
import json


def context_user_data(request):
    file_path = find("json/church_info.json")

    church_info = {}
    try:
        with open(file_path, "r") as file:
            church_info = json.load(file)
            # print("INFO da igreja:", church_info)
    except FileNotFoundError:
        print("Erro: File not found")

    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        # print("Processador de contexto funcionando..", user, "Função:", user.type)
        return {
            "user": user,
            "church_info": church_info,
        }
    else:
        return {"church_info": church_info}
