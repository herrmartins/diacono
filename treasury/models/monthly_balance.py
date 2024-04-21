from core.models import BaseModel
from django.db import models
from django.db.models import ProtectedError
from django.utils import timezone
from django.core.exceptions import ValidationError


class MonthlyBalance(BaseModel):
    month = models.DateField(unique=True)
    is_first_month = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Saldo Mensal"
        verbose_name_plural = "Saldos Mensais"

    def __str__(self):
        return f"{self.month} - {self.balance} - {self.is_first_month}"

    def save(self, *args, **kwargs):
        current_month = timezone.now().date().replace(day=1)
        is_testing = kwargs.pop('is_testing', False)

        if not is_testing:
            if self.month is None:
                raise ValidationError("The month field cannot be None.")
            if self.month > current_month:
                raise ValidationError("Cannot add balances with a future month...")

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False, is_testing=False):
        if not is_testing:
            raise ProtectedError(
                "Deletion of MonthlyBalance instances is not allowed.", self)

        super().delete(using=using, keep_parents=keep_parents)

