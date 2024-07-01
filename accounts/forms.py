from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """Form được dùng để render trong trang đăng ký"""

    display_name = forms.CharField(max_length=32, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            # Custom field
            "display_name",
            # Auth field
            "password1",
            "password2",
        )
        labels = {
            "username": "Tên người dùng",
            "display_name": "Tên hiển thị",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # These are not fields of the model, in this case get_user_model()
        # So need to custom here
        self.fields["display_name"].label = "Tên hiển thị"
        self.fields["password1"].label = "Mật khẩu"
        self.fields["password2"].label = "Xác nhận mật khẩu"

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Đăng ký"))
