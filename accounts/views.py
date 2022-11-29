from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

# Create your views here.
# 임시 함수
def test(request):
    return render(request, "test/main.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            # 바꿔야 함!
            return redirect("accounts:test")

    else:
        form = CustomUserCreationForm()

    context = {
        "form": form,
    }

    # 바꿔야 함!
    return render(request, "test/form.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())

            # 바꿔야 함!
            return redirect("accounts:test")

    else:
        form = AuthenticationForm(request)

    context = {
        "form": form,
    }

    # 바꿔야 함!
    return render(request, "test/form.html", context)


def logout(request):
    auth_logout(request)

    # 바꿔야 함!
    return redirect("accounts:test")