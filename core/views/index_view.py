from django.views.generic import TemplateView
from users.models import UsersFunctions
from users.forms import LoginForm


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Não está sendo utilizado
            context["user_role"] = UsersFunctions.objects.get(
                member_id=self.request.user.id
            ).function
        else:
            context["login_form"] = LoginForm
        return context
