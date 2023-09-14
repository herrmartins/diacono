from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser


class RegisterUserForm(UserCreationForm):
    # exemplo de um campo comum, mas o username não dá, nem o password
    """username = forms.CharField(widget=forms.TextInput(
    attrs={"class": "form-control"}))"""

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2")
        labels = {
            "username": "",
            "password1": "",
            "password2": "",
        }

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
