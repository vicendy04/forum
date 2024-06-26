from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UserRegisterForm(UserCreationForm):
    """Form được dùng để render trong trang đăng ký"""

    # Bug chỗ này khi chưa custom User model
    display_name = forms.CharField(
        max_length=32, required=True, label="Your display name"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Đăng ký"))

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "display_name",
            "password1",
            "password2",
        )
