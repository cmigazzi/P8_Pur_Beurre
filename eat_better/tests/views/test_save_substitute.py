"""Contains tests for save_substitute view."""

import json

from django.urls import reverse


class TestSaveSubstitute:

    def test_user_is_not_authenticated(self, client, django_db_populated):
        data = {"data": {
                    "original": 3803,
                    "substitute": 3043
                         }
                }
        json_data = json.dumps(data)
        json_response = client.post(reverse("save_substitute"),
                                    json_data,
                                    content_type="application/json",
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        response = json.loads(json_response.content)
        assert response["title"] == "Non connecté"

    def test_is_not_ajax(self, client, django_db_populated):
        data = {"data": {
                    "original": 3803,
                    "substitute": 3043
                         }
                }
        json_data = json.dumps(data)
        json_response = client.post(reverse("save_substitute"),
                                    json_data,
                                    content_type="application/json")
        response = json.loads(json_response.content)
        assert response["message"] == "Erreur de requête"

    def test_user_is_authenticated(self, client,
                                   django_user_model, user_for_test):
        data = {"original": "3803", "substitute": "3911"}
        json_response = client.post(reverse("save_substitute"),
                                    data,
                                    content_type="application/json",
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        response = json.loads(json_response.content)
        assert response["title"] == "Succès"
