from .forms import LoginForm, UserCreationForm


def auth_and_signup(request):
    forms = {"auth_form": LoginForm(),
             "user_creation_form": UserCreationForm}
    return forms
