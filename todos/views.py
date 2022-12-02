from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model as User
from .forms import TodosForm
from .models import Todos
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib import messages


def change_value(value):
    if value == "":
        index = value
        return index
    else:
        hour, min = map(int, value.split(":"))
        index = ((hour - 6) * 6) + (min // 10)
        return index


# Create your views here.
def today(request):
    today = str(datetime.now())[:10]
    # 로그인 유저의 today todos 찾기
    today_todos = Todos.objects.filter(user_id=request.user, when=today).order_by(
        "started_at"
    )
    # timetable 넘겨주기 위해
    time_list = []
    for todo in today_todos:
        if todo.started_at is not None:
            start = change_value(todo.started_at)
            end = change_value(todo.expired_at)
            time = end - start

            time_list.append(start)
            time_list.append(time)

    # started_at__lte=today, expired_at__gte=today
    # filter 에 추가할 조건
    # started 보다 today가 많고, expired 보다 today가 적다는 조건
    # todo_id=user_todos
    # filter에 추가해야하는데 역참조 조건 달기가 까다로움
    # todo_id는 todo에 달린 user_id 가 request.user의 pk 이다
    # 아니면 todo_id는 user_todos 의 pk와 같다 라고 하면 되는데
    # 구현이 잘 안 됨
    todosForm = TodosForm()
    print(0)
    print(today_todos)
    for i in today_todos:
        print(i)
    context = {
        "time_list": time_list,
        "today_todos": today_todos,
        "todosForm": todosForm,
    }
    return render(request, "todos/complete/today_main.html", context)


def create(request):
    if request.method == "POST":
        start = request.POST.get("started_at")
        end = request.POST.get("expired_at")
        when = request.POST.get("when")
        todoForm = TodosForm(request.POST, request.FILES)

        # timetable 체크 및 중복되면 저장 x
        user = request.user
        today = str(datetime.now())[:10]
        today_todos = Todos.objects.filter(user_id=request.user, when=today)
        exist = set()
        for todo in today_todos:
            if todo.started_at is not None:
                st = change_value(todo.started_at)
                ed = change_value(todo.expired_at)
                for t in range(st, ed + 1):
                    exist.add(t)
        if start or end != "":
            timetable = set(range(change_value(start), change_value(end) + 1))
            if (start < end) and timetable.isdisjoint(exist):
                pass
            else:
                start = ""
                end = ""
                messages.warning(request, "시간이 잘못되었습니다.")

        if todoForm.is_valid():
            todo = todoForm.save(commit=False)
            todo.user_id = user
            when += " 09:00:00"  # 시간 저장할때 9시간을 더해줘야 한국시간으로 잘 저장이 된다.
            todo.when = when
            if start != "":
                todo.started_at = start
            if end != "":
                todo.expired_at = end
            todo.save()
        return redirect("todos:today")  # 추후에 비동기로 반드시 바꾸어 줘야 함.

    else:  # 테스트용
        todoForm = TodosForm()
    context = {
        "todoForm": todoForm,
    }
    return render(request, "todos/complete/today_main.html", context)


def delete(request, todos_pk):
    if request.method == "POST":
        todo = Todos.objects.get(pk=todos_pk)
        todo.delete()
    return redirect("todos:today")  # 추후에 비동기로 바꾸는거 권장


def week(request, few_week):
    # 추후 프론트에서 다음주 지난주 어떻게 보낼줄 지 정해주면 수정하면 됨
    next_ = few_week + 1
    last_ = few_week - 1
    today = datetime.today().weekday() + 1
    now = datetime.now()
    week = now + timedelta(weeks=few_week, days=-(today % 7))
    print("today :", today)
    print("현재 : ", now)
    print("기준 날짜 : ", week)

    time_list = []
    for i in range(7):
        temp = week + timedelta(days=i)
        # RuntimeWarning: 이 나온다.
        temp_time = temp.strftime("%Y-%m-%d")
        time_list.append(Todos.objects.filter(when=temp_time))
    todos = TodosForm()
    context = {
        "todos": todos,
        "time_list": time_list,
        "next": next_,
        "last": last_,
    }
    return render(request, "todos/working/week_todos.html", context)


def read_all(request):
    todos = Todos.objects.filter(user_id=request.user).order_by("when")
    # 값 보내기 위한 알고리즘
    time_separation = ""
    all_days = []
    for todo in todos:
        if time_separation != todo.when:
            time_separation = todo.when
            all_days.append([])

            all_days[-1].append(todo)
        else:
            all_days[-1].append(todo)
    context = {
        "all_days": all_days,
    }
    return render(request, "todos/working/read_all.html", context)
