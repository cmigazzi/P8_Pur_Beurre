"""Contain tests configuration and fixtures"""

import pytest
import requests


@pytest.fixture()
def index_url_get(client):
    """Create fixture for root url."""
    response = client.get('/')
    return response


@pytest.fixture()
def legals_url_get(client):
    """Create fixture for /mentions-legales."""
    response = client.get('/mentions-legales/')
    return response


@pytest.fixture()
def off_api_request(monkeypatch):
    """Patch the OpenFoodFacts API call."""
    def mock_request(*args, **kwargs):
        return {'page_size': 10,
                "products": [
                    {'nutrition_grade_fr': 'e',
                        'brands': 'LU,Mondelez,Granola',
                        'product_name_fr': 'Granola Chocolat au Lait',
                        'categories': "Snacks, Snacks sucrés, "
                                      "Biscuits et gâteaux, "
                                      "Biscuits, Biscuits au chocolat, "
                                      "Biscuits au chocolat au lait",
                        'url': "https://fr.openfoodfacts.org/produit/"
                               "3017760826174/granola-chocolat-au-lait-lu",
                        'nutriments': {
                            'saturated-fat_100g': '13',
                            'fat_100g': '24',
                            'sugars_100g': '30',
                            'salt_100g': 1.1938},
                        'stores': "Carrefour"
                     }
                    ]
                }
    monkeypatch.setattr(requests, "get", mock_request)


@pytest.fixture()
def off_api_bad_products(monkeypatch):
    """Patch the OpenFoodFacts API call."""
    def mock_request(*args, **kwargs):
        return {'page_size': 10,
                "products": [
                    {'nutrition_grade_fr': 'a',
                        'brands': '',
                        'product_name_fr': 'Granola Chocolat au Lait',
                        'categories': "Snacks, Snacks sucrés, "
                                      "Biscuits et gâteaux, "
                                      "Biscuits, Biscuits au chocolat, "
                                      "Biscuits au chocolat au lait",
                        'url': "https://fr.openfoodfacts.org/produit/"
                               "3017760826174/granola-chocolat-au-lait-lu",
                        'nutriments': {
                            'saturated-fat_100g': '13',
                            'fat_100g': '24',
                            'sugars_100g': '30',
                            'salt_100g': 1.1938},
                        'stores': "Carrefour"
                     },
                    {'nutrition_grade_fr': 'b',
                        'brands': 'LU,Mondelez,Granola',
                        'product_name_fr': 'Granola Chocolat au Lait',
                        'url': "https://fr.openfoodfacts.org/produit/"
                               "3017760826174/granola-chocolat-au-lait-lu",
                        'nutriments': {
                           'saturated-fat_100g': '13',
                           'fat_100g': '24',
                           'sugars_100g': '30',
                           'salt_100g': 1.1938},
                        'stores': "Carrefour"
                     },
                    {'nutrition_grade_fr': 'c',
                        'brands': 'LU,Mondelez,Granola',
                        'product_name_fr': 'Granola Chocolat au Lait',
                        'categories': "Snacks, Snacks sucrés, "
                                      "Biscuits et gâteaux, "
                                      "Biscuits, Biscuits au chocolat, "
                                      "Biscuits au chocolat au lait",
                        'url': "https://fr.openfoodfacts.org/produit/"
                               "3017760826174/granola-chocolat-au-lait-lu",
                        'nutriments': {
                           'saturated-fat_100g': '',
                           'fat_100g': '24',
                           'sugars_100g': '30',
                           'salt_100g': 1.1938},
                        'stores': "Carrefour"
                     },
                    {'nutrition_grade_fr': 'd',
                        'brands': 'LU,Mondelez,Granola',
                        'product_name_fr': 'Granola Chocolat au Lait',
                        'categories': "Snacks, Snacks sucrés, "
                                      "Biscuits et gâteaux, "
                                      "Biscuits, Biscuits au chocolat, "
                                      "Biscuits au chocolat au lait",
                        'url': "https://fr.openfoodfacts.org/produit/"
                               "3017760826174/granola-chocolat-au-lait-lu",
                        'nutriments': {
                           'saturated-fat_100g': '13',
                           'fat_100g': '24',
                           'salt_100g': 1.1938},
                        'stores': "Carrefour"
                     }
                    ]
                }
    monkeypatch.setattr(requests, "get", mock_request)
