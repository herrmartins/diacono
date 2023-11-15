from django.views.generic import TemplateView
from users.models import CustomUser


class UsersQualifyingListView(TemplateView):
    template_name = 'secretarial/users_qualifying.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = CustomUser.objects.all()
        return context
