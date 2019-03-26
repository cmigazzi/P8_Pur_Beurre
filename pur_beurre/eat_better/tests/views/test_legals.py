"""Contains tests for legals view."""
import pytest


class TestLegals():

    @pytest.mark.django_db
    def test_legals(self, legals_url_get):
        """Test legals url use mentions-legales.html."""
        templates = legals_url_get.templates
        assert "mentions-legales.html" in [t.name for t in templates]
