from core.models import BaseModel
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime


class MonthlyBalance(BaseModel):
    month = models.DateField(unique=True)
    is_first_month = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Saldo Mensal"
        verbose_name_plural = "Saldos Mensais"

    def __str__(self):
        return f"{self.month} - {self.balance} - {self.is_first_month}"


@receiver(post_save, sender=MonthlyBalance)
def create_missing_monthly_balances(sender, instance, created, **kwargs):
    if created:
        current_date = timezone.now()
        instance_month_aware = timezone.make_aware(
            datetime.combine(instance.month, datetime.min.time()),
            timezone.get_current_timezone(),
        )

        diff = relativedelta(current_date, instance_month_aware)

        for i in range(1, diff.years * 12 + diff.months + 1):
            month = (instance_month_aware.month + i) % 12
            year = (
                instance_month_aware.year + (instance_month_aware.month + i - 1) // 12
            )
            new_month = timezone.datetime(
                year, month, 1, tzinfo=instance_month_aware.tzinfo
            )

            is_first = i == 1

            if not MonthlyBalance.objects.filter(month=new_month).exists():
                MonthlyBalance.objects.create(
                    month=new_month,
                    is_first_month=False,
                    balance=instance.balance,
                )
