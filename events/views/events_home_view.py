from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from events.utils.events_by_month_named import events_by_month_named


class EventsHomeView(PermissionRequiredMixin, TemplateView):
    permission_required = []
    template_name = "events/home.html"
    extra_context = {"events": events_by_month_named()}
