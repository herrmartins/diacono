from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin


class EventsHomeView(PermissionRequiredMixin, TemplateView):
    permission_required = []
    template_name = "events/home.html"
