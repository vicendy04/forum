from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from users.models import Profile


class UserRegisterForm(UserCreationForm):
    """Form được dùng để render trong trang đăng ký"""

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            # Auth field
            "password1",
            "password2",
        )
        labels = {
            "username": "Tên người dùng",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # These are not fields of the model, in this case get_user_model()
        # So need to custom here
        self.fields["password1"].label = "Mật khẩu"
        self.fields["password2"].label = "Xác nhận mật khẩu"

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Đăng ký"))


# Create a UserUpdateForm to update
class UserUpdateForm(forms.ModelForm):
    pass


# Create a ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "date_of_birth", "bio", "avatar"]
