from django.views.generic import TemplateView
from events.utils.events_by_month_named import events_by_month_named


class EventsHomeView(TemplateView):
    template_name = "events/home.html"
    extra_context = {"events": events_by_month_named()}
