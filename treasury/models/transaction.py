from django.db import models
from core.models import BaseModel
from treasury.models import CategoryModel
from django.utils import timezone
from django.core.exceptions import ValidationError


class TransactionModel(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_positive = models.BooleanField(default=True)
    date = models.DateField()

    edit_history = models.ManyToManyField(
        "treasury.TransactionEditHistory", blank=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.date} - {self.description} - R$ {self.amount}"

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        if self.date > today:
            raise ValidationError("Cannot add transactions with a future date")

        try:
            from treasury.models import MonthlyBalance
            MonthlyBalance.objects.get(is_first_month=True)
        except MonthlyBalance.DoesNotExist:
            raise ValidationError(
                "Cannot add transactions without adding the monthly balances...")

        super().save(*args, **kwargs)
