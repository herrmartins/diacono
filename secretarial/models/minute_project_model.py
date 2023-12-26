from django.db import models
from core.models import BaseModel
from users.models import CustomUser
from django.dispatch import receiver
from secretarial.models import MeetingAgendaModel
from secretarial.utils.make_basic_minute_text import make_minute
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from .make_basic_minute_text import make_minute


class MinuteProjectModel(BaseModel):
    president = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="meet_president"
    )
    secretary = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="meet_secretary"
    )
    treasurer = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="meet_treasurer"
    )
    meeting_date = models.DateField()
    number_of_attendees = models.CharField(max_length=3)
    previous_minute_reading = models.BooleanField(default=True)
    minute_reading_acceptance_proposal = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="mr_acceptor", null=True
    )
    minute_reading_acceptance_proposal_support = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="mr_supporter", null=True
    )
    previous_finance_report_reading = models.BooleanField(default=True)
    finance_report_acceptance_proposal = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="fr_acceptor", null=True
    )
    finance_report_acceptance_proposal_support = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name="fr_supporter", null=True
    )

    last_months_balance = models.DecimalField(decimal_places=2, max_digits=8)
    revenue = models.DecimalField(decimal_places=2, max_digits=8)
    expenses = models.DecimalField(decimal_places=2, max_digits=8)
    meeting_agenda = models.ManyToManyField(MeetingAgendaModel)
    body = RichTextField(blank=True, null=True)

    class Meta:
        verbose_name = "Projeto de Ata"
        verbose_name_plural = "Projeto de Ata"

    def __str__(self):
        return "Ata do dia " + str(self.meeting_date)


@receiver(pre_save, sender=MinuteProjectModel)
def create_basic_minute_text(sender, instance, **kwargs):
    data_dict = {
        "church": "Igreja Batista Regular de Cidade Satélite",
        "president": f"{instance.president.first_name} {instance.president.last_name}",
        "secretary": f"{instance.secretary.first_name} {instance.secretary.last_name}",
        "treasurer": f"{instance.treasurer.first_name} {instance.treasurer.last_name}",
        "meeting_date": str(instance.meeting_date),
        "number_of_attendees": instance.number_of_attendees,
        "previous_minute_reading": instance.previous_minute_reading,
        "minute_reading_acceptance_proposal": f"{instance.minute_reading_acceptance_proposal.first_name} {instance.minute_reading_acceptance_proposal.last_name}",
        "minute_reading_acceptance_proposal_support": f"{instance.minute_reading_acceptance_proposal_support.first_name} {instance.minute_reading_acceptance_proposal_support.last_name}",
        "previous_finance_report_reading": instance.previous_finance_report_reading,
        "finance_report_acceptance_proposal": f"{instance.finance_report_acceptance_proposal.first_name} {instance.finance_report_acceptance_proposal.last_name}",
        "finance_report_acceptance_proposal_support": f"{instance.finance_report_acceptance_proposal_support.first_name} {instance.finance_report_acceptance_proposal_support.last_name}",
        "last_months_balance": instance.last_months_balance,
        "revenue": instance.revenue,
        "expenses": instance.expenses,
    }

    instance.body = make_minute(data_dict)
