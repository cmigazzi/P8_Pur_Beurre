import json

from django.shortcuts import render
from django.http import JsonResponse

from .forms import SearchForm
from .models import Product


def index(request):
    """Returns view for index url."""
    if request.method == "POST":
        term = json.loads(request.body.decode("utf-8"))["term"].lower()
        products = Product.objects.filter(name__istartswith=term).distinct()[:5]
        data = [{"name": p.name, "brand": p.brand.name} for p in products]
        return JsonResponse(data, safe=False)

    form = SearchForm()
    context = {"search_form": form}
    return render(request, "index.html", context)


def legals(request):
    """Returns view for legals url."""
    return render(request, "mentions-legales.html")


def search(request):
    """Returns view for search url."""
    product = request.GET.get("product")
    searched_product = Product.objects.filter(
                name=request.GET.get("product"))[0]
    results = Product.objects.filter(
        nutriscore__lt=searched_product.nutriscore)
    context = {"product": product,
               "results": results}
    return render(request, "results.html", context)
