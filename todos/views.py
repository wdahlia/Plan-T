from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model as User
from .forms import TodosForm
from .models import Todos, Tag
from datetime import datetime, timedelta
from django.contrib import messages
from function import change_value
from django.http import JsonResponse
from django.core import serializers
import json
import math

# Create your views here.
def today(request):
    today = str(datetime.now())[:10]
    # 로그인 유저의 today todos 찾기
    today_todos = Todos.objects.filter(user_id=request.user, when=today).order_by(
        "started_at"
    )

    # timetable 넘겨주기 위해 & 달성율 체크
    achievement_cnt = 0
    time_list = []
    for todo in today_todos:
        if todo.is_completed == True:
            achievement_cnt += 1
        if (
            todo.started_at is not None  # 나중에 지워야됨
            and todo.expired_at is not None  # 나중에 지워야됨
            and todo.started_at != ""
            and todo.expired_at != ""
        ):
            start = change_value(todo.started_at)
            end = change_value(todo.expired_at)
            time = end - start

            time_list.append([])
            time_list[-1].append(start)
            time_list[-1].append(time)
    if len(today_todos) != 0:
        achievement_rate = round(100 * (achievement_cnt / len(today_todos)))
    else:
        achievement_rate = 0
    todosForm = TodosForm()

    if request.method == "POST":
        res_json = serializers.serialize(
            "json",
            Todos.objects.filter(user_id=request.user, when=today).order_by(
                "started_at"
            ),
        )
        return JsonResponse({"resJson": res_json})

    context = {
        "time_list": time_list,
        "today_todos": today_todos,
        "todosForm": todosForm,
        "achievement_rate": achievement_rate,
    }
    return render(request, "todos/complete/today_main.html", context)


def create(request):
    if request.method == "POST":
        start, end, tags = (
            request.POST.get("started_at"),
            request.POST.get("expired_at"),
            request.POST.get("tags"),
        )
        todoForm = TodosForm(request.POST, request.FILES)

        # timetable 체크 및 중복되면 저장 x
        user = request.user
        today = str(datetime.now())[:10]
        today_todos = Todos.objects.filter(user_id=request.user, when=today)

        # 시간 입력이 잘못되었을때
        exist = set()
        for todo in today_todos:
            if todo.started_at != "":
                st = change_value(todo.started_at)
                ed = change_value(todo.expired_at)
                for t in range(st, ed + 1):
                    exist.add(t)
        if (start != "") and (end != ""):
            timetable = set(range(change_value(start), change_value(end) + 1))
            if (start <= end) and (timetable.isdisjoint(exist)):
                pass
            else:
                messages.warning(request, "시간이 잘못되었습니다.")
                return redirect("todos:today")
        elif (start != "") and (end == ""):
            messages.error(request, "끝나는 시간을 입력해주세요.")
            return redirect("todos:today")
        elif (start == "") and (end != ""):
            messages.error(request, "시작 시간을 입력해주세요.")
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
            if tags != "":
                if "," in tags:
                    taglist = list(tags.replace(" ", "").split(","))
                else:
                    taglist = list(tags.replace(" ", ""))
                for t in taglist:
                    Tag.objects.create(todo=todo, content=t)

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
    todo = get_object_or_404(Todos, pk=pk)

    if request.method == "POST":
        todoForm = TodosForm(request.POST, request.FILES, instance=todo)
        start, end, when, tags = (
            request.POST.get("started_at"),
            request.POST.get("expired_at"),
            request.POST.get("when"),
            request.POST.get("tags"),
        )

        user = request.user
        today = str(datetime.now())[:10]
        today_todos = Todos.objects.filter(user_id=request.user, when=today)

        # 시간은 수정 기능 막아둬서 주석 처리함

        # 시간 입력이 잘못되었을때
        # exist = set()
        # for todo in today_todos:
        #     if todo.started_at != "":
        #         st = change_value(todo.started_at)
        #         ed = change_value(todo.expired_at)
        #         for t in range(st, ed + 1):
        #             exist.add(t)

        # if (start != "") and (end != ""):
        #     timetable = set(range(change_value(start), change_value(end) + 1))
        #     if (start <= end) and (timetable.isdisjoint(exist)):
        #         pass
        #     else:
        #         messages.warning(request, "시간이 잘못되었습니다.")
        #         return redirect("todos:today")
        # elif (start != "") and (end == ""):
        #     messages.error(request, "끝나는 시간을 입력해주세요.")
        #     return redirect("todos:today")
        # elif (start == "") and (end != ""):
        #     messages.error(request, "시작 시간을 입력해주세요.")
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
            if tags != "":
                if "," in tags:
                    taglist = list(tags.replace(" ", "").split(","))
                else:
                    taglist = list(tags.replace(" ", ""))
                for t in taglist:
                    Tag.objects.create(todo=todo, content=t)
        context = {
            "todoTitle": todo.title,
            "todoCont": todo.content,
        }
        return JsonResponse(context)
        # return redirect("todos:today")
    else:
        todoForm = TodosForm(instance=todo)
        context = {
            "todoForm": todoForm,
        }
        return JsonResponse(context)


def week(request):
    # 추후 프론트에서 다음주 지난주 어떻게 보낼줄 지 정해주면 수정하면 됨
    few_week = 0  # int(few_week)
    next_ = +1
    last_ = -1
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
    return render(request, "todos/complete/week_todos.html", context)


def week_asyn(request, few_week):
    # 추후 프론트에서 다음주 지난주 어떻게 보낼줄 지 정해주면 수정하면 됨
    few_week = int(few_week)
    # next_ = few_week + 1
    # last_ = few_week - 1
    today = datetime.today().weekday() + 1
    now = datetime.now()
    week = now + timedelta(weeks=few_week, days=-(today % 7))
    print("today :", today)
    print("현재 : ", now)
    print("기준 날짜 : ", week)

    time_list = []
    res = []
    for i in range(7):
        temp = week + timedelta(days=i)
        # RuntimeWarning: 이 나온다.
        temp_time = temp.strftime("%Y-%m-%d")
        time_list.append(Todos.objects.filter(when=temp_time))
        res_json = serializers.serialize("json", Todos.objects.filter(when=temp_time))
        # print(res_json)
        res.append(res_json)
        # print(res[i])

    todos = TodosForm()

    if request.method == "GET":
        # print(res)
        return JsonResponse({"resJson": res})

    # temp = week + timedelta(days=i)
    # temp_time = temp.strftime("%Y-%m-%d") + " 09:00:00"
    # res_json = serializers.serialize("json", Todos.objects.filter(when=temp_time))

    # print(res)
    context = {
        "todos": todos,
        "time_list": time_list,
        # "next": next_,
        # "last": last_,
    }
    return render(request, "todos/complete/week_todos.html", context)


from dateutil.relativedelta import relativedelta


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
    past = Todos.objects.filter(
        user_id=request.user, when__range=(few_month_ago, yesterday)
    ).order_by("-when")
    # 현재
    present = Todos.objects.filter(user_id=request.user, when=today)
    # 미래
    tomorrow = str(now + timedelta(days=1))[:10]
    future = Todos.objects.filter(user_id=request.user, when__gte=tomorrow).order_by(
        "when"
    )
    #

    # test
    # for p in past:
    #     print(p.when, "past")
    # for p in present:
    #     print(p.when, "present")
    # for p in future:
    #     print(p.when, "future")
    #
    context = {
        "past": past,
        "present": present,
        "future": future,
    }
    return render(request, "todos/complete/all_todos.html", context)


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
