from django.core.management.base import BaseCommand

from .api_to_database.api import Api
from .api_to_database.product_recorder import ProductRecorder


class Command(BaseCommand):
    """Represent custom command for database population."""

    help = "Request data from API to database"

    def handle(self, *args, **kwargs):
        """Handle getdata command."""
        n = 1
        self.stdout.write("Loading data from OpenFoodFacts...")
        products = Api().call()
        self.stdout.write("Populating database...")
        for product in products:
            if n != len(products):
                self.stdout.write(f"{n}/{len(products)} products.",
                                  ending="\r")
            else:
                self.stdout.write(f"{n}/{len(products)}")
            ProductRecorder(product)
            n += 1
        self.stdout.write("Database populating done successfully !")
