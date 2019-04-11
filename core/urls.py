from django.urls import path
from django.contrib.auth import views as auth_views

from .views import signup
from .forms import LoginForm


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(
            template_name="login.html",
            authentication_form=LoginForm), 
         name="login"),
    path("logout/", auth_views.LogoutView.as_view()),
    path("signup/", signup, name="signup"),
]
