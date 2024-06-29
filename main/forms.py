from django import forms
from .models import Thread, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ThreadForm(forms.ModelForm):
    """Form tạo mới Thread"""

    class Meta:
        model = Thread
        fields = ["forum", "title"]
        labels = {
            "forum": "Forum",
            "title": "Title",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Tạo Thread"))


class CommentForm(forms.ModelForm):
    """Form tạo mới Comment"""

    class Meta:
        model = Comment
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Đăng"))
