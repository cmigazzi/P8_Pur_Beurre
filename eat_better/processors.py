from .forms import NavSearchForm


def nav_search_form(request):
    forms = {"nav_search_form": NavSearchForm()}
    return forms
