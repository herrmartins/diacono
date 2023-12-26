from django.views.generic.edit import UpdateView
from users.models import CustomUser
from users.forms import UpdateUserProfileModelForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class UserProfileUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'users.change_users'
    model = CustomUser
    form_class = UpdateUserProfileModelForm
    template_name = "users/user_profile_update_form.html"
