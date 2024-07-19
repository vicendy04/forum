from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


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
        # Ảnh hưởng đến thứ tự xuất hiện trong form
        fields = ["username", "display_name", "password1", "password2", "date_of_birth"]
        labels = {"username": "Tên người dùng"}
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "hx-get": reverse_lazy("users:check_username"),
                    "hx-trigger": "keyup changed delay:1s",
                    "hx-swap": "innerHTML",
                    "hx-target": "#div_id_username",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # remove help_text
        for field in self.fields.values():
            field.help_text = ""

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


# Create a ProfileUserUpdateForm to update
class ProfileUserUpdateForm(forms.Form):
    # Profile fields
    display_name = forms.CharField(label="Tên người dùng", max_length=32)
    # User fields
    email = forms.EmailField(label="Email", required=False)
    # Profile fields
    bio = forms.CharField(label="Bio", widget=forms.Textarea, required=False)
    date_of_birth = forms.DateField(
        label="Ngày sinh",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    avatar = forms.ImageField(label="Avatar", required=False)

    def __init__(self, user, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.profile = profile
        self.set_initial_fields()

    def save(self):
        # Update user model
        self.user.email = self.cleaned_data["email"]
        self.user.save()

        # Update profile model
        self.profile.display_name = self.cleaned_data["display_name"]
        self.profile.date_of_birth = self.cleaned_data["date_of_birth"]
        self.profile.bio = self.cleaned_data["bio"]
        avatar = self.cleaned_data["avatar"]
        if avatar:
            self.profile.avatar = avatar
        self.profile.save()

    def set_initial_fields(self):
        """Đặt giá trị sẵn cho profile"""

        self.fields["email"].initial = self.user.email
        self.fields["display_name"].initial = self.profile.display_name
        self.fields["date_of_birth"].initial = self.profile.date_of_birth
        self.fields["bio"].initial = self.profile.bio
