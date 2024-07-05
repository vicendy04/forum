from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


# Create your views here.


class UserRegisterView(CreateView):
    """Controller xử lý đăng ký"""

    model = get_user_model()
    form_class = UserRegisterForm
    template_name = "users/register.html"

    def form_valid(self, form):
        new_user = form.save()

        # Create the user profile
        Profile.objects.create(
            user=new_user,
            display_name=form.cleaned_data.get("display_name"),
            date_of_birth=form.cleaned_data.get("date_of_birth"),
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("main:forum_list")


def view_or_update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(instance=request.user, data=request.POST)
        profile_form = ProfileUpdateForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Cập nhật profile thành công")
        else:
            messages.error(request, "Lỗi không thể cập nhật profile")

        # fix khi reload page không gửi lại post
        return redirect("users:profile")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, "users/profile.html", context)
