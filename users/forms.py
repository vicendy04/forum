from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

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
        fields = ["username", "display_name", "password1", "password2", "date_of_birth"]
        labels = {"username": "Tên người dùng"}
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "hx-get": reverse_lazy("users:check_username"),
                    "hx-trigger": "keyup changed delay:2s",
                    "hx-swap": "innerHTML",
                    "hx-target": "#div_id_username",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Trường không phải của model sẽ xử lý ở đây
        self.fields["password1"].label = "Mật khẩu"
        self.fields["password2"].label = "Xác nhận mật khẩu"

        self.helper = FormHelper(self)
        self.helper.form_id = "register-form"
        self.helper.form_method = "POST"
        self.helper.attrs = {
            "hx-post": reverse_lazy("users:register"),
            "hx-trigger": "submit",
            "hx-swap": "outerHTML",
            "hx-target": "this",
        }
        self.helper.add_input(Submit("submit", "Đăng ký"))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 5:
            raise forms.ValidationError("Tên đăng nhập quá ngắn.")
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập đã được sử dụng.")
        return username


# Create a UserUpdateForm to update
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["email"]
        labels = {"email": "Email"}

    # def clean_email(self):
    #     data = self.cleaned_data["email"]
    #     qs = get_user_model().objects.exclude(id=self.instance.id).filter(email=data)
    #     if qs.exists():
    #         raise forms.ValidationError("Email đã được sử dụng.")
    #     return data


# Create a ProfileUpdateForm to update
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "date_of_birth", "bio", "avatar"]
        labels = {"display_name": "Tên người dùng", "date_of_birth": "Ngày sinh"}
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"})}
