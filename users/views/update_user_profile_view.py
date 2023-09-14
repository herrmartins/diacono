from django.views.generic.edit import UpdateView
from users.models import CustomUser
from users.forms import UpdateUserProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UpdateUserProfileModelForm
    template_name = "users/user_profile_update_form.html"
