from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model as User
from .forms import TodosForm
from .models import Todos, Tag
from datetime import datetime, timedelta
from django.contrib import messages
from function import change_value, create_tag, check_time
from django.http import JsonResponse
from django.core import serializers
import json
from accounts.decorator import login_message_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from studies.models import StudyTodos
from dateutil.relativedelta import relativedelta

# Create your views here.
@login_message_required
def today(request):

    today = str(datetime.now())[:10]

    # 로그인 유저의 today todos 찾기
    today_todos = Todos.objects.filter(user_id=request.user, when=today).order_by(
        "started_at"
    )

    # timetable 넘겨주기 위해 & 태그 보여주기 위해
    time_list = []
    tag_list = []

    for todo in today_todos:
        if todo.started_at != "" and todo.expired_at != "":
            start = change_value(todo.started_at)
            end = change_value(todo.expired_at)
            time = end - start

            time_list.append([])
            time_list[-1].append(start)
            time_list[-1].append(time)

        # 업데이트 화면 태크 보여주기
        today_tag = Todos.objects.get(pk=todo.pk).tagged.all()
        if today_tag:
            tag_json = serializers.serialize("json", today_tag)
            tag_list.append(tag_json)
        else:
            tag_list.append("")

    # 비동기 보여주기 (업데이트)
    if request.method == "POST":
        res_json = serializers.serialize(
            "json",
            Todos.objects.filter(user_id=request.user, when=today).order_by(
                "started_at"
            ),
        )
        return JsonResponse({"resJson": res_json, "resJson2": tag_list})

    # 오늘 해야 하는 스터디 todos
    today_study_todos = StudyTodos.objects.filter(
        user_id=request.user, start__lte=today, end__gte=today
    )

    # 달성율
    if len(today_todos) != 0:
        achievement_rate = round(
            100 * (today_todos.filter(is_completed=True).count() / len(today_todos))
        )
    else:
        achievement_rate = 0

    todosForm = TodosForm()

    context = {
        "time_list": time_list,
        "today_todos": today_todos,
        "todosForm": todosForm,
        "achievement_rate": achievement_rate,
        "today_study_todos": today_study_todos,
    }
    return render(request, "todos/complete/today_main.html", context)


@login_message_required
def create(request):
    if request.method == "POST":
        start, end, tags = (
            request.POST.get("started_at"),
            request.POST.get("expired_at"),
            request.POST.get("tags"),
        )
        todoForm = TodosForm(request.POST)

        # timetable 체크 및 중복되면 저장 x
        user = request.user
        today = str(datetime.now())[:10]
        today_todos = Todos.objects.filter(user_id=request.user, when=today)

        # 시간 입력이 잘못되었을때
        if check_time(request, today_todos, start, end, messages) == False:
            return redirect("todos:today")

        if todoForm.is_valid():
            todo = todoForm.save(commit=False)
            todo.user_id, todo.when, todo.started_at, todo.expired_at = (
                user,
                today,
                start,
                end,
            )
            todo.save()

            # tag create
            create_tag(tags, Tag, todo)

        return redirect("todos:today")
    else:
        messages.warning(request, "잘못된 접근입니다.")
        return redirect("todos:today")


@login_message_required
def delete(request, todos_pk):
    today = str(datetime.now())[:10]

    if request.method == "POST":
        todo = Todos.objects.get(pk=todos_pk)
        todo.delete()
        res_json = serializers.serialize(
            "json",
            Todos.objects.filter(user_id=request.user, when=today).order_by(
                "started_at"
            ),
        )
        return JsonResponse({"resJson": res_json})
    res_json = serializers.serialize(
        "json",
        Todos.objects.filter(user_id=request.user, when=today).order_by("started_at"),
    )
    return JsonResponse({"resJson": res_json})


@login_message_required
def update(request, pk):
    todo = get_object_or_404(Todos, pk=pk)
    today = str(datetime.now())[:10]

    if request.method == "POST":
        todoForm = TodosForm(request.POST, instance=todo)
        start, end, tags = (
            request.POST.get("started_at"),
            request.POST.get("expired_at"),
            request.POST.get("tags"),
        )

        user = request.user

        # 시간은 수정 기능 막아둬서 주석 처리함

        # 시간 입력이 잘못되었을때
        # if check_time(request, today_todos, start, end, messages) == False:
        #     return redirect("todos:today")

        if todoForm.is_valid():
            todo = todoForm.save(commit=False)
            todo.user_id, todo.when, todo.started_at, todo.expired_at = (
                user,
                today,
                start,
                end,
            )
            todo.save()

            # 태그 업데이트 => 삭제 후 다시 생성
            todo_tags = Tag.objects.filter(todo=pk)
            for todo_tag in todo_tags:
                todo_tag.delete()
            create_tag(tags, Tag, todo)

        # 해당 투두에 태그가 있을 때 json으로 보냄
        todo_tags = Tag.objects.filter(todo=pk)
        if todo_tags:
            tag_json = serializers.serialize("json", todo_tags.order_by("id"))
        else:
            tag_json = ""

        context = {
            "todoTitle": todo.title,
            "todoCont": todo.content,
            "tagJson": tag_json,
        }
        return JsonResponse(context)

    else:
        todoForm = TodosForm(instance=todo)
        context = {
            "todoForm": todoForm,
        }
        return JsonResponse(context)


