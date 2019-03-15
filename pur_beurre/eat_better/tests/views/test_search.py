"""Contains tests for search view."""

from django.urls import reverse


class TestSearch():

    def test_search(self, client):
        """Test search form."""
        context = {"product": "Nutella"}
        response = client.get(reverse("search"), context)
        assert response.status_code == 200

        templates = [t.name for t in response.templates]
        assert "results.html" in templates
        assert response.context["product"] == context["product"]