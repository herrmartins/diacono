from core.models import BaseModel
from django.db import models
from users.models import CustomUser
from ckeditor.fields import RichTextField
from secretarial.models import MinuteCategoriesModel, MeetingAgendaModel


class MeetingMinuteModel(BaseModel):
    presidente = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    secretary = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True)
    meeting_date = models.DateField()
    attendees = models.ManyToManyField(CustomUser)
    body = RichTextField(blank=True, null=True)
    agenda = models.ManyToManyField(
        MeetingAgendaModel, blank=True)
    category = models.ManyToManyField(
        MinuteCategoriesModel, blank=True)

    class Meta:
        verbose_name = "Ata"
        verbose_name_plural = "Atas"

    def __str__(self):
        return "Reunião do dia" + self.meeting_date
