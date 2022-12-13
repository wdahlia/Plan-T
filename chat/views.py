from django.shortcuts import render, redirect
from studies.models import Study
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def room(request, study_pk):
    user = request.user
    study = Study.objects.get(id=study_pk)

    
    # 로그인 검증 및 스터디원 여부 파악
    if user.is_authenticated:
        if user in study.participated.all() and study in user.join_study.all():
            nickname = user.username
            memberimg = user.image
        else:
            messages.error(request, "스터디에 가입해주세요.")

            return redirect("studies:detail", study_pk)
    else:
        messages.error(request, "로그인을 해주세요.")

        return redirect("studies:detail", study_pk)

    context = {
        "study": study,
        "room_id": study_pk,
        "nickname": nickname,
        "memberimg": memberimg,
    }

    return render(request, "chat/test.html", context)