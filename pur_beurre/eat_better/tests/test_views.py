"""Contains tests for index url"""


class TestIndex():

    def test_basic(self, index_url_get):
        """Test home url."""
        assert index_url_get.status_code == 200

    def test_contacts(self, index_url_get):
        """Test index url use index.html."""
        templates = index_url_get.templates
        assert "index.html" in [t.name for t in templates]

    def test_legals(self, legals_url_get):
        """Test legals url use mentions-legales.html."""
        templates = legals_url_get.templates
        assert "mentions-legales.html" in [t.name for t in templates]
