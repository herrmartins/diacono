from django.test import TestCase
from django.utils import timezone
from treasury.models import TransactionModel, TransactionEditHistory
from users.models import CustomUser


class TransactionModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test_user", password="password"
        )

    def test_create_transaction(self):
        user = self.user  # Replace with an existing user ID
        category = None  # Replace with an existing category or create one
        date = timezone.now().date()
        amount = 100.0
        description = "Test Transaction"

        transaction = TransactionModel.objects.create(
            user_id=user.pk,
            category=category,
            date=date,
            amount=amount,
            description=description,
        )
        self.assertIsNotNone(transaction)

    def test_edit_transaction(self):
        # Create a transaction
        transaction = TransactionModel.objects.create(
            user_id=1,  # Replace with an existing user ID
            category=None,  # Replace with an existing category or create one
            date=timezone.now().date(),
            amount=100,
            description="Original Description",
        )

        # Edit the transaction
        transaction.amount = 150
        transaction.description = "Updated Description"
        transaction.save()

        edited_history = TransactionEditHistory.objects.filter(transaction=transaction)
        self.assertEqual(edited_history.count(), 1)

        # Retrieve the transaction again
        updated_transaction = TransactionModel.objects.get(pk=transaction.pk)

        # Check the updated values
        self.assertEqual(updated_transaction.amount, 150)
        self.assertEqual(updated_transaction.description, "Updated Description")
