import unittest
from decimal import Decimal
from datetime import datetime
from collections import defaultdict
import calendar
from django.utils import timezone
from treasury.models import TransactionModel, CategoryModel
from treasury.utils import (
    get_aggregate_transactions_by_category,
    get_total_transactions_amount,
    get_last_day_of_month,
)
from users.models import CustomUser
from model_mommy import mommy
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist


class TestTransactionFunctions(unittest.TestCase):
    def setUp(self):
        user = mommy.make("users.CustomUser")
        now = timezone.now().date()
        category1 = CategoryModel.objects.create(name="Category 1")
        category2 = CategoryModel.objects.create(name="Category 2")
        category3 = CategoryModel.objects.create(name="Category 3")

        self.transaction1 = TransactionModel.objects.create(
            user=user,
            category=category1,
            amount=Decimal("50.00"),
            is_positive=True,
            date=now,
            description="Test Transaction 1",
        )
        self.transaction2 = TransactionModel.objects.create(
            user=user,
            category=category2,
            amount=Decimal("100.00"),
            is_positive=True,
            date=now,
            description="Test Transaction 2",
        )
        self.transaction3 = TransactionModel.objects.create(
            user=user,
            category=category3,
            amount=Decimal("75.00"),
            is_positive=True,
            date=now,
            description="Test Transaction 3",
        )

        TransactionModel.objects.create(
            user=user,
            category=category1,
            amount=Decimal("-50.00"),
            is_positive=False,
            date=now,
            description="Test Transaction - Category 1",
        )
        TransactionModel.objects.create(
            user=user,
            category=category3,
            amount=Decimal("-25.00"),
            is_positive=False,
            date=now,
            description="Test Transaction - Category 3",
        )

    def test_aggregate_transactions_by_category(self):
        now = timezone.now().date()
        then = datetime(2022, 1, 1).date()

        aggregated_dict = get_aggregate_transactions_by_category(now.year, now.month)
        expected_keys = ["Category 1", "Category 2", "Category 3"]
        expected_result = {
            "Category 1": "50.00",
            "Category 2": "100.00",
            "Category 3": "750.00",
        }

        self.assertCountEqual(aggregated_dict.keys(), expected_keys)

        for value in aggregated_dict.values():
            self.assertIsInstance(Decimal(value), Decimal)

        aggregated_dict_empty = get_aggregate_transactions_by_category(
            then.year, then.month
        )
        self.assertEqual(aggregated_dict_empty, {})

        aggregated_dict_negative = get_aggregate_transactions_by_category(
            now.year, now.month, is_positive=False
        )
        expected_result_negative = {
            "Category 1": "-50.00",
            "Category 3": "-25.00",
        }

        self.assertEqual(aggregated_dict_negative, expected_result_negative)

        aggregated_dict_edge_case = get_aggregate_transactions_by_category(
            now.year, now.month, is_positive=False
        )
        self.assertEqual(aggregated_dict_edge_case, expected_result_negative)

        # Test 7: Performance Test - For a large dataset
        # Add test logic for performance

    def test_total_transactions_amount(self):
        # Test cases for get_total_transactions_amount function
        transactions_dict = {
            "Category 1": "75.00",
            "Category 2": "50.00",
            "Sem categoria": "100.00",
        }

        # Test 1: Basic test with transactions dictionary
        total_amount = get_total_transactions_amount(transactions_dict)
        self.assertEqual(total_amount, "225.00")

        # Test 2: Empty Dictionary
        total_amount_empty = get_total_transactions_amount({})
        self.assertEqual(total_amount_empty, "0.00")

        # Test 3: Negative Values - Test with negative transaction values
        transactions_dict_negative = {"Category 1": "-25.00", "Category 2": "-50.00"}
        total_amount_negative = get_total_transactions_amount(
            transactions_dict_negative
        )
        self.assertEqual(total_amount_negative, "-75.00")

        # Test 4: Edge Cases - Large values, zero, singular values
        transactions_dict_large = {"Category 1": "1000.00", "Category 2": "0.00"}
        total_amount_large = get_total_transactions_amount(transactions_dict_large)
        self.assertEqual(total_amount_large, "1000.00")

    def test_last_day_of_month(self):
        # Test cases for get_last_day_of_month function
        # Test 1: Basic test for a specific month and year
        last_day_1 = get_last_day_of_month(2023, 12)
        self.assertEqual(last_day_1, "31/12/2023")

        # Test 2: Edge Cases - February (leap year, non-leap year), December, January
        last_day_feb_leap = get_last_day_of_month(2024, 2)
        last_day_feb_non_leap = get_last_day_of_month(2023, 2)
        last_day_dec = get_last_day_of_month(2023, 12)
        last_day_jan = get_last_day_of_month(2023, 1)
        self.assertEqual(last_day_feb_leap, "29/02/2024")
        self.assertEqual(last_day_feb_non_leap, "28/02/2023")
        self.assertEqual(last_day_dec, "31/12/2023")
        self.assertEqual(last_day_jan, "31/01/2023")

        # Test 3: Incorrect Inputs - Invalid month or year
        with self.assertRaises(ValueError):
            get_last_day_of_month(2023, 13)
        with self.assertRaises(ValueError):
            get_last_day_of_month(2023, 0)

        # Test 4: Performance Test - For a range of month and year inputs
        # Add test logic for performance


if __name__ == "__main__":
    unittest.main()
