"""Contains tests for details view."""

import pytest

from django.urls import reverse


@pytest.mark.django_db
class TestDetails:

    def test_status_code_with_valid_product(self, client, django_db_populated):
        response = client.get(reverse("details", args=[3803]))
        assert response.status_code == 200

    def test_templates(self, client):
        response = client.get(reverse("details", args=[3803]))
        templates = [t.name for t in response.templates]
        assert "details.html" in templates

    def test_404_error(self, client):
        response = client.get(reverse("details", args=[3805643]))
        assert response.status_code == 404
