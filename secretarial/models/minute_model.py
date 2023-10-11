from core.models import BaseModel
from django.db import models
from users.models import CustomUser
from ckeditor.fields import RichTextField
from secretarial.models import MeetingAgendaModel
from django.urls import reverse


class MeetingMinuteModel(BaseModel):
    presidente = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name="president")
    secretary = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name="secretary")
    meeting_date = models.DateField()
    body = RichTextField(blank=True, null=True)
    agenda = models.ManyToManyField(
        MeetingAgendaModel, blank=True)

    class Meta:
        verbose_name = "Ata"
        verbose_name_plural = "Atas"

    def get_absolute_url(self):
        return reverse("core:minute-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return "Reunião do dia" + self.meeting_date
