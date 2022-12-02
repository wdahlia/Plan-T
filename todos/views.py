from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model as User
from .forms import TodosForm
from .models import Todos
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib import messages
from .function import change_value

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
        start, end, when = (
            request.POST.get("started_at"),
            request.POST.get("expired_at"),
            request.POST.get("when"),
        )
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

        if start and end != "":
            timetable = set(range(change_value(start), change_value(end) + 1))
            if (start < end) and timetable.isdisjoint(exist):
                pass
            else:
                start = ""
                end = ""
                messages.warning(request, "시간이 잘못되었습니다.")
                return redirect("todos:today")

        # 시작시간만 입력하거나 끝나는 시간만 입력했을 때
        elif start != "" and end == "":
            messages.error(request, "끝나는 시간을 입력해주세요.")
            return redirect("todos:today")
        elif start == "" and end != "":
            messages.error(request, "시작 시간을 입력해주세요.")
            return redirect("todos:today")
        else:
            pass

        if todoForm.is_valid():
            todo = todoForm.save(commit=False)
            when += " 09:00:00"  # 시간 저장할때 9시간을 더해줘야 한국시간으로 잘 저장이 된다.
            todo.user_id, todo.when, todo.started_at, todo.expired_at = (
                user,
                when,
                start,
                end,
            )
            todo.save()
        return redirect("todos:today")  # 추후에 비동기로 반드시 바꾸어 줘야 함.
    else:
        messages.warning(request, "잘 못 된 접근입니다.")
        return redirect("todos:today")


def delete(request, todos_pk):
    if request.method == "POST":
        todo = Todos.objects.get(pk=todos_pk)
        todo.delete()
    return redirect("todos:today")  # 추후에 비동기로 바꾸는거 권장



def update(request, pk):
    if request.method == "POST":
        todo = get_object_or_404(Todos, pk=pk)
        todoForm = TodosForm(request.POST, request.FILES, instance=todo)
        start, end, when = (
            request.POST.get("started_at"),
            request.POST.get("expired_at"),
            request.POST.get("when"),
        )

        user = request.user
        today = str(datetime.now())[:10]
        today_todos = Todos.objects.filter(user_id=request.user, when=today)

        # 타임테이블 중복 여부 판별
        exist = set()
        for todo in today_todos:
            if todo.started_at is not None:
                st = change_value(todo.started_at)
                ed = change_value(todo.expired_at)
                for t in range(st, ed + 1):
                    exist.add(t)

        if (start and end) != "":
            timetable = set(range(change_value(start), change_value(end) + 1))
            if (start < end) and timetable.isdisjoint(exist):
                pass
            else:
                start = ""
                end = ""
                messages.warning(request, "시간이 잘못되었습니다.")
                return redirect("todos:today")

        # 시작시간만 입력하거나 끝나는 시간만 입력했을 때
        elif start != "" and end == "":
            messages.error(request, "끝나는 시간을 입력해주세요.")
            return redirect("todos:today")
        elif start == "" and end != "":
            messages.error(request, "시작 시간을 입력해주세요.")
            return redirect("todos:today")
        else:
            pass

        if todoForm.is_valid():
            todo = todoForm.save(commit=False)
            when += " 09:00:00"  # 시간 저장할때 9시간을 더해줘야 한국시간으로 잘 저장이 된다.
            todo.user_id, todo.when, todo.started_at, todo.expired_at = (
                user,
                when,
                start,
                end,
            )
            todo.save()
        return redirect("todos:today")
    else:
        messages.warning(request, "잘 못 된 접근입니다.")
        return redirect("todos:today")

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
