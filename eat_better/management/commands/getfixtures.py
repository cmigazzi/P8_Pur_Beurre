from itertools import chain

from django.core.management.base import BaseCommand
from django.core import serializers

from eat_better.models import Product, Category, Hierarchy, Brand, Nutriments
from .api_to_database.api import Api


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        api = Api()
        categories = api.CATEGORIES
        JSONSerializer = serializers.get_serializer("json")
        first_loop = True

        for category in categories:
            products = Product.objects.filter(categories__name=category)[:200]

            nutriments = Nutriments.objects.filter(
                id__in=[p.nutriments_id for p in products])

            brands = Brand.objects.filter(
                id__in=[p.brand_id for p in products])

            hierarchies = Hierarchy.objects.filter(product__in=products)

            categories_id = set([h.category_id for h in hierarchies])
            categories = Category.objects.filter(id__in=categories_id)

            if first_loop is True:
                all_products = products
                all_nutriments = nutriments
                all_brands = brands
                all_hierarchies = hierarchies
                all_categories = categories

            else:
                all_products.union(products)
                all_nutriments.union(nutriments)
                all_brands.union(brands)
                all_hierarchies.union(hierarchies)
                all_categories.union(categories)

        data = list(chain(
            all_nutriments,
            all_brands,
            all_categories,
            all_products,
            all_hierarchies))

        json_serializer = JSONSerializer()

        with open(f"fixtures/db.json", "w") as out:
            json_serializer.serialize(data, stream=out)
