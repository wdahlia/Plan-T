from django.shortcuts import render, redirect, get_object_or_404
from .models import Study
from .forms import StudyForm, StudyTodoForm
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.
# 스터디 목록
def index(request):
    category = request.GET.get("tabmenu")

    # 입력 받은 카테고리 값에 따라서 조건을 건다.
    if category is None or category == "on":
        category_studies = Study.objects.all()
    else:
        category_studies = Study.objects.filter(category=category)

    context = {"category_studies": category_studies}

    return render(request, "studies/working/study_index.html", context)


# 스터디 생성
def create(request):
    if request.method == "POST":
        studyform = StudyForm(request.POST)
        if studyform.is_valid():
            form = studyform.save(commit=False)
            # 시간저장(선택)
            start, end = (
                request.POST.get("start_at"),
                request.POST.get("end_at"),
            )
            if start != "":
                form.start_at = start
            if end != "":
                form.end_at = end
            #
            form.owner = request.user
            form.save()

            form.participated.add(request.user)
            request.user.join_study.add(form)

            return redirect("studies:index")
    else:
        studyform = StudyForm()

    context = {"studyform": studyform}

    return render(request, "studies/working/create_study.html", context)


# Study todo 생성
def create_todos(request, study_pk):
    if request.method == "POST":
        # URL 로 받은 pk 를 가지고 특정 study 를 가져옴
        # 날짜도 통신으로 받아온다.
        study = Study.objects.get(pk=study_pk)
        todoForm = StudyTodoForm(request.POST)
        if todoForm.is_valid() and study.owner == request.user:
            todo = todoForm.save(commit=False)
            # 스터디원 모두를 위해 생성
            users = study.participated
            for user in users:
                todo.user_id = user
                todo.save()

        return redirect("studies:index")  # redirect 위치 임시


def detail(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = request.user
    check = False
    if study in user.join_study.all():
        check = True

    context = {"study": study, "check": check, "study_todo_form": StudyTodoForm()}

    return render(request, "studies/test/detail.html", context)


def join(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)
    # 탈퇴
    if study.participated.filter(pk=request.user.pk).exists():
        study.participated.remove(request.user)
        is_participated = False
    # 가입신청 or 초대 수락
    else:
        study.participated.add(request.user)
        is_participated = True
    context = {
        "is_participated": is_participated,
        "studyCount": study.participated.count(),
    }
    return redirect("studies:detail", study_pk)


def accept(request, user_pk, study_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    study = get_object_or_404(Study, pk=study_pk)

    # 강퇴
    if user.join_study.filter(pk=study_pk).exists():
        user.join_study.remove(study)
        is_accepted = False
    # 수락 or 초대
    else:
        if study.max_people >= len(study.participated.all()):
            user.join_study.add(study)
            is_accepted = True
        else:
            messages.error(request, "최대 인원을 초과하였습니다.")
            return redirect("studies:detail", study_pk)
    context = {
        "is_accepted": is_accepted,
        "studyCount": user.join_study.count(),
    }
    return redirect("studies:detail", study_pk)
