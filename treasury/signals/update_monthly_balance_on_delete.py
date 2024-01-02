from django.db.models.signals import pre_delete
from django.dispatch import receiver
from treasury.models import TransactionModel, MonthlyBalance
from django.db import models
from django.db.models import Sum
from dateutil.relativedelta import relativedelta


@receiver(pre_delete, sender=TransactionModel)
def update_monthly_balance_on_delete(sender, instance, **kwargs):
    month = instance.date.replace(day=1)
    amount = instance.amount

    from treasury.models import MonthlyBalance
    from django.db.models import F, Sum

    try:
        monthly_balance = MonthlyBalance.objects.get(month=month)
        monthly_balance.balance -= amount
        monthly_balance.save()
    except MonthlyBalance.DoesNotExist:
        pass

    # Update subsequent months' balances
    subsequent_months = MonthlyBalance.objects.filter(month__gt=month)
    for sub_month in subsequent_months:
        previous_sub_month = sub_month.month - relativedelta(months=1)
        try:
            previous_month_balance = MonthlyBalance.objects.get(
                month=previous_sub_month
            )
            prev_balance = previous_month_balance.balance
        except MonthlyBalance.DoesNotExist:
            prev_balance = 0

        sub_month_transactions = TransactionModel.objects.filter(
            date__year=sub_month.month.year,
            date__month=sub_month.month.month,
        )

        sub_month_total_amount = (
            sub_month_transactions.aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        prev_balance += sub_month_total_amount
        sub_month.balance = prev_balance
        sub_month.save()
