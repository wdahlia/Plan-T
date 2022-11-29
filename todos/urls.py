from django.urls import path
from . import views

app_name = "todos"

urlpatterns = [
    path("today", views.today, name="today"),
    path("create", views.create, name="create"),
    path("delete/<int:todos_pk>", views.delete, name="delete"),
    path("timetable/", views.timetable, name="timetable"),
    path("week", views.week, name="week"),
]
