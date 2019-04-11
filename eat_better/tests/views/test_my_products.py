"""Contains tests for my_products view."""

from django.urls import reverse


class TestMyProducts:

    def test_user_is_not_authenticated(self, client):
        response = client.get(reverse("my_products"))
        assert response.status_code == 302
        assert "login" in response.url

    def test_user_is_authenticated(self, client, user_for_test):
        response = client.get(reverse("my_products"))
        templates = [t.name for t in response.templates]

        assert response.status_code == 200
        assert "my-products.html" in templates

    def test_no_products(self, client, user_for_test):
        response = client.get(reverse("my_products"))
        result = bytes("Aucun produit enregistré", "utf-8")
        assert result in response.content
