from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model as User
from .forms import TimetableForm
from .models import Timetable
from datetime import datetime

# Create your views here.
def index(request):

    return render(request, "todos/working/index.html")


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
