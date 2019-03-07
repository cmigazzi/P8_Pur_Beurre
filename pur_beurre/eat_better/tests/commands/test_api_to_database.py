from eat_better.management.commands.api_to_database.get_data import Api


def test_api():
    a = Api()
    assert a


def test_api_call(off_api_request):
    """Test Api call method."""
    a = Api()
    products = a.call()
    for p in products:
        assert "product_name_fr" in p.keys()
        assert "categories" in p.keys()
        assert "brands" in p.keys()
        assert "nutriments" in p.keys()
        assert "nutrition_grade_fr" in p.keys()


def test_bad_products(off_api_bad_products):
    """Test bad product management"""
    a = Api()
    products = a.call()
    assert products == []