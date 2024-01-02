from django.db.models.signals import post_save
from django.dispatch import receiver
from treasury.models import MonthlyBalance, TransactionModel
from dateutil.relativedelta import relativedelta
from django.db.models import F, Sum


@receiver(post_save, sender=TransactionModel)
def update_monthly_balance_on_create(sender, instance, created, **kwargs):
    if created:
        month = instance.date.replace(day=1)
        difference = instance.amount
        try:
            current_monthly_balance = MonthlyBalance.objects.get(month=month)
            current_monthly_balance.balance = F("balance") + difference
            current_monthly_balance.save()
        except MonthlyBalance.DoesNotExist:
            print("NÃO EXISTE...")
            previous_month = month - relativedelta(months=1)
            try:
                previous_month_balance = MonthlyBalance.objects.get(
                    month=previous_month
                )
                previous_balance = previous_month_balance.balance
            except MonthlyBalance.DoesNotExist:
                previous_balance = 0

            MonthlyBalance.objects.create(
                month=month, balance=previous_balance + difference
            )

        subsequent_months = MonthlyBalance.objects.filter(month__gt=month)

        for sub_month in subsequent_months:
            previous_sub_month = sub_month.month - relativedelta(months=1)

            try:
                previous_month_balance = MonthlyBalance.objects.get(
                    month=previous_sub_month
                )
                previous_balance = previous_month_balance.balance
            except MonthlyBalance.DoesNotExist:
                previous_balance = 0

            sub_month_transactions = TransactionModel.objects.filter(
                date__year=sub_month.month.year,
                date__month=sub_month.month.month,
            )

            sub_month_total_amount = (
                sub_month_transactions.aggregate(total_amount=Sum("amount"))[
                    "total_amount"
                ]
                or 0
            )

            new_balance = previous_balance + sub_month_total_amount

            sub_month.balance = new_balance

            sub_month.save()
