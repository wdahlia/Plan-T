from django.shortcuts import render, redirect
from .models import Study
from .forms import StudyForm

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
