from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from core.models import BaseModel
from treasury.models import CategoryModel


class TransactionModel(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_positive = models.BooleanField(default=True)
    date = models.DateField()

    edit_history = models.ManyToManyField("treasury.TransactionEditHistory", blank=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return f"{self.date} - {self.description} - R$ {self.amount}"


@receiver(post_save, sender=TransactionModel)
def track_transaction_edit(sender, instance, **kwargs):
    if not instance._state.adding:
        from treasury.models import TransactionEditHistory

        original_transaction = TransactionModel.objects.get(pk=instance.pk)

        if (
            original_transaction.description != instance.description
            or original_transaction.amount != instance.amount
            or original_transaction.date != instance.date
        ):
            TransactionEditHistory.objects.create(
                user=instance.user,
                transaction=instance,
                original_description=original_transaction.description,
                original_amount=original_transaction.amount,
                original_date=original_transaction.date,
                edited_description=instance.description,
                edited_amount=instance.amount,
                edited_date=instance.date,
            )


@receiver(post_save, sender=TransactionModel)
def update_monthly_balance(sender, instance, created, **kwargs):
    if created:
        month = instance.date.replace(day=1)
        amount = instance.amount

        from treasury.models import MonthlyBalance

        monthly_balance, created = MonthlyBalance.objects.get_or_create(
            month=month, defaults={"balance": amount}
        )

    if not created:
        monthly_balance.balance += amount
        monthly_balance.save()


@receiver(pre_save, sender=TransactionModel)
def check_is_positive(sender, instance, **kwargs):
    if instance.amount < 0:
        instance.is_positive = False
    else:
        instance.is_positive = True


@receiver(post_delete, sender=TransactionModel)
def update_monthly_balance_on_delete(sender, instance, **kwargs):
    month = instance.date.replace(day=1)
    amount = instance.amount

    from treasury.models import MonthlyBalance

    try:
        monthly_balance = MonthlyBalance.objects.get(month=month)
        monthly_balance.balance -= amount
        monthly_balance.save()
    except MonthlyBalance.DoesNotExist:
        print("Erro")
