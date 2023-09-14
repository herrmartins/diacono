from django.views.generic import TemplateView
from users.models import CustomUser, UsersFunctions


class SecretarialHomeView(TemplateView):
    template_name = 'secretarial/home.html'
