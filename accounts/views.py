from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            # 바꿔야 함!
            return redirect("accounts:signup")

    else:
        form = CustomUserCreationForm()

    context = {
        "form": form,
    }

    # 바꿔야 함!
    return render(request, "test/signup.html", context)