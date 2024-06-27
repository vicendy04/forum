from django import forms
from .models import Thread, Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ThreadForm(forms.ModelForm):
    """Form tạo mới Thread"""

    class Meta:
        model = Thread
        fields = ["category", "title"]
        labels = {
            "category": "Category",
            "title": "Title",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Tạo Thread"))


class PostForm(forms.ModelForm):
    """Form tạo mới Post"""

    class Meta:
        model = Post
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Đăng"))
