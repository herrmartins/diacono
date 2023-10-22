from django.db.models.aggregates import Star
from django.views.generic import TemplateView
from users.models import Congregated, StaffMember, RegularMember


class SecretarialHomeView(TemplateView):
    template_name = "secretarial/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        number_of_members = StaffMember.objects.count() + RegularMember.objects.count()
        number_of_visitors = Congregated.objects.count()
        print("Membros:", number_of_members, "Visitantes:", number_of_visitors)
        context["number_of_members"] = number_of_members
        context["number_of_visitors"] = number_of_visitors

        return context
