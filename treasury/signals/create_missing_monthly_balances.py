from django.db.models.signals import post_save
from django.dispatch import receiver
from treasury.models import MonthlyBalance
from dateutil.relativedelta import relativedelta
from django.utils import timezone



@receiver(post_save, sender=MonthlyBalance)
def create_missing_monthly_balances(sender, instance, created, **kwargs):
    if created:
        previous_month = instance.month - relativedelta(months=1)
        # Get the month the user saved
        instance_month = instance.month
        # Get the current date
        current_date = timezone.now().date()  # Extract date only
        n_while = 0
        while instance_month.year < current_date.year or (
            instance_month.year == current_date.year
            and instance_month.month <= current_date.month
        ):
            if not MonthlyBalance.objects.filter(month=instance_month).exists():
                is_first = instance_month == instance.month
                MonthlyBalance.objects.create(
                    month=instance_month,
                    is_first_month=is_first,
                    balance=instance.balance,
                )
            next_month = instance_month + relativedelta(months=1)
            instance_month = next_month.replace(day=1)