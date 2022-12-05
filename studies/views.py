from django.shortcuts import render, redirect, get_object_or_404
from .models import Study
from .forms import StudyForm, StudyTodoForm

# Create your views here.
def index(request):
    all_studies = Study.objects.all()
    context = {"all_studies": all_studies}
    return render(request, "studies/test/index.html", context)


def create(request):
    if request.method == "POST":
        studyform = StudyForm(request.POST)
        if studyform.is_valid():
            form = studyform.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect("studies:index")
    else:
        studyform = StudyForm()
    context = {"studyform": studyform}
    return render(request, "studies/test/create.html", context)


def create_todos(request, study_pk):
    if request.method == "POST":
        study = Study.objects.get(pk=study_pk)
        when = request.POST.get("when")
        todoForm = StudyTodoForm(request.POST)

        if todoForm.is_valid():
            todo = todoForm.save(commit=False)
            todo.when = when

            # 스터디원 모두를 위해 생성
            users = study.participated
            for user in users:
                todo.user_id = user
                todo.save()
        return redirect("studies:index")  # redirect 위치 임시
