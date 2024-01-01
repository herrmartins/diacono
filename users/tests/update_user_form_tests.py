from django.test import TestCase
from users.forms import UpdateUserProfileModelForm


class UpdateUserProfileFormTest(TestCase):
    def test_update_user_profile_blank_data(self):
        # Test with blank form data
        form = UpdateUserProfileModelForm(data={})
        self.assertTrue(form.is_valid())

    def test_update_user_profile_wrong_date_format(self):
        form = UpdateUserProfileModelForm(data={"date_of_birth": "07-06-1986"})
        self.assertFalse(form.is_valid())
