from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.shortcuts import get_object_or_404

from .models import Comment, Forum, Thread, ThreadPrefix


class ThreadForm(forms.ModelForm):
    """Form tạo mới Thread"""

    class Meta:
        model = Thread
        fields = ["forum", "prefix", "title"]
        # tên để hiển thị trên giao diện
        labels = {"forum": "Diễn đàn", "prefix": "Loại thread", "title": "Tiêu đề"}

    def __init__(self, forum_slug=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_initial_forum(forum_slug)
        self.set_initial_prefix()

        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Tạo Thread"))

    def set_initial_forum(self, forum_slug):
        if forum_slug:
            forum = get_object_or_404(Forum, slug=forum_slug)
            self.fields["forum"].initial = forum

    def set_initial_prefix(self):
        default_prefix = get_object_or_404(ThreadPrefix, name="No Prefix")
        self.fields["prefix"].initial = default_prefix


class CommentForm(forms.ModelForm):
    """Form tạo mới Comment"""

    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": "Bình luận"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Đăng"))
