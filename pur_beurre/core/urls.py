from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import signup


urlpatterns = [
    path("login/", auth_views.LoginView.as_view()),
    path("logout/", auth_views.LogoutView.as_view()),
    path("signup/", signup, name="signup"),
    # path("login/", )
]
