import json

from django.shortcuts import render
from django.http import JsonResponse

from .forms import SearchForm
from .models import Product


def index(request):
    if request.method == "POST":
        term = json.loads(request.body.decode("utf-8"))["term"].lower()
        products = Product.objects.filter(name__istartswith=term).distinct()[:5]
        data = [{"name": p.name, "brand": p.brand.name} for p in products]
        return JsonResponse(data, safe=False)

    form = SearchForm()
    context = {"search_form": form}
    return render(request, "index.html", context)


def legals(request):
    return render(request, "mentions-legales.html")


def search(request):
    product = request.GET.get("product")
    context = {"product": product}
    return render(request, "results.html", context)
