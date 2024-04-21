from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from unittest.mock import MagicMock, patch
from treasury.models import (TransactionModel, MonthlyBalance, CategoryModel)
from users.models import CustomUser
from io import BytesIO
from django.utils import timezone
from PIL import Image
from django.utils.timezone import now
from model_mommy import mommy
from treasury.tests.test_utils import get_test_image_file
import shutil
from tempfile import mkdtemp
from django.core.files.storage import Storage
import os
from treasury.tests.test_utils import get_test_image_file
from django.utils.timezone import make_aware
import datetime


class FakeStorage(Storage):
    def __init__(self, base_location):
        self.base_location = base_location
        self.files = {}

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        self.files[name] = content
        return name

    def delete(self, name):
        if name in self.files:
            del self.files[name]

    def exists(self, name):
        return name in self.files

    def path(self, name):
        return os.path.join(self.base_location, name)

    def __del__(self):
        shutil.rmtree(self.base_location)


class TransactionModelMethodsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_media_root = mkdtemp()
        cls.storage = FakeStorage(base_location=cls.temp_media_root)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if hasattr(cls, 'storage') and hasattr(cls.storage, 'base_location'):
            shutil.rmtree(cls.storage.base_location, ignore_errors=True)

    def setUp(self):
        super().setUp()
        TransactionModel.acquittance_doc.field.storage = self.storage
        image_io = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_io, 'JPEG')
        image_io.seek(0)

        self.image = SimpleUploadedFile(
            name='test.jpg', content=image_io.getvalue(), content_type='image/jpeg')

        self.user = CustomUser.objects.create(username='testuser')

        self.category = CategoryModel.objects.create(name='Test Category')

        current_month = now().date().replace(day=1)
        MonthlyBalance.objects.create(
            month=current_month, is_first_month=True, balance=1000)

    def test_save_new_transaction(self):
        transaction = mommy.make(TransactionModel, acquittance_doc=self.image)
        self.assertIsNotNone(transaction.pk)

    def create_transaction(self, **kwargs):
        doc = get_test_image_file()
        defaults = {
            "user": self.user,
            "category": self.category,
            "description": "Test Transaction",
            "amount": 100,
            "date": timezone.now().date(),
            "is_positive": True,
            "acquittance_doc": doc,
        }
        defaults.update(kwargs)
        return mommy.make("TransactionModel", **defaults)

    def test_delete_transaction(self):
        transaction = self.create_transaction()
        transaction.delete()
        self.assertFalse(self.storage.exists(transaction.acquittance_doc.name),
                         "File should have been deleted but still exists.")

    def test_save_new_transaction_with_future_date(self):
        future_date = timezone.now().date() + timezone.timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.create_transaction(date=future_date)

    def test_update_transaction_changes_file(self):
        new_image = get_test_image_file()
        transaction = mommy.make(
            'TransactionModel', acquittance_doc=get_test_image_file())
        old_image_path = transaction.acquittance_doc.path

        transaction.acquittance_doc = new_image
        transaction.save()

        # Directly check if the old file still exists using the configured storage
        self.assertFalse(transaction.acquittance_doc.storage.exists(
            old_image_path), "Old file should have been deleted but still exists.")

    def test_update_transaction_no_file_change(self):
        transaction = self.create_transaction()
        with patch.object(transaction.acquittance_doc, 'delete', MagicMock(name="delete")) as mock_delete:
            transaction.description = "Updated description"
            transaction.save()
            self.assertFalse(mock_delete.called)
