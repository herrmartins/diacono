from django.views.generic import CreateView
from secretarial.models import MinuteExcerptsModel
from django.urls import reverse


class ExcerptCreateView(CreateView):
    model = MinuteExcerptsModel
    template_name = 'secretarial/excerpt_created.html'
    fields = ['title', 'excerpt']
