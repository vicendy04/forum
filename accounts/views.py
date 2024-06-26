from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .forms import UserRegisterForm


# Create your views here.


class UserRegisterView(CreateView):
    """Controller xử lý đăng ký"""

    model = User
    form_class = UserRegisterForm
    template_name = "registration/register.html"

    def get_success_url(self):
        return reverse_lazy("main:category_list")
