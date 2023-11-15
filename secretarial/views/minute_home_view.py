from django.views.generic import TemplateView
from secretarial.forms import MinuteProjectModelForm
from secretarial.models import (MeetingMinuteModel,
                                MinuteProjectModel,
                                MinuteExcerptsModel,
                                MinuteTemplateModel)


class MinuteHomeView(TemplateView):
    template_name = 'secretarial/minute_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MinuteProjectModelForm()
        context["meeting_minutes"] = MeetingMinuteModel.objects.all().reverse()[
            :10]
        context["number_of_projects"] = MinuteProjectModel.objects.count()
        context["number_of_excerpts"] = MinuteExcerptsModel.objects.count()
        context["number_of_minutes"] = MeetingMinuteModel.objects.count()
        context["number_of_templates"] = MinuteTemplateModel.objects.count()

        return context
