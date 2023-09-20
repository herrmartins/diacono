from django.db import models
from core.models import BaseModel


class MeetingAgendaModel(BaseModel):
    agenda_theme = models.CharField(max_length=100)

    def __str__(self):
        return self.agenda_theme
