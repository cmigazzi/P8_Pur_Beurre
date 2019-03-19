"""Contains tests for search view."""

import pytest

from django.urls import reverse

from eat_better.models import Product


class TestSearch:

    @pytest.mark.django_db
    def test_status_code(self, client, django_db_populated):
        context = {"product": "Quatre-Quarts Pur Beurre"}
        response = client.get(reverse("search"), context)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_templates(self, client, django_db_populated):
        """Test search form."""
        context = {"product": "Quatre-Quarts Pur Beurre"}
        response = client.get(reverse("search"), context)
        templates = [t.name for t in response.templates]
        assert "results.html" in templates

    @pytest.mark.django_db
    def test_product_to_search(self, client, django_db_populated):
        context = {"product": "Quatre-Quarts Pur Beurre"}
        response = client.get(reverse("search"), context)
        assert response.context["product"] == context["product"]

    @pytest.mark.django_db
    def test_results(self, client, django_db_populated):
        context = {"product": "Quatre-Quarts Pur Beurre"}
        response = client.get(reverse("search"), context)
        assert len(response.context["results"]) != 0
        for product in response.context["results"]:
            assert isinstance(product, Product)
