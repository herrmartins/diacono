from django.contrib import admin
from secretarial.models import (
    MeetingAgendaModel,
    MeetingMinuteModel,
    MinuteTemplateModel)

admin.site.register(MeetingAgendaModel)
admin.site.register(MeetingMinuteModel)
admin.site.register(MinuteTemplateModel)
