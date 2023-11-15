from django import template
from users.models import CustomUser

register = template.Library()


@register.filter
def get_user_role(pk):
    user = CustomUser.objects.get(pk=pk)
    functions = user.functions.all()
    print("Funções:", functions)
    try:
        return functions
    except CustomUser.DoesNotExist:
        return ""
