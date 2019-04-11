"""Contains tests for index view"""

import json

import pytest

from django.urls import reverse
from django.http import JsonResponse


@pytest.mark.django_db
class TestIndex():

    def test_basic(self, index_url_get):
        """Test home url."""
        assert index_url_get.status_code == 200

    def test_templates(self, index_url_get):
        """Test index url use index.html."""
        templates = [t.name for t in index_url_get.templates]
        assert index_url_get.context["search_form"]
        assert "index.html" in templates
        assert "search.html" in templates

    def test_post(self, client, django_db_blocker):
        with django_db_blocker.unblock():
            data = json.dumps({"term": "N"})
            response = client.post(reverse("index"),
                                   data,
                                   content_type="application/json")
            assert response.status_code == 200
            assert isinstance(response, JsonResponse)
