"""Contains tests for core models."""
import pytest

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from core.models import User, UserManager


@pytest.mark.django_db
class TestUser:
    def test_model_exist(self):
        """Test that User model exist."""
        assert issubclass(User, AbstractBaseUser)

    def test_user_manager_exist(self):
        """Test that UserManager exist."""
        assert issubclass(UserManager, BaseUserManager)

    def test_create_user(self):
        """Test user creation."""
        User.objects.create_user(email="non@oui.com", password="ouinon")
        assert User.objects.get(email="non@oui.com")

    def test_create_superuser(self):
        """Test superuser creation."""
        User.objects.create_superuser(email="admin@root.com", password="ouinon")
        assert User.objects.get(email="admin@root.com").is_staff is True

    def test_create_user_without_email(self):
        """Test user creation without email."""
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="ouinon")

    def test_create_user_without_password(self):
        """Test user creation without password.""""
        with pytest.raises(ValueError):
            User.objects.create_user(email="non@oui.com", password="")
