"""Tests for api_to_database module."""
import pytest

from eat_better.management.commands.api_to_database.api \
    import Api
from eat_better.management.commands.api_to_database.product_recorder \
    import ProductRecorder
from eat_better.models import Nutriments, Brand, Product, Hierarchy

from decimal import Decimal


def test_api():
    """Test Api class exist."""
    a = Api()
    assert a


def test_api_call(clean_product):
    """Test Api call method."""
    a = Api()
    products = a.call()
    assert clean_product in products


def test_bad_products(off_api_bad_products):
    """Test bad product management."""
    a = Api()
    products = a.call()
    assert products == []


def test_rename_fields(good_product, product_without_category):
    """Test rename_field static method."""
    p = Api().rename_fields(good_product, "Biscuits et gâteaux")
    result = {'nutriscore': 'e',
              'brand': 'LU',
              'name': 'Granola Chocolat au Lait',
              'categories': [(0, "Biscuits et gâteaux"),
                             (1, "Biscuits"),
                             (2, "Biscuits au chocolat"),
                             (3, "Biscuits au chocolat au lait")],
              'url': "https://fr.openfoodfacts.org/produit/"
                     "3017760826174/granola-chocolat-au-lait-lu",
              'image': "https://static.openfoodfacts.org/images/products/"
                       "301/776/082/6174/front_fr.5.200.jpg",
              'nutriments': {
                            'saturated_fat': '13',
                            'fat': '24',
                            'sugars': '30',
                            'salt': 1.1938},
              }

    bad_p = Api().rename_fields(product_without_category,
                                "Biscuits et gâteaux")
    assert p == result
    assert bad_p is False


@pytest.mark.django_db
def test_product_recorder(clean_product):
    """Test ProductRecorder."""
    p = ProductRecorder(clean_product)
    product = Product.objects.get(name=clean_product["name"])
    assert p.product_input == clean_product

    # test nutriments
    n = Nutriments.objects.get(id=p.nutriments.id)
    assert n.saturated_fat == 13.0
    assert n.fat == 24.0
    assert n.sugars == 30.0
    assert n.salt == Decimal('1.194')

    # test categories
    assert [c.name for l, c in p.categories] == [n for l, n in
                                                 clean_product["categories"]]

    # test brand
    assert p.brand == Brand.objects.get(name=clean_product["brand"])

    # test product
    assert p.product == product
    assert p.product.name == clean_product["name"]
    assert p.product.brand.name == clean_product["brand"]
    assert p.product.image == clean_product["image"]

    fat = clean_product["nutriments"]["fat"]
    assert p.product.nutriments.fat == fat

    # test hierarchy
    categories_hierarchy = Hierarchy.objects.filter(product=product)
    assert len(categories_hierarchy) != 0
    for c in categories_hierarchy:
        assert str(c.level), c.category in p.categories
