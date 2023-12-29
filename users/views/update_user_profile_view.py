from django.views.generic.edit import UpdateView
from users.models import CustomUser
from users.forms import UpdateUserProfileModelForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class UserProfileUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "users.change_customuser"
    model = CustomUser
    form_class = UpdateUserProfileModelForm
    template_name = "users/user_profile_update_form.html"

    def get_permission_required(self):
        if self.get_object() == self.request.user:
            return []
        return super().get_permission_required()
