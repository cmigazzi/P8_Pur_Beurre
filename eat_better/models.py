from django.db import models
from core.models import User


class Category(models.Model):
    """Define the category columns/attributes."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """String representation of the model."""
        return self.name


class Nutriments(models.Model):
    """Define the nutriments columns/attributes."""

    fat = models.DecimalField(max_digits=4, decimal_places=1)
    sugars = models.DecimalField(max_digits=4, decimal_places=1)
    saturated_fat = models.DecimalField(max_digits=4, decimal_places=1)
    salt = models.DecimalField(max_digits=6, decimal_places=3)


class Brand(models.Model):
    """Define the brand columns/attributes."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """String representation of the model."""
        return self.name


class Product(models.Model):
    """Define the product columns/attributes."""

    name = models.CharField(max_length=150)
    nutriscore = models.CharField(max_length=1)
    url = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, through="Hierarchy")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    nutriments = models.ForeignKey(Nutriments, on_delete=models.CASCADE)

    def __str__(self):
        """String representation of the model."""
        return self.name


class Hierarchy(models.Model):
    """Define the hierarchy columns/attributes."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        """String representation of the model."""
        return f"{self.product}, {self.category}, {self.level}"

    class Meta:
        """Order by level desc."""

        ordering = ("-level",)


class Substitution(models.Model):
    """Define the substitution columns/attributes."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original = models.ForeignKey(Product, on_delete=models.CASCADE,
                                 related_name="original")
    substitute = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name="substitute")

    def __str__(self):
        """String representation of the model."""
        return f"oridignal: {self.original}, substitue:{self.substitute}"
