from django.views.generic.detail import DetailView
from users.models import CustomUser
from django.contrib.auth.mixins import PermissionRequiredMixin


class UserProfileView(PermissionRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_profile.html"
    context_object_name = "user_object"
    permission_required = 'users.view_users'

    def has_permission(self):
        user = self.request.user
        obj = self.get_object()

        if obj == user:
            return True
        return super().has_permission()
