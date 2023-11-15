from django.views.generic import ListView
from secretarial.models import MeetingMinuteModel


class MinutesListView(ListView):
    model = MeetingMinuteModel
    template_name = 'secretarial/list_minutes.html'
    context_object_name = 'minutes'
