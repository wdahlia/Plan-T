from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from todos.models import Todos, Tag
from accounts.models import User
import operator
from .decorator import login_message_required

# Create your views here.
# 회원가입
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # 소셜 로그인 때문에 인증 백엔드가 중첩되어 지정을 해줘야함.
            # link : https://ghqls0210.tistory.com/49
            auth_login(
                request, user, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("todos:today")

    else:
        form = CustomUserCreationForm()

    context = {
        "form": form,
    }

    # 바꿔야 함!
    return render(request, "accounts/complete/accounts_form.html", context)


# 로그인
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # 소셜 로그인 때문에 인증 백엔드가 중첩되어 지정을 해줘야함.
            # link : https://ghqls0210.tistory.com/49
            auth_login(
                request,
                form.get_user(),
                backend="django.contrib.auth.backends.ModelBackend",
            )

            return redirect("todos:today")

    else:
        form = AuthenticationForm(request)

    context = {
        "form": form,
    }

    # 바꿔야 함!
    return render(request, "main_index.html", context)


# 로그아웃
@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)

    # 바꿔야 함!
    return redirect("index")


# 회원탈퇴
@login_required
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    # 바꿔야 함!
    return redirect("index")


# 회원정보 수정
@login_message_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.user, request.POST, request.FILES)

        if form.is_valid():
            form.save()
            # 비밀번호가 변경되면 기존 세션과 회원 인증 정보가
            # 일치하지 않게 되기 때문에 새로운 password hash 로
            # 세션을 업데이트 해주는 메소드이다.
            update_session_auth_hash(request, form.user)

            # 바꿔야 함!
            return redirect("accounts:profile")

    else:
        form = CustomUserChangeForm(request.user)

    context = {
        "form": form,
    }

    # 바꿔야 함!
    return render(request, "accounts/working/accounts_update.html", context)


# 프로필
@login_required
def profile(request):
    you = request.user
    user = User.objects.get(pk=you.pk)

    # 지금껏 user 가 쓴 tag 를 몇번 썼는지, 그리고 몇번 썼는지 세어서 context 로 넘겨줌
    todo = Todos.objects.filter(user_id=user)
    tags = Tag.objects.filter(todo__in=todo)

    tag_count = {}
    for t in tags:
        if t.content in tag_count:
            tag_count[t.content] += 1
        else:
            tag_count[t.content] = 1

    sorted_tag = sorted(tag_count.items(), key=operator.itemgetter(1), reverse=True)
    sorted_tag = sorted_tag[:10]

    result = []
    for tt in sorted_tag:
        result.append({"content": tt[0], "count": tt[1]})

    joined_studies = []
    studies = user.join_study.all()
    for study in studies:
        if user in study.participated.all():
            joined_studies.append(study)
    # 전체 나의 투두 달성률
    todo

    context = {
        "user": user,
        "todos": todo,
        "result": result,
        "joined_studies": joined_studies,
    }
    return render(request, "accounts/working/mypage.html", context)


# 특정 태그의 Todo 목록
@login_required
def same_tag(request, tag):
    you = request.user
    user = User.objects.get(pk=you.pk)
    todo = Todos.objects.filter(user_id=user)
    same_tags = Tag.objects.filter(
        content=tag,
        todo__in=todo,
    )

    context = {"same_tags": same_tags, "tag": tag}

    return render(request, "accounts/working/same_tag.html", context)
