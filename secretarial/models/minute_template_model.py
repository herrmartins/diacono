from core.models import BaseModel
from django.db import models
from ckeditor.fields import RichTextField
from secretarial.models import MeetingAgendaModel


class MinuteTemplateModel(BaseModel):
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True, null=True)
    agenda = models.ManyToManyField(
        MeetingAgendaModel, blank=True)

    class Meta:
        verbose_name = "Modelo de Ata"
        verbose_name_plural = "Modelos de Ata"

    def __str__(self):
        return self.title
