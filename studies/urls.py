from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/<int:study_pk>", views.create_todos, name="create_todos"),
]
