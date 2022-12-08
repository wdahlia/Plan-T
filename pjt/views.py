from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return redirect("todos:today")
    return render(request, "main_index.html")
