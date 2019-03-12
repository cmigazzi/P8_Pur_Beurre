"""Contains all the functions to get data from OpenFoodFacts API."""

import requests

from eat_better.models import Nutriments, Category, Brand, Product, Hierarchy


class Api():
    """Represent the API caller."""

    def __init__(self):
        self.CATEGORIES = ["Fromages",
                           "Biscuits et gâteaux",
                           "Produits à tartiner sucrés",
                           "Petit-déjeuners",
                           "Desserts"]
        self.FIELD_NEEDED = ["product_name_fr",
                             "categories",
                             "brands",
                             "nutriments",
                             "url",
                             "nutrition_grade_fr"]
        self.NUTRIMENTS = ["saturated-fat_100g",
                           "fat_100g",
                           "sugars_100g",
                           "salt_100g"
                           ]

    def call(self):
        """Request the OpenFoodFact API to get data.

        Returns:
            list -- list of dictionnary that represents a product

        """
        clean_products = []

        for category in self.CATEGORIES:
            payload = {"search_terms": f"{category}",
                       "search_tag": "category",
                       "sort_by": "unique_scans_n",
                       "page_size": 1000,
                       "json": 1}

            response = requests.get(
                            "https://fr.openfoodfacts.org/cgi/search.pl?",
                            params=payload)

            products = response["products"]

            for product in products:
                try:
                    for field in self.FIELD_NEEDED:
                        if product[field] in ('', None):
                            raise KeyError
                        if field == "nutriments":
                            for nutriment in self.NUTRIMENTS:
                                if product[field][nutriment] in ('', None):
                                    raise KeyError
                except KeyError:
                    print("Bad product")
                else:
                    clean_product = {
                        k: v for k, v in product.items()
                        if k in self.FIELD_NEEDED and v != ''}

                    clean_nutriments = {
                        k: v for k, v in product["nutriments"].items()
                        if k in self.NUTRIMENTS and v != ''}

                    clean_product["nutriments"] = clean_nutriments

                    product_renamed = self.rename_fields(clean_product,
                                                         category)

                    if product_renamed is False:
                        break

                    clean_products.append(product_renamed)

        return clean_products

    @staticmethod
    def rename_fields(product, category):
        product["name"] = product.pop("product_name_fr")
        product["nutriscore"] = product.pop("nutrition_grade_fr")
        product["brand"] = product.pop("brands").split(',')[0]
        categories = product["categories"].split(', ')
        try:
            main_category_id = categories.index(category)
        except ValueError:
            return False
        categories = categories[main_category_id:]
        product["categories"] = [c for c in enumerate(categories)]
        nutriments = product["nutriments"]
        nutriments["saturated_fat"] = nutriments.pop("saturated-fat_100g")
        nutriments["fat"] = nutriments.pop("fat_100g")
        nutriments["sugars"] = nutriments.pop("sugars_100g")
        nutriments["salt"] = nutriments.pop("salt_100g")
        product["nutriments"] = nutriments

        return product


class ProductRecorder():
    """Represent the recorder of products from API to database.

    Methods:
        save_nutriments -- save nutriments to database
        save_categories -- save categories to database
        save_brand -- save brand to database
        save_product -- save product to database
        save_hierarchy -- save categories hierarchy
    """

    def __init__(self, product):
        """Process product saving.

        Arguments:
            product {dict} -- product attributes
        """
        self.product_input = product
        self.nutriments = self.save_nutriments()
        self.brand = self.save_brand()
        self.categories = self.save_categories()
        self.product = self.save_product()
        self.save_hierarchy()

    def save_nutriments(self):
        """Save nutriments.

        Returns:
            [Nutriments object] -- Nutriments
        """
        data = self.product_input["nutriments"]
        nutriments = Nutriments.objects.create(**data)
        return nutriments

    def save_categories(self):
        """Save categories.

        Returns:
            [list] -- tuple (level, Category object)
        """
        categories = []
        for level, category in self.product_input["categories"]:
            c, created = Category.objects.get_or_create(name=category)
            categories.append((level, c))
        return categories

    def save_brand(self):
        """Save brand.

        Returns:
            [Brand object] -- Brand
        """
        brand, created = Brand.objects.get_or_create(
                                    name=self.product_input["brand"])
        return brand

    def save_product(self):
        """Save product.

        Returns:
            Product object -- Product
        """
        product = Product.objects.create(
                            name=self.product_input["name"],
                            url=self.product_input["url"],
                            nutriscore=self.product_input["nutriscore"],
                            brand=self.brand,
                            nutriments=self.nutriments
                                        )
        return product

    def save_hierarchy(self):
        """Save categories hierarchy."""
        for level, category in self.categories:
            Hierarchy.objects.create(product=self.product,
                                     category=category,
                                     level=level)
