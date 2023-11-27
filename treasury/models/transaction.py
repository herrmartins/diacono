from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from core.models import BaseModel
from treasury.models import CategoryModel
from django.db.models import Sum, F


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
        print("OPERAÇÃO:", amount)

        from treasury.models import MonthlyBalance

        # Get or create the MonthlyBalance for the current month
        monthly_balance, _ = MonthlyBalance.objects.get_or_create(
            month=month,
            defaults={"balance": 0},
        )

        # Calculate the sum of all transaction amounts for the current month
        current_month_total = (
            TransactionModel.objects.filter(
                date__year=instance.date.year, date__month=instance.date.month
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        last_month_balance = (
            MonthlyBalance.objects.filter(month__lt=month).order_by("-month").first()
        )

        if last_month_balance:
            cumulative_balance = last_month_balance.balance + current_month_total
        else:
            cumulative_balance = current_month_total

        # Update the monthly balance with the cumulative balance
        MonthlyBalance.objects.filter(pk=monthly_balance.pk).update(
            balance=cumulative_balance
        )


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
        print("OPERAÇÃO:", amount)
        print("BALANÇO:", monthly_balance)
        monthly_balance.balance -= amount
        print("APÓS SOMA DA OPERAÇÃO,", monthly_balance.balance)
        monthly_balance.save()
    except MonthlyBalance.DoesNotExist:
        print("MonthlyBalance does not exist for this month")
