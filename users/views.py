from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from crispy_forms.utils import render_crispy_form
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django_htmx.http import HttpResponseClientRedirect

from .forms import ProfileUserUpdateForm, UserRegisterForm
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
    user = request.user
    profile = user.profile

    if request.method == "POST":
        form = ProfileUserUpdateForm(
            data=request.POST, files=request.FILES, user=user, profile=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật profile thành công")
        else:
            messages.error(request, "Lỗi không thể cập nhật profile")

        # fix khi reload page không gửi lại post
        return redirect("users:profile")
    else:
        form = ProfileUserUpdateForm(user=user, profile=profile)

    context = {"form": form}
    return render(request, "users/profile.html", context)


def check_username(request):
    form = UserRegisterForm(request.GET)
    return HttpResponse(as_crispy_field(form["username"]))


def user_profile(request, username):
    User = get_user_model()
    user_to = get_object_or_404(
        User.objects.prefetch_related("threads_created", "followers", "following"),
        username=username,
    )
    profile = get_object_or_404(Profile, user=user_to)

    threads = user_to.threads_created.all()
    followers = user_to.followers.all()
    following = user_to.following.all()

    context = {
        "user_from": request.user,
        "user_to": user_to,
        "profile": profile,
        "threads": threads,
        "followers": followers,
        "following": following,
    }
    return render(request, "users/user_profile.html", context)


# @login_required and htmx can't be used together
def follow(request, username):
    """Follow button"""

    if not request.user.is_authenticated:
        login_url = reverse_lazy("users:login")
        user_profile_url = reverse_lazy(
            "users:user_profile", kwargs={"username": username}
        )
        query_string = "?next=" + user_profile_url
        redirect_url = f"{login_url}{query_string}"
        return HttpResponseClientRedirect(redirect_url)

    if request.method == "POST" and request.htmx:
        user_from = request.user
        user_to = get_object_or_404(get_user_model(), username=username)
        this_user_followed = user_from.following.filter(id=user_to.id).exists()

        if this_user_followed:
            user_from.following.remove(user_to)
        else:
            user_from.following.add(user_to)

        followers = user_to.followers.all()

        context = {
            "user_from": user_from,
            "user_to": user_to,
            "followers": followers,
        }
        context.update(csrf(request))

        html_content = render_to_string("users/includes/follow_form.html", context)
        return HttpResponse(content=html_content)
