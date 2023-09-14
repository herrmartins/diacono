from django.views.generic.edit import UpdateView
from users.models import CustomUser, UsersFunctions
from users.forms import UpdateUserProfileModelForm
from django.contrib.auth.mixins import LoginRequiredMixin


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UpdateUserProfileModelForm
    template_name = "users/user_profile_update_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = CustomUser.objects.get(id=self.request.user.id)
        # Não está sendo utilizado
        context["user_role"] = UsersFunctions.objects.get(
            member_id=self.request.user.id
            ).function
        return context
