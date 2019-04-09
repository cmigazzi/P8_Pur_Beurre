"""Contains tests for search view."""

import pytest

from django.urls import reverse

from eat_better.models import Product


@pytest.mark.django_db
class TestSearch:

    def test_status_code(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        assert response.status_code == 200

    def test_templates(self, client, django_db_populated):
        """Test search form."""
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        templates = [t.name for t in response.templates]
        assert "results.html" in templates

    def test_products_name_in_templates(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        results = response.context["results"]
        content = response.content
        for product in results:
            byte_mark = bytes(f"{product.name}", 'utf-8')
            assert byte_mark in content

    def test_product_to_search(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        product = response.context["product"]
        assert isinstance(product, Product)

    def test_searched_product_not_found(self, client, django_db_populated):
        context = {"product": "steack hachés"}
        response = client.get(reverse("search"), context)
        assert response.context["product"] == context["product"]

    def test_results(self, client, django_db_populated):
        context = {"product": "Cake aux fruits"}
        response = client.get(reverse("search"), context)
        assert len(response.context["results"]) != 0
        for product in response.context["results"]:
            assert isinstance(product, Product)

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

    def test_searched_product_is_already_healthy(self, client,
                                                 django_db_populated):
        searched_product = Product.objects.filter(nutriscore="a")[0]
        context = {"product": searched_product.name}
        response = client.get(reverse("search"), context)

        assert response.context["is_healthy"] is True
