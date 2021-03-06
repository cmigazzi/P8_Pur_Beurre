import json

from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .forms import SearchForm
from .models import Product, Substitution


def index(request):
    """Return view for index url."""
    if request.method == "POST":
        term = json.loads(request.body.decode("utf-8"))["term"].lower()
        products = Product.objects.filter(name__istartswith=term)  \
                                  .distinct()
        products_names = [p.name for p in products]
        delete_duplicates = list(set(products_names))
        data = [{"name": name} for name in delete_duplicates][:5]
        return JsonResponse(data, safe=False)

    searched_form = SearchForm()
    context = {"search_form": searched_form}
    return render(request, "index.html", context)


def legals(request):
    """Return view for legals url."""
    return render(request, "mentions-legales.html")


def search(request):
    """Return view for search url."""
    try:
        searched_product = Product.objects.filter(
                    name=request.GET.get("product"))[0]
        if searched_product.nutriscore == "a":
            is_healthy = True
            results = []
        else:
            results = []
            for hierarchy in searched_product.hierarchy_set.all():
                pre_results = Product.objects.filter(
                                nutriscore__lt=searched_product.nutriscore,
                                categories__name=hierarchy.category) \
                                .order_by("nutriscore")

                if len(results) == 0 and len(pre_results) != 0:
                    results = pre_results
                    if len(results) > 80:
                        break

                elif len(results) + len(pre_results) > 80:
                    results.union(pre_results)
                    break

                elif len(results) != 0:
                    results.union(pre_results)

            is_healthy = False

    except IndexError:
        searched_product = request.GET.get("product")
        results = []
        is_healthy = False

    context = {"product": searched_product,
               "is_healthy": is_healthy,
               "results": results}
    return render(request, "results.html", context)


def details(request, id_product):
    """Return view for details url."""
    try:
        product = Product.objects.get(id=id_product)
    except Product.DoesNotExist:
        raise Http404("Aucun produit trouvé.")
    else:
        context = {"product": product,
                   "nutriscore_url": f"img/nutriscore/{product.nutriscore}.png",
                   "nutriments": product.nutriments}
        return render(request, "details.html", context)


@require_http_methods(["POST"])
def save_substitute(request):
    """Handle ajax request to save d=the substitute."""
    if request.is_ajax():
        if request.user.is_authenticated:
            data = json.loads(request.body.decode("utf-8"))
            user = request.user
            try:
                original = Product.objects.get(id=data["original"])
                substitute = Product.objects.get(id=data["substitute"])
                Substitution.objects.create(user=user,
                                            original=original,
                                            substitute=substitute)
            except Product.DoesNotExist:
                response = {
                    "title": "Erreur",
                    "message": ("Impossible de retrouver "
                                "les produits à sauvegarder.")}
            else:
                response = {
                    "title": "Succès",
                    "message": "Le produit est sauvegardé !"}
        else:
            response = {
                "title": "Non connecté",
                "message": ("Connectez-vous pour pouvoir "
                            "sauvegarder des produits")
            }
    else:
        response = {
            "title": "Erreur",
            "message": "Erreur de requête"}
    return JsonResponse(response)


@login_required
def my_products(request):
    """Render favourites products view."""
    user = request.user
    products = Substitution.objects.filter(user=user)
    context = {"products": products}
    return render(request, "my-products.html", context)
