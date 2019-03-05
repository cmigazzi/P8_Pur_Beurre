"""Contain tests configuration and fixtures"""

import pytest


@pytest.fixture()
def index_url_get(client):
    response = client.get('/')
    return response
