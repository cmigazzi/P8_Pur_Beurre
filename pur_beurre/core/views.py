"""Contains views for core app."""

from django.shortcuts import render, redirect
from .forms import UserCreationForm


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = UserCreationForm()
    context = {"form": form}
    return render(request, "signup.html", context)
