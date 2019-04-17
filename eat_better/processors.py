"""Contains the context processors of eat_better app."""

from .forms import NavSearchForm


def nav_search_form(request):
    """Define the navbar search form in the context of each views."""
    forms = {"nav_search_form": NavSearchForm()}
    return forms
