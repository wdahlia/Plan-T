from django.urls import path
from . import views

app_name = "todos"

urlpatterns = [
    path("timetable/", views.timetable, name="timetable"),
    path("today", views.today, name="today"),
    path("week", views.week, name="week"),
    path("create", views.create, name="create"),
]
