from django.urls import path
from . import views

app_name = "todos"

urlpatterns = [
    path("today/", views.today, name="today"),
    path("create/", views.create, name="create"),
    path("delete/<int:todos_pk>", views.delete, name="delete"),
    path("week/", views.week, name="week"),
    path("week/<str:few_week>", views.week_asyn, name="week_asyn"),
    path("read_all", views.read_all, name="read_all"),
    path("update/<int:pk>", views.update, name="update"),
    path("is_completed/", views.is_completed, name="is_completed"),
    path("detail_asyn/", views.detail_asyn, name="detail_asyn"),
]
