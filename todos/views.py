from django.shortcuts import render, redirect
from .forms import TodosForm
from .models import Timetable, Todos

# Create your views here.
def today(request):
    if request.method == "POST":
        pass  # 은진 누나 완성되면 합칠 예정.
    else:
        # 아직 테스트는 안해봤음.
        today = "2022-11-29"  # pk or input 으로 받을지 정해야됨. 임시
        todos = TodosForm()
        today_todos = Todos.objects.filter(started_at=today)
        today_timetable = Timetable.objects.filter(today=today)  # 이 부분은 작동하는지 모르겠음.
    context = {
        "todos": todos,
        "today_todos": today_todos,
        "today_timetable": today_timetable,
    }
    return render(request, "todos/working/index.html", context)
