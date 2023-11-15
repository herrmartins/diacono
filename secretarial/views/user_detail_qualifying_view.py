from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from secretarial.forms import UpdateUserRoleModelForm


class UserDetailQualifyingView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "secretarial/user_detail_qualify.html"
    form_class = UpdateUserRoleModelForm
    context_object_name = "user_object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(pk=self.kwargs['pk'])
        context["user_roles"] = user.functions.all()
        context["user_status"] = user.type

        return context
