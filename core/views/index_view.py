from django.views.generic import TemplateView
from users.forms import LoginForm
from users.models import CustomUser


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # For dubugging purposes, I check the user group permissions
        if self.request.user.is_authenticated:
            user = CustomUser.objects.get(pk=self.request.user.pk)
            user_groups = user.groups.all()

            print("Usuário:", self.request.user, "Grupo:", user_groups)
        context["login_form"] = LoginForm
        return context
