from django.shortcuts import render, redirect, get_object_or_404
from .models import Study, StudyTodos, StudyTodosManagement
from .forms import StudyForm, StudyTodosForm
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from accounts.decorator import login_message_required
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
# 스터디 목록
@login_required
def index(request):
    category = request.GET.get("tabmenu")

    # 카테고리
    if category is None or category == "on" or category == "None":
        category_studies = Study.objects.all().order_by("-pk")
    else:
        category_studies = Study.objects.filter(category=category).order_by("-pk")

    # 검색
    search = request.GET.get("search")
    if search is not None and search != "None":
        studies = Study.objects.all()
        search_lists = studies.filter(
            Q(title__icontains=search) | Q(desc__icontains=search)
        )
        category_studies = category_studies & search_lists
    # 페이지 네이션 코드
    page_number = request.GET.get("page")
    paginator = Paginator(category_studies, 8)
    page_list = paginator.get_page(page_number)

    context = {
        "category_studies": category_studies,
        "page_list": page_list,
        "category": category,
        "search": search,
    }

    return render(request, "studies/complete/study_index.html", context)


# 스터디 생성
@login_message_required
def create(request):
    if request.method == "POST":
        studyform = StudyForm(request.POST)
        # 시간저장(선택)
        start, end = (
            request.POST.get("start_at"),
            request.POST.get("end_at"),
        )

        if start <= end:
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

                form.owner = request.user
                form.save()

                form.participated.add(request.user)
                request.user.join_study.add(form)
            return redirect("studies:index")
        # 종료시점이 시작시점보다 먼저 있을 때
        else:
            messages.warning(request, "시작시점과 종료시점을 바르게 입력하세요")
            return render(request, "studies/complete/create_study.html", context)

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
        start, end = request.POST.get("start"), request.POST.get("end")
        if start == "" and end != "":
            messages.error(request, "시작시점을 입력하세요.")
            return redirect("studies:detail", study_pk)
        elif start != "" and end == "":
            messages.error(request, "종료시점을 입력하세요.")
            return redirect("studies:detail", study_pk)
        elif start == "" and end == "":
            messages.error(request, "시작시점과 종료시점을 입력하세요.")
            return redirect("studies:detail", study_pk)
        else:
            pass
        # 가입된 멤버
        joined_member = []
        for user in study.participated.all():
            for studyy in user.join_study.all():
                if studyy.pk == study_pk:
                    joined_member.append(user)
                    break

        if start <= end:
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
        else:
            messages.error(request, "올바른 기간을 입력해주세요.")
            return redirect("studies:detail", study_pk)

    messages.error(request, "저장 실패")
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
    # 인증
    if request.user in study_.participated.all():
        if study_ in request.user.join_study.all():
            # 로그인 유저, 시작은 오늘 이하, 끝은 오늘 이상의 study todos
            today = str(datetime.now())[:10]
            study_todos = StudyTodos.objects.filter(
                user_id=request.user,
                start__lte=today,
                end__gte=today,
                study_pk=study_,
            )
            #
            # 가입된 멤버
            joined_member = []
            # 수락은 안된 가입 신청 멤버
            application_member = []
            for user in study_.participated.all():
                for study in user.join_study.all():
                    if study.pk == study_pk:
                        joined_member.append(user)
                        break
                else:
                    application_member.append(user)
            #

            context = {
                "study": study_,
                "study_todo_form": StudyTodosForm(),
                "joined_member": joined_member,
                "application_member": application_member,
                "study_todos": study_todos,
            }

            return render(request, "studies/complete/study_detail.html", context)
    return redirect("studies:index")


@login_required
def delete(request, study_pk):
    if request.method == "POST":
        study_ = get_object_or_404(Study, pk=study_pk)
        study_.delete()
        return redirect("studies:index")
    # 잘못된 방식으로 보내면
    return redirect("studies:detail", study_pk)


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
    # 신청 취소
    if study.participated.filter(pk=request.user.pk).exists():
        study.participated.remove(request.user)
        is_participated = False
    # 가입신청
    else:
        study.participated.add(request.user)
        is_participated = True
    context = {
        "is_participated": is_participated,
    }
    return JsonResponse(context)


# 반장이 가입신청 인원 수락 거절(가입 신청기록 삭제)
@login_required
def refusal(request, study_pk, user_pk):
    if request.method:
        study = get_object_or_404(Study, pk=study_pk)
        user = get_object_or_404(get_user_model(), pk=user_pk)
        # 거절
        study.participated.remove(user)
        studyJoinNumber = len(study.participated.all()) - 1
        context = {"studyJoinNumber": studyJoinNumber}
        return JsonResponse(context)
    else:
        messages.error(request, "잘못된 요청입니다.")
        return redirect("studies:detail", study_pk)


@login_required
def accept_and_drive_out(request, user_pk, study_pk):
    if request.method == "POST":
        user = get_object_or_404(get_user_model(), pk=user_pk)
        study = get_object_or_404(Study, pk=study_pk)

        # 강퇴 & 탈퇴(수락 거절 + 가입 신청 거절)
        if user.join_study.filter(pk=study_pk).exists():
            user.join_study.remove(study)
            study.participated.remove(user)
            # 스터디 관련 todos 삭제
            delete_studies_todos = StudyTodos.objects.filter(
                user_id=user,
                study_pk=study,
            )
            for delete_studies_todo in delete_studies_todos:
                delete_studies_todo.delete()
            #
            # 반장이 하면 강퇴(화면 유지), 멤버가 하면 탈퇴(index페이지로 이동)
            if study.owner == request.user:
                owner__ = True
            else:
                owner__ = False
            #
        # 수락 or 초대
        else:
            if study.max_people > study.member_number:
                user.join_study.add(study)
                today = str(datetime.now())[:10]
                # 수락과 동시에 아직 안끝난 studies_todos 생성
                study_todos = StudyTodos.objects.filter(
                    user_id=study.owner,
                    study_pk=study,
                    end__gte=today,
                )
                for study_todo in study_todos:
                    StudyTodos.objects.create(
                        study_pk=study,
                        management_pk=study_todo.management_pk,
                        user_id=user,
                        title=study_todo.title,
                        content=study_todo.content,
                        start=study_todo.start,
                        end=study_todo.end,
                    )
                #
                owner__ = True
            else:
                messages.error(request, "최대 인원을 초과하였습니다.")
                return redirect("studies:detail", study_pk)

        # 가입된 멤버 수 최신화
        member_number = 0
        studyJoinNumber = 0
        member = []
        for user_application in study.participated.all():
            for study_joined in user_application.join_study.all():
                if study_joined.pk == study_pk:
                    member_number += 1
                    member.append(user_application)
                    break
            else:
                studyJoinNumber += 1
            #
        # # test
        # print(member)
        # print(len(member))
        # print(member_number)
        study.member_number = member_number
        study.save()
        if owner__ == True:
            context = {
                "member_number": member_number,
                "studyJoinNumber": studyJoinNumber,
            }
            return JsonResponse(context)
        else:
            return redirect("studies:index")
    else:
        messages.error(request, "잘못된 요청입니다.")
        return redirect("studies:detail", study_pk)
