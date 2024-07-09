from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms

from .models import Thread, Comment


class ThreadForm(forms.ModelForm):
    """Form tạo mới Thread"""

    class Meta:
        model = Thread
        fields = ["forum", "prefix", "title"]
        # tên để hiển thị trên giao diện
        labels = {
            "forum": "Diễn đàn",
            "prefix": "Loại thread",
            "title": "Tiêu đề",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Tạo Thread"))


class CommentForm(forms.ModelForm):
    """Form tạo mới Comment"""

    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content": "Bình luận",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Đăng"))
