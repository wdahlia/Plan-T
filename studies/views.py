from django.shortcuts import render, redirect, get_object_or_404
from .models import Study
from .forms import StudyTodoForm

# Create your views here.
def index(request):
    return render(request, "studies/test/index.html")


def create_todos(request, study_pk):
    study = Study.objects.get(pk=study_pk)
    if request.method == "POST":
        when = request.POST.get("when")
        todoForm = StudyTodoForm(request.POST)
        if todoForm.is_valid():
            todo = todoForm.save(commit=False)
            users = study.participated
            todo.when = when
            for user in users:
                todo.user_id = user
                todo.save()
        return redirect("studies:index")  # redirect 위치 임시
