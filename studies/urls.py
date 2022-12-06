from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("create/<int:study_pk>", views.create_todos, name="create_todos"),
    path("detail/<int:study_pk>", views.detail, name="detail"),
    path("detail/<int:study_pk>/join", views.join, name="join"),
    path("detail/<int:study_pk>/<int:user_pk>/accept", views.accept, name="accept"),
]
