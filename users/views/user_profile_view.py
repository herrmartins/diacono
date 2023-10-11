from django.views.generic.detail import DetailView
from users.models import CustomUser, UsersFunctions
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_profile.html"
    context_object_name = "user_object"
