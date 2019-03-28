import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .forms import SearchForm
from .models import Product, Substitution


def index(request):
    """Returns view for index url."""
    if request.method == "POST":
        term = json.loads(request.body.decode("utf-8"))["term"].lower()
        products = Product.objects.filter(name__istartswith=term).distinct()[:5]
        data = [{"name": p.name} for p in products]
        return JsonResponse(data, safe=False)

    searched_form = SearchForm()
    context = {"search_form": searched_form}
    return render(request, "index.html", context)


def legals(request):
    """Returns view for legals url."""
    return render(request, "mentions-legales.html")


def search(request):
    """Returns view for search url."""
    try:
        searched_product = Product.objects.filter(
                    name=request.GET.get("product"))[0]
        results = []
        for hierarchy in searched_product.hierarchy_set.all():
            pre_results = Product.objects.filter(
                            nutriscore__lt=searched_product.nutriscore,
                            categories__name=hierarchy.category)

            if len(results) == 0 and len(pre_results) != 0:
                results = pre_results
                if len(results) > 80:
                    break

            elif len(results) + len(pre_results) > 80:
                results.union(pre_results)
                break

            elif len(results) != 0:
                results.union(pre_results)

    except IndexError:
        searched_product = request.GET.get("product")
        results = []

    context = {"product": searched_product,
               "results": results}
    return render(request, "results.html", context)


def details(request, id_product):
    """Return view for details url."""
    product = Product.objects.get(id=id_product)
    context = {"product": product,
               "nutriments": product.nutriments}
    return render(request, "details.html", context)


@require_http_methods(["POST"])
def save_substitute(request):
    if request.is_ajax():
        data = json.loads(request.POST["data"])
        user = request.user
        try:
            original = Product.objects.get(id=data["original"])
            substitute = Product.objects.get(id=data["substitute"])
            Substitution.objects.create(user=user,
                                        original=original,
                                        substitute=substitute)
        except ObjectDoesNotExist:
            response = {
              "title": "Erreur",
              "message": "Impossible de retrouver les produits à sauvegarder."}
        else:
            response = {
                "title": "Succès",
                "message": "Le produit est sauvegardé !"}
    else:
        response = {
            "title": "Erreur",
            "message": "Erreur de requête"}
    return JsonResponse(response)


@login_required
def my_products(request):
    user = request.user
    products = Substitution.objects.filter(user=user)
    context = {"products": products}
    return render(request, "my-products.html", context)
