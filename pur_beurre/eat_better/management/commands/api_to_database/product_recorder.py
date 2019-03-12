"""Contains ProductRecorder class to save data."""

from eat_better.models import Nutriments, Category, Brand, Product, Hierarchy


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
