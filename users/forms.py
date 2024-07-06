from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from users.models import Profile


class UserRegisterForm(UserCreationForm):
    """Form được dùng để render trong trang đăng ký"""

    display_name = forms.CharField(label="Tên hiển thị", max_length=255)

    date_of_birth = forms.DateField(
        label="Ngày sinh",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )

    class Meta:
        model = get_user_model()
        #
        # Ảnh hưởng đến thứ tự xuất hiện trong form
        #
        fields = [
            # Model field
            "username",
            # Profile field
            "display_name",
            # UserCreationForm field
            "password1",
            "password2",
            # Profile field
            "date_of_birth",
        ]
        labels = {
            "username": "Tên người dùng",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Trường không phải của model sẽ xử lý ở đây
        self.fields["password1"].label = "Mật khẩu"
        self.fields["password2"].label = "Xác nhận mật khẩu"

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Đăng ký"))


# Create a UserUpdateForm to update
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["email"]
        labels = {
            "email": "Email",
        }


# Create a ProfileUpdateForm to update
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "date_of_birth", "bio", "avatar"]
        labels = {
            "display_name": "Tên người dùng",
            "date_of_birth": "Ngày sinh",
        }
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
