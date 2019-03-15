"""Contains tests for index view"""

import pytest


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

        # def test_index_ajax(self, client, product_query):
    #     """Test ajax requests for autocompletion."""
    #     data = json.dump({'text': 'N'})
    #     response = client.post('/',
    #                            data,
    #                            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    #     assert len(response.json()["results"]) == 5
