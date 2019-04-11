"""Contains tests for signup views and url."""
import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from core.forms import UserCreationForm

User = get_user_model()


@pytest.mark.django_db
class TestSignup:

    def test_url(self, client):
        assert client.get(reverse("signup"))

    def test_template(self, client):
        response = client.get(reverse("signup"))
        assert "signup.html" in [t.name for t in response.templates]

    def test_view_return_user_creation_form(self, client):
        response = client.get(reverse("signup"))
        assert isinstance(response.context["user_creation_form"],
                          UserCreationForm)

    def test_post_form(self, client):
        data = {"email": "jondoe@gmail.com",
                "password1": "iamjon2019",
                "password2": "iamjon2019"}

        client.post(reverse("signup"), data)
        user = User.objects.get(email="jondoe@gmail.com")
        assert user
