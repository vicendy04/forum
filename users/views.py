from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model

from .forms import UserRegisterForm


# Create your views here.


class UserRegisterView(CreateView):
    """Controller xử lý đăng ký"""

    model = get_user_model()
    form_class = UserRegisterForm
    template_name = "registration/register.html"

    def get_success_url(self):
        return reverse_lazy("main:forum_list")
