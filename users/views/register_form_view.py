from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from users.models import CustomUser
from users.forms import RegisterUserForm


class RegisterFormView(CreateView):
    model = CustomUser
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('core:home')
