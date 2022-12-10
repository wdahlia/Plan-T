from django.shortcuts import render, redirect, get_object_or_404
from .models import Study, StudyTodos, StudyTodosManagement
from .forms import StudyForm, StudyTodosForm
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from accounts.decorator import login_message_required
from django.db.models import Q

# Create your views here.
# 스터디 목록
@login_required
def index(request):
    category = request.GET.get("tabmenu")

    # 입력 받은 카테고리 값에 따라서 조건을 건다.
    if category is None or category == "on" or category == "None":
        category_studies = Study.objects.all()
    else:
        category_studies = Study.objects.filter(category=category)
    # 검색을 한다면
    search = request.GET.get("search")
    if search is not None:
        studies = Study.objects.all()
        search_lists = studies.filter(
            Q(title__icontains=search) | Q(desc__icontains=search)
        )
        category_studies = category_studies & search_lists

    context = {"category_studies": category_studies, "category": category}

    return render(request, "studies/complete/study_index.html", context)


# 스터디 생성
@login_message_required
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

    return render(request, "studies/complete/create_study.html", context)


@login_message_required
def update(request, study_pk):
    study_ = get_object_or_404(Study, pk=study_pk)

    if request.method == "POST":
        studyform = StudyForm(request.POST, instance=study_)

        if studyform.is_valid():
            form = studyform.save(commit=False)
            # 시간저장(선택)
            start, end = (
                request.POST.get("start_at"),
                request.POST.get("end_at"),
            )
            form.start_at = start
            form.end_at = end
            form.save()
            return redirect("studies:detail", study_pk)
    else:
        studyform = StudyForm(instance=study_)
    # 날짜는 str로 바꾸어 줘야 value에서 받을 수 있다.
    study_start = str(study_.start_at)
    study_end = str(study_.end_at)

    context = {
        "studyform": studyform,
        "study": study_,
        "study_start": study_start,
        "study_end": study_end,
    }

    return render(request, "studies/complete/study_update.html", context)


# Study todo 생성
@login_message_required
def create_todos(request, study_pk):
    if request.method == "POST":
        study = Study.objects.get(pk=study_pk)
        study_todos_management = StudyTodosManagement.objects.create()

        # 가입된 멤버
        joined_member = []
        for user in study.participated.all():
            for studyy in user.join_study.all():
                if studyy.pk == study_pk:
                    joined_member.append(user)
                    break
        #
        # 가입된 멤버 각각 생성
        for userr in joined_member:
            todoForm = StudyTodosForm(request.POST)
            if todoForm.is_valid() and study.owner == request.user:
                todo = todoForm.save(commit=False)
                todo.study_pk = study
                todo.user_id = userr
                todo.management_pk = study_todos_management
                todo.save()
        else:
            return redirect("studies:detail", study_pk)
        #

    messages.error(request, "저장 실패.")  # 이거 왜 작동안하지?
    return redirect("studies:detail", study_pk)


def delete_todos(request, study_pk, management_pk):
    management = get_object_or_404(StudyTodosManagement, pk=management_pk)
    study_ = get_object_or_404(Study, pk=study_pk)
    if request.user == study_.owner:
        if request.method == "POST":
            management.delete()
    return redirect("studies:detail", study_pk)


@login_required
def detail(request, study_pk):
    study_ = get_object_or_404(Study, pk=study_pk)
    a = StudyTodosManagement.objects.all()
    for i in a:
        print(i)
    # 로그인 유저, 시작은 오늘 이하, 끝은 오늘 이상의 study todos
    today = str(datetime.now())[:10]
    study_todos = StudyTodos.objects.filter(
        user_id=request.user,
        start__lte=today,
        end__gte=today,
        study_pk=study_pk,
    )
    #
    # 가입된 멤버
    joined_member = []
    # 가입 신청 멤버
    application_member = []
    for user in study_.participated.all():
        for study in user.join_study.all():
            if study.pk == study_pk:
                joined_member.append(user)
                break
        else:
            application_member.append(user)
    #
    for i in study_todos:
        print(i)
    context = {
        "study": study_,
        "study_todo_form": StudyTodosForm(),
        "joined_member": joined_member,
        "application_member": application_member,
        "study_todos": study_todos,
    }

    return render(request, "studies/complete/study_detail.html", context)


# study.participated.all
@login_required
def info(request, study_pk):
    study = get_object_or_404(Study, pk=study_pk)

    start = str(study.start_at)
    end = str(study.end_at)
    context = {
        "study": study,
        "study_todo_form": StudyTodosForm(),
        "start": start,
        "end": end,
    }

    return render(request, "studies/complete/study_info.html", context)


@login_required
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
    return redirect("studies:info", study_pk)


@login_required
def refusal(request, study_pk, user_pk):
    study = get_object_or_404(Study, pk=study_pk)
    user = get_object_or_404(get_user_model(), pk=user_pk)
    # 거절
    study.participated.remove(user)

    return redirect("studies:detail", study_pk)


@login_required
def accept(request, user_pk, study_pk):
    print(user_pk, study_pk)
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

    # 가입된 멤버 수
    member_number = 0
    for user in study.participated.all():
        for study in user.join_study.all():
            if study.pk == study_pk:
                member_number += 1
                break

    study.member_number = member_number
    study.save()

    context = {
        "is_accepted": is_accepted,
        "studyCount": user.join_study.count(),
    }
    print(user_pk, study_pk)

    return redirect("studies:detail", study_pk)  # 나중에 detail로
