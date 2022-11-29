from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    login as auth_login, 
    logout as auth_logout,
    update_session_auth_hash
)
from django.views.decorators.http import require_POST

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


# 데코레이터 추가 필요
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)

    # 바꿔야 함!
    return redirect("accounts:test")


# 데코레이터 추가 필요
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()

    # 바꿔야 함!
    return redirect("accounts:test")


# 데코레이터 추가 필요
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            # 비밀번호가 변경되면 기존 세션과 회원 인증 정보가
            # 일치하지 않게 되기 때문에 새로운 password hash 로
            # 세션을 업데이트 해주는 메소드이다.
            update_session_auth_hash(request, form.user)

            # 바꿔야 함!
            return redirect("accounts:test")

    else:
        form = CustomUserChangeForm(request.user)

    context = {
        "form": form,
    }

    # 바꿔야 함!
    return render(request, "test/form.html", context)