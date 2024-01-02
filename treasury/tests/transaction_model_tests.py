from django.test import TestCase
from django.utils import timezone
from treasury.models import TransactionModel, TransactionEditHistory, MonthlyBalance
from users.models import CustomUser
from model_mommy import mommy
import unittest
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from datetime import date, timedelta
from random import randint
from django.db import models
import random


class TransactionModelTests(TestCase):
    def setUp(self):
        self.current_month = timezone.now().date().replace(day=1)
        self.two_months_ago = self.current_month - relativedelta(months=2)
        self.a_year_ago = self.current_month - relativedelta(months=12)

        self.user = CustomUser.objects.create_user(
            username="test_user", password="password"
        )

    def test_create_transaction(self):
        mommy.make(MonthlyBalance, month=self.two_months_ago, balance=100)
        MonthlyBalance.objects.get(month=self.current_month).delete()
        queried_monthly_balance = None
        try:
            queried_monthly_balance = MonthlyBalance.objects.get(
                month=self.current_month
            )
        except MonthlyBalance.DoesNotExist:
            pass
        self.assertIsNone(
            queried_monthly_balance,
            "MonthlyBalance for two months ago should not exist",
        )

        # Working almost properly, but understand the code.
        mommy.make(TransactionModel, date=self.current_month)

        try:
            queried_monthly_balance = MonthlyBalance.objects.get(
                month=self.current_month
            )
        except MonthlyBalance.DoesNotExist:
            pass

        self.assertIsNotNone(
            queried_monthly_balance, "MonthlyBalance for this month ago should exist"
        )

    def test_create_transactions_no_monthly_balance(self):
        mommy.make(MonthlyBalance, month=self.two_months_ago, balance=100)
        MonthlyBalance.objects.get(month=self.current_month).delete()
        transaction = mommy.make(TransactionModel, date=self.current_month)
        queried_monthly_balance = None

        try:
            queried_monthly_balance = MonthlyBalance.objects.get(
                month=self.current_month
            )
        except MonthlyBalance.DoesNotExist:
            pass

        self.assertIsNotNone(
            queried_monthly_balance, "MonthlyBalance for this month ago should exist"
        )

        expected_balance_c_month = Decimal(100) + Decimal(transaction.amount)
        self.assertEqual(expected_balance_c_month, queried_monthly_balance.balance)

    def test_edit_transaction(self):
        # Create an initial transaction with an amount of 100
        transaction = TransactionModel.objects.create(
            user_id=1,
            category=None,
            date=self.current_month,
            amount=100,
            description="Original Description",
        )

        # Confirm the initial MonthlyBalance
        queried_monthly_balance = MonthlyBalance.objects.get(month=self.current_month)
        self.assertEqual(queried_monthly_balance.balance, Decimal(100))

        # Create another transaction with an amount of 50
        additional_transaction = TransactionModel.objects.create(
            user_id=1,
            category=None,
            date=self.current_month,
            amount=50,
            description="Additional Transaction",
        )

        # Confirm the updated MonthlyBalance after the additional transaction
        queried_monthly_balance = MonthlyBalance.objects.get(month=self.current_month)
        self.assertEqual(queried_monthly_balance.balance, Decimal(150))

        # Edit the initial transaction's amount to 150
        transaction.amount = 150
        transaction.description = "Updated Description"
        transaction.save()

        # Confirm the updated MonthlyBalance after the edited transaction
        queried_monthly_balance = MonthlyBalance.objects.get(month=self.current_month)
        self.assertEqual(queried_monthly_balance.balance, Decimal(200))

        additional_transaction.amount = 100
        additional_transaction.save()

        queried_monthly_balance = MonthlyBalance.objects.get(month=self.current_month)
        self.assertEqual(queried_monthly_balance.balance, Decimal(250))

        # Check TransactionEditHistory and updated transaction values
        edited_history = TransactionEditHistory.objects.filter(transaction=transaction)
        self.assertEqual(edited_history.count(), 1)

        updated_transaction = TransactionModel.objects.get(pk=transaction.pk)
        self.assertEqual(updated_transaction.amount, 150)
        self.assertEqual(updated_transaction.description, "Updated Description")

        negative_transaction = mommy.make(
            TransactionModel, amount=-5, date=self.current_month
        )
        queried_monthly_balance = MonthlyBalance.objects.get(month=self.current_month)
        self.assertEqual(queried_monthly_balance.balance, Decimal(245))

        negative_transaction.amount = 5
        negative_transaction.save()
        queried_monthly_balance = MonthlyBalance.objects.get(month=self.current_month)
        self.assertEqual(queried_monthly_balance.balance, Decimal(255))

    def test_delete_transaction(self):
        mommy.make(MonthlyBalance, month=self.a_year_ago, balance=100)
        transactions = []
        n = 0
        for i in range(4):
            transaction_date = self.a_year_ago + timedelta(
                days=i * 3 * 30
            )  # Every three months

            transactions.append(
                mommy.make(TransactionModel, date=transaction_date, amount=10)
            )
            n += 1

        this_month_expected_balance = Decimal(n * 10 + 100)

        this_month_balance = MonthlyBalance.objects.get(
            month=self.current_month
        ).balance

        self.assertEqual(this_month_expected_balance, this_month_balance)

        while TransactionModel.objects.exists():
            # Delete the first transaction
            TransactionModel.objects.first().delete()
            n = TransactionModel.objects.count()
            this_month_expected_balance = Decimal(n * 10 + 100)

            this_month_balance = MonthlyBalance.objects.get(
                month=self.current_month
            ).balance

            self.assertEqual(this_month_expected_balance, this_month_balance)

    def test_with_transactions_in_different_months(self):
        current_date = date.today()

        mommy.make(
            MonthlyBalance, month=self.a_year_ago, balance=100, is_first_month=True
        )

        # Generate a list of expected months between a_year_ago and current_date
        expected_months = [
            self.a_year_ago.replace(day=1) + relativedelta(months=i)
            for i in range(
                (current_date.year - self.a_year_ago.year) * 12
                + current_date.month
                - self.a_year_ago.month
                + 1
            )
        ]

        # Create transactions for a few different months with varying positive and negative amounts
        for i in range(7):
            random_date = expected_months[i]
            amount = randint(-100, 100)
            if not MonthlyBalance.objects.get(month=random_date).is_first_month:
                mommy.make(TransactionModel, date=random_date, amount=amount)

        # Fetch all MonthlyBalance instances within the date range
        all_monthly_balances = MonthlyBalance.objects.filter(
            month__range=(self.a_year_ago, current_date)
        ).order_by("month")

        # Asserting that all monthly balances were created
        self.assertEqual(all_monthly_balances.count(), len(expected_months))

        previous_balance = 100  # Set the initial previous balance for the first month

        for balance in all_monthly_balances:
            transactions = TransactionModel.objects.filter(
                date__year=balance.month.year, date__month=balance.month.month
            )

            total_amount = transactions.aggregate(total_amount=models.Sum("amount"))[
                "total_amount"
            ]
            if balance.is_first_month:
                self.assertEqual(balance.balance, previous_balance)
            else:
                if total_amount is not None:
                    expected_balance = previous_balance + total_amount
                    self.assertEqual(balance.balance, expected_balance)
                else:
                    self.assertEqual(balance.balance, previous_balance)

            previous_balance = balance.balance

        all_transactions = []
        for expected_month in expected_months:
            transactions = TransactionModel.objects.filter(
                date__year=expected_month.year, date__month=expected_month.month
            )
            all_transactions.extend(list(transactions))

        transactions_to_update = random.sample(all_transactions, 3)

        for transaction in transactions_to_update:
            new_amount = random.randint(-100, 100)
            transaction.amount = new_amount
            transaction.save()

        # Fetch all MonthlyBalance instances again after updating transactions
        updated_monthly_balances = MonthlyBalance.objects.filter(
            month__range=(self.a_year_ago, current_date)
        ).order_by("month")

        # Check subsequent months' balances after updating transactions
        previous_balance = 100  # Reset the initial previous balance for the first month

        for balance in updated_monthly_balances:
            if not balance.is_first_month:
                transactions = TransactionModel.objects.filter(
                    date__year=balance.month.year, date__month=balance.month.month
                )
                total_amount = transactions.aggregate(
                    total_amount=models.Sum("amount")
                )["total_amount"]

                if total_amount is not None:
                    expected_balance = previous_balance + total_amount
                    self.assertEqual(balance.balance, expected_balance)
                else:
                    self.assertEqual(balance.balance, previous_balance)
                previous_balance = balance.balance

    def test_transactions_deletion_affects_monthly_balances(self):
        current_date = date.today()

        mommy.make(
            MonthlyBalance, month=self.a_year_ago, balance=100, is_first_month=True
        )

        # Generate a list of expected months between a_year_ago and current_date
        expected_months = [
            self.a_year_ago.replace(day=1) + relativedelta(months=i)
            for i in range(
                (current_date.year - self.a_year_ago.year) * 12
                + current_date.month
                - self.a_year_ago.month
                + 1
            )
        ]

        # Create transactions for a few different months with varying positive and negative amounts
        for i in range(7):
            random_date = expected_months[i]
            amount = randint(-100, 100)
            if not MonthlyBalance.objects.get(month=random_date).is_first_month:
                mommy.make(TransactionModel, date=random_date, amount=amount)

        # Fetch all MonthlyBalance instances within the date range
        all_monthly_balances = MonthlyBalance.objects.filter(
            month__range=(self.a_year_ago, current_date)
        ).order_by("month")

        # Asserting that all monthly balances were created
        self.assertEqual(all_monthly_balances.count(), len(expected_months))

        previous_balance = 100  # Set the initial previous balance for the first month

        for balance in all_monthly_balances:
            transactions = TransactionModel.objects.filter(
                date__year=balance.month.year, date__month=balance.month.month
            )

            total_amount = transactions.aggregate(total_amount=models.Sum("amount"))[
                "total_amount"
            ]
            if balance.is_first_month:
                self.assertEqual(balance.balance, previous_balance)
            else:
                if total_amount is not None:
                    expected_balance = previous_balance + total_amount
                    self.assertEqual(balance.balance, expected_balance)
                else:
                    self.assertEqual(balance.balance, previous_balance)

            previous_balance = balance.balance

        initial_monthly_balances = MonthlyBalance.objects.all()

        print("BALANÇOS PÓS TRANSAÇÕES:", initial_monthly_balances)

        # Simulate deleting transactions
        transactions_to_delete = random.sample(list(TransactionModel.objects.all()), 3)

        for transaction in transactions_to_delete:
            transaction.delete()

        # Fetch all MonthlyBalance instances after deletion
        updated_monthly_balances = MonthlyBalance.objects.filter(
            month__range=(self.a_year_ago, current_date)
        ).order_by("month")

        # Check if the balances have been updated after deleting transactions
        for initial_balance, updated_balance in zip(
            initial_monthly_balances, updated_monthly_balances
        ):
            if initial_balance.is_first_month:
                self.assertEqual(initial_balance.balance, updated_balance.balance)
            else:
                initial_total_amount = TransactionModel.objects.filter(
                    date__year=initial_balance.month.year,
                    date__month=initial_balance.month.month,
                ).aggregate(total_amount=models.Sum("amount"))["total_amount"]

                updated_total_amount = TransactionModel.objects.filter(
                    date__year=updated_balance.month.year,
                    date__month=updated_balance.month.month,
                ).aggregate(total_amount=models.Sum("amount"))["total_amount"]

                if (
                    initial_total_amount is not None
                    and updated_total_amount is not None
                ):
                    expected_balance = (
                        initial_balance.balance
                        + initial_total_amount
                        - updated_total_amount
                    )
                    self.assertEqual(updated_balance.balance, expected_balance)
                else:
                    self.assertEqual(updated_balance.balance, initial_balance.balance)


if __name__ == "__main__":
    unittest.main()
