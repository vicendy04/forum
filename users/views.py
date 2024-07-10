from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django_htmx.http import HttpResponseClientRedirect


from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


# Create your views here.


def register(request):
    if request.method == "GET":
        context = {"form": UserRegisterForm()}
        return render(request, "users/register.html", context)

    # htmx post request
    elif request.method == "POST" and request.htmx:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(
                user=new_user,
                display_name=form.cleaned_data.get("display_name"),
                date_of_birth=form.cleaned_data.get("date_of_birth"),
            )
            login(request, new_user)
            # redirect via htmx
            return HttpResponseClientRedirect(reverse_lazy("main:forum_list"))

        # https://django-crispy-forms.readthedocs.io/en/latest/crispy_tag_forms.html#ajax-validation-recipe
        else:
            context = {}
            context.update(csrf(request))
            form_html = render_crispy_form(form, context=context)
            return HttpResponse(form_html)


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


def check_username(request):
    form = UserRegisterForm(request.GET)
    return HttpResponse(as_crispy_field(form["username"]))
