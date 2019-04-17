"""Contains tests for LoginForm and UserCreationForm."""

import pytest

from core.forms import LoginForm, UserCreationForm


def test_valid_login_form(user_for_test):
    """Test the login form with a valid user."""
    valid_data = {"username": "test@test.com", "password": "djangotest"}
    valid_form = LoginForm(data=valid_data)
    assert valid_form.is_valid() is True


@pytest.mark.django_db
def test_invalid_login_form():
    """Test login form with wrong username."""
    invalid_data = {"username": "test@no.com", "password": "djangotest"}
    invalid_form = LoginForm(data=invalid_data)
    assert invalid_form.is_valid() is False


@pytest.mark.django_db
def test_valid_user_creation_form():
    """Test user creation form with valid data."""
    data = {"email": "create@test.com",
                     "password1": "djangotest",
                     "password2": "djangotest"}
    form = UserCreationForm(data=data)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_user_creation_form_with_password_error():
    """Test user creation form with passwords that don't match."""
    data = {"email": "create@test.com",
            "password1": "djangotest",
            "password2": "django"}
    form = UserCreationForm(data=data)
    assert form.is_valid() is False


@pytest.mark.django_db
def test_user_creation_form_with_email_error():
    """Test user creation form with invalid email adress."""
    data = {"email": "createtest.com",
            "password1": "djangotest",
            "password2": "djangotest"}
    form = UserCreationForm(data=data)
    assert form.is_valid() is False
