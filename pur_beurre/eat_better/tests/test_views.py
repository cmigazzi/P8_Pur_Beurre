"""Contains tests for index url"""
import json

import pytest

from django.urls import reverse


class TestIndex():

    @pytest.mark.django_db
    def test_basic(self, index_url_get):
        """Test home url."""
        assert index_url_get.status_code == 200

    @pytest.mark.django_db
    def test_index_templates(self, index_url_get):
        """Test index url use index.html."""
        templates = [t.name for t in index_url_get.templates]
        assert index_url_get.context["search_form"]
        assert "index.html" in templates
        assert "search.html" in templates

    def test_legals(self, legals_url_get):
        """Test legals url use mentions-legales.html."""
        templates = legals_url_get.templates
        assert "mentions-legales.html" in [t.name for t in templates]

    def test_search(self, client):
        """Test search form."""
        context = {"product": "Nutella"}
        response = client.get(reverse("search"), context)
        assert response.status_code == 200

        templates = [t.name for t in response.templates]
        assert "results.html" in templates
        assert response.context["product"] == context["product"]

    # def test_index_ajax(self, client, product_query):
    #     """Test ajax requests for autocompletion."""
    #     data = json.dump({'text': 'N'})
    #     response = client.post('/',
    #                            data,
    #                            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    #     assert len(response.json()["results"]) == 5
