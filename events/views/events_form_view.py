from events.forms import EventForm
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import PermissionRequiredMixin
from events.utils.events_by_month_named import events_by_month_named


class EventsFormView(FormView):
    template_name = 'events/form.html'
    form_class = EventForm
    extra_context = {"events": events_by_month_named()}
    success_url = '/events/register/'
