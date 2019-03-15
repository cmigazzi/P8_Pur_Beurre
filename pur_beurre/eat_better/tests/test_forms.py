from eat_better.forms import SearchForm


def test_search_form():
    valid_data = {"product": "Nutella"}
    invalid_data = {"product": ""}
    valid_form = SearchForm(data=valid_data)
    invalid_form = SearchForm(data=invalid_data)

    assert valid_form.is_valid() is True
    assert invalid_form.is_valid() is False