@login_required
def week(request):
    # 오늘 날짜 기준 정렬
    few_week = 0
    today = datetime.today().weekday() + 1
    now = datetime.now()
    week = now + timedelta(weeks=few_week, days=-(today % 7))

    time_list = []
    for i in range(7):
        temp = week + timedelta(days=i)
        temp_time = temp.strftime("%Y-%m-%d")
        time_list.append(Todos.objects.filter(when=temp_time, user_id=request.user))
    todos = TodosForm()
    context = {
        "todos": todos,
        "time_list": time_list,
    }
    return render(request, "todos/complete/week_todos.html", context)


@login_required
def week_asyn(request, few_week):
    few_week = int(few_week)
    today = datetime.today().weekday() + 1
    now = datetime.now()
    week = now + timedelta(weeks=few_week, days=-(today % 7))

    time_list = []
    res = []
    for i in range(7):
        temp = week + timedelta(days=i)
        temp_time = temp.strftime("%Y-%m-%d")
        time_list.append(Todos.objects.filter(when=temp_time, user_id=request.user))
        # 비동기
        res_json = serializers.serialize(
            "json", Todos.objects.filter(when=temp_time, user_id=request.user)
        )
        res.append(res_json)

    # todos = TodosForm()
    if request.method == "GET":
        return JsonResponse({"resJson": res})


@login_required
def read_all(request):
    # 값 보내기 위한 알고리즘(past, present, future)
    # 현재 생각하는 문제
    # 페이지 네이션을 쓰는지
    # 스터디 todos는 어떻게 처리 할 것인지 or 4주씩 하는 것인지
    # 한달 단위로 한다고 했는데 그러면 미래도 한달단위인지?
    now = datetime.now()
    today = str(now)[:10]
    yesterday = str(now - timedelta(1))[:10]
    # print(str(yesterday)[:10])
    # 과거
    # months=1을 통하여 월별 관리, 모든 과거: lte
    few_month_ago = str(now - relativedelta(months=1))[:10]
    past_data = Todos.objects.filter(
        user_id=request.user, when__range=(few_month_ago, yesterday)
    ).order_by("-when")

    # 각 데이터에서 when 필드를 문자열로 추출해서 중복을 제거함
    # 각 날짜를 키를 하는 딕셔너리를 생성
    past_date = set(map(lambda x: x.when.strftime("%Y-%m-%d"), past_data))
    past = dict.fromkeys(past_date)

    # 각 데이터의 날짜를 문자열로 만들고
    # 해당 날짜를 키로써 접근한 것이 None 이면 빈 리스트 생성
    # 생성 후 해당 리스트에 날짜에 맞는 데이터가 쌓임
    for i in past_data:
        date = i.when.strftime("%Y-%m-%d")

        if not past[date]:
            past[date] = []

        temp = past[date]
        temp.append(i)

    # 현재
    present = Todos.objects.filter(user_id=request.user, when=today)
    # 미래
    tomorrow = str(now + timedelta(days=1))[:10]
    future = Todos.objects.filter(user_id=request.user, when__gte=tomorrow).order_by(
        "when"
    )

    context = {
        "past": past,
        "present": present,
        "future": future,
    }
    return render(request, "todos/complete/all_todos.html", context)


@login_required
def stuty_list(request):
    today = str(datetime.now())[:10]
    # 로그인 유저의 today todos 찾기
    today_todos = Todos.objects.filter(user_id=request.user, when=today).order_by(
        "started_at"
    )
    # timetable 넘겨주기 위해
    time_list = []
    for todo in today_todos:
        if todo.started_at is not None and todo.expired_at is not None:
            start = change_value(todo.started_at)
            end = change_value(todo.expired_at)
            time = end - start

            time_list.append(start)
            time_list.append(time)

    todosForm = TodosForm()

    context = {
        "time_list": time_list,
        "today_todos": today_todos,
        "todosForm": todosForm,
    }
    return render(request, "todos/test/study_list.html", context)


# checkbox 비동기
@require_POST
def is_completed(request):
    if request.method == "POST":
        # JSON 데이터 받음
        data = json.loads(request.body)

        # 변경된 값이랑 어떤 todo 인지 특정할 수 있는 id 값
        is_completed = data.get("is_completed")
        todoId = data.get("todoId")

        # 해당 id 값으로 todo 객체를 가져옴
        obj = Todos.objects.get(id=todoId)

        # 받아온 값으로 변경
        obj.is_completed = is_completed
        obj.save()

        # 변경된 값으로 응답
        context = {"is_completed": is_completed}

        return JsonResponse(context)


@login_required
def detail_asyn(request):
    pk = request.GET.get("todoIdValue")

    todo = Todos.objects.filter(id=pk)

    context = {"todo": serializers.serialize("json", todo)}

    return JsonResponse(context)
