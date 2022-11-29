from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("test/", views.test, name="test"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("delete/", views.delete, name="delete"),
]
