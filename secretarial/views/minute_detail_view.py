from django.views.generic import DetailView
from secretarial.models import MeetingMinuteModel


class MinuteDetailView(DetailView):
    model = MeetingMinuteModel
    template_name = 'secretarial/minute_detail.html'
    context_object_name = 'minute'
