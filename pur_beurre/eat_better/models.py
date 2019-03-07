from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    nutriscore = models.CharField(max_length=1)
    url = models.CharField(max_length=255)
    category = models.ManyToManyField("Category", through="Hierarchy")
    nutriments = models.OneToOneField("Nutriments", on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Hierarchy(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    level = models.IntegerField()


class Nutriments(models.Model):
    fats = models.DecimalField(max_digits=3, decimal_places=1)
    sugars = models.DecimalField(max_digits=3, decimal_places=1)
    saturated_fat = models.DecimalField(max_digits=3, decimal_places=1)
    salt = models.DecimalField(max_digits=4, decimal_places=3)
