from django.urls import path
from . import views

app_name = "todos"

urlpatterns = [
    path("todos/", views.index, name="index"),
    path("timetable/", views.timetable, name="timetable"),
]
