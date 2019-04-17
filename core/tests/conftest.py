"""Contains fixtures for core app tests."""

import pytest


@pytest.fixture()
def user_for_test(client, django_user_model):
    """Create a user for tests."""
    login_data = {"email": "test@test.com", "password": "djangotest"}
    django_user_model.objects.create_user(**login_data)
    client.login(**login_data)
