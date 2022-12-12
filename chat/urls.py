from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('<int:study_pk>/', views.room, name="room"),
]