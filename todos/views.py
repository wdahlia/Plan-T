from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model as User
from .forms import TimetableForm, TodosForm
from .models import Timetable, Todos
from datetime import datetime


# Create your views here.
def today(request):
    if request.method == "POST":
        pass  # 은진 누나 완성되면 합칠 예정.
    else:
        # 아직 테스트는 안해봤음.
        today = "2022-11-29"  # pk or input 으로 받을지 정해야됨. 임시
        todosForm = TodosForm()
        today_todos = Todos.objects.filter(started_at=today)
        today_timetable = Timetable.objects.filter(today=today)  # 이 부분은 작동하는지 모르겠음.
    context = {
        "todosForm": todosForm,
        "today_todos": today_todos,
        "today_timetable": today_timetable,
    }
    return render(request, "todos/working/index.html", context)


def timetable(request):
    # today = str(datetime.now())[:10]
    # timetable = Timetable.objects.filter(today__contain=today)
    if request.method == "POST":
        timetable_form = TimetableForm(request.POST)
        if timetable_form.is_valid():
            save_file = timetable_form.save()
    else:
        timetable_form = TimetableForm()
    # context = {"timetable_form": timetable_form, "timetable": timetable}
    context = {"timetable_form": timetable_form}
    return render(request, "todos/working/timetable.html", context)


def week(request):
    # 미완성
    # 1
    # 날짜를 어떻게 받을지 아직 못정함.
    # 화면에 할일을 클릭은 주소 url이 좋을거 같지만
    # 여기서 값을 받는것은 JS를 활용한 input값 받기 일거 같다.
    sunday_todos = Todos.objects.filter(started_at="일")
    monday_todos = Todos.objects.filter(started_at="월")
    tuesday_todos = Todos.objects.filter(started_at="화")
    wednesday_todos = Todos.objects.filter(started_at="수")
    thursday_todos = Todos.objects.filter(started_at="목")
    friday_todos = Todos.objects.filter(started_at="금")
    saturday_todos = Todos.objects.filter(started_at="토")
    # 다음주 지난주 클릭은 비동기로 axios를 사용하여 서버와 통신하게 만들어야 될 거 같다.

    # 2
    # 과거인지 지금 혹은 미래인지 구분하기
    # 장고에서 날짜 비교가 되는지 모르겠다.
    # 비교가 된다면
    # if 2022-11-29 <= 2022-12-01:
    #   a = True
    # else:
    #   a = False
    # 해서 7개의 변수를 만들어서 context로 보내준다.

    # 3
    todos = TodosForm()
    context = {
        "todos": todos,
    }
    return render(request, "todos/working/week.html", context)


def create(request):
    if request.method == "POST":
        todoForm = TodosForm(request.POST, request.FILES)
        if todoForm.is_valid():
            todoForm.save()
    return redirect("todos:today")  # 추후에 비동기로 반드시 바꾸어 줘야 함.


def delete(request, todos_pk):
    if request.method == "POST":
        todo = Todos.objects.get(pk=todos_pk)
        todo.delete()
    return redirect("todos:today")  # 추후에 비동기로 바꾸는거 권장


def read_all(request):
    todos = Todos.objects.filter(user_id=request.user)
    # 알고리즘 잘 작동하나 확인 필요
    # 예상 모형 [[2022-10-12,2022-10-12,2022-10-12],[2022-10-13,2022-10-13,2022-10-13],[2022-10-14,2022-10-14,2022-10-14]]
    time = ""
    all_days = []
    for todo in todos:
        if time != todo.started_at:
            time = todo.started_at
            all_days.append()
            all_days[-1].append(time)
        else:
            all_days[-1].append(time)
    context = {
        "all_days": all_days,
    }
    return render(request, "todos/working/read_all.html", context)
