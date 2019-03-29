from django import forms


class SearchForm(forms.Form):
    product = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
                    "class": "form-control mr-2 autocomplete col-lg-9 col-md-8 col-sm-6 col-xs-4 search-field",
                    "placeholder": "Produit"})
                             )


class NavSearchForm(forms.Form):
    product = forms.CharField(
        max_length=150,
        label='', 
        widget=forms.TextInput(attrs={
                    "class": "form-control input-sm mr-sm-1 search-field",
                    "type": "search",
                    "placeholder": "Chercher",
                    "aria-label": "Search"})
                             )
