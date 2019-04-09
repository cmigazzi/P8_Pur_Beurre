"""Contains tests for search view."""

import pytest

from django.urls import reverse

from eat_better.models import Product


class TestSearch:

    @pytest.mark.django_db
    def test_status_code(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_templates(self, client, django_db_populated):
        """Test search form."""
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        templates = [t.name for t in response.templates]
        assert "results.html" in templates

    @pytest.mark.django_db
    def test_products_name_in_templates(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        results = response.context["results"]
        content = response.content
        for product in results:
            byte_mark = bytes(f"{product.name}", 'utf-8')
            assert byte_mark in content

    @pytest.mark.django_db
    def test_product_to_search(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        product = response.context["product"]
        assert isinstance(product, Product)

    @pytest.mark.django_db
    def test_searched_product_not_found(self, client, django_db_populated):
        context = {"product": "steack hachés"}
        response = client.get(reverse("search"), context)
        assert response.context["product"] == context["product"]

    @pytest.mark.django_db
    def test_results(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        assert len(response.context["results"]) != 0
        for product in response.context["results"]:
            assert isinstance(product, Product)

    @pytest.mark.django_db
    def test_query_results(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        searched_product = Product.objects.get(name=context["product"])
        categories = searched_product.categories.all()
        response = client.get(reverse("search"), context)
        results = response.context["results"]
        for product in results:
            assert product.nutriscore < searched_product.nutriscore
            assert len([c for c in product.categories.all()
                        if c in categories]) != 0
