from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from users.models import CustomUser
from users.models import UsersFunctions


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "users/user_profile.html"
    context_object_name = "user"
    success_url = reverse_lazy("user-profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_role = UsersFunctions.objects.get(member_id=self.request.user.id)
        print("Função do usuário:", user_role)
        context["user_role"] = user_role
        return context
