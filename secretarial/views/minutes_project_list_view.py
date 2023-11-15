from django.views.generic import ListView
from secretarial.models import MinuteProjectModel


class MinutesProjectListView(ListView):
    model = MinuteProjectModel
    template_name = 'secretarial/list_minutes_projects.html'
    context_object_name = 'minutes'
