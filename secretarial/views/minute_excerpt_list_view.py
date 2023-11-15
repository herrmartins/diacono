from django.views.generic import ListView
from secretarial.models import MinuteExcerptsModel


class MinutesExcerptsListView(ListView):
    model = MinuteExcerptsModel
    template_name = 'secretarial/list_excerpts.html'
    context_object_name = 'excerpts'
