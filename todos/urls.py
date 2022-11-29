from django.urls import path
from . import views

app_name = "todos"

urlpatterns = [
    path("today", views.today, name="today"),
]
